import multiprocessing
import queue
import tkinter as tk
from functools import lru_cache
from itertools import combinations, islice, permutations, product
from multiprocessing import Pool, cpu_count
from tkinter import messagebox, scrolledtext, ttk
from typing import Dict, FrozenSet, Tuple

_DESCENDING_BITMASKS_CACHE = {}  # type: Dict[int, FrozenSet[int]]


def _get_descending_bitmasks(num_cables):
    # type: (int) -> FrozenSet[int]
    """Precompute bitmasks of all binary vectors sorted in descending order."""
    cached = _DESCENDING_BITMASKS_CACHE.get(num_cables)
    if cached is not None:
        return cached

    masks = {((1 << k) - 1) << (num_cables - k) for k in range(num_cables + 1)}
    frozen = frozenset(masks)
    _DESCENDING_BITMASKS_CACHE[num_cables] = frozen
    return frozen


def _apply_logic_mask(mask1, mask2, logic_func, all_ones_mask):
    # type: (int, int, str, int) -> int
    if logic_func == "OR":
        return mask1 | mask2
    if logic_func == "AND":
        return mask1 & mask2
    if logic_func == "XOR":
        return mask1 ^ mask2
    if logic_func == "NAND":
        return (mask1 & mask2) ^ all_ones_mask
    raise ValueError("logique non suportée: {}".format(logic_func))


@lru_cache(maxsize=None)
def _initial_wire_masks(num_cables):
    # type: (int) -> Tuple[int, ...]
    """
    For cable index c in [0, num_cables - 1], bit i (from MSB to LSB across 2^num_cables
    combinations in product([0, 1], repeat=num_cables)) holds input c for combination i.
    """
    total_combos = 1 << num_cables
    masks = []
    for cable_idx in range(num_cables):
        shift = num_cables - 1 - cable_idx
        mask = 0
        for combo_idx in range(total_combos):
            if (combo_idx >> shift) & 1:
                mask |= 1 << (total_combos - 1 - combo_idx)
        masks.append(mask)
    return tuple(masks)


def apply_logic(input1, input2, logic_func):
    """
    Fonction helper pour appliquer la logique booléenne.
    prends en charge : OR, AND, XOR, NAND.
    """
    if logic_func == "OR":
        return input1 or input2
    elif logic_func == "AND":
        return input1 and input2
    elif logic_func == "XOR":
        return input1 ^ input2
    elif logic_func == "NAND":
        return not (input1 and input2)
    else:
        raise ValueError("logique non suportée: {}".format(logic_func))


def boolean_calculations(num_cables, connections):
    """
    Générer table de vérité basée sur num_cable et connexions.
    """
    total_combos = 1 << num_cables
    all_ones_mask = (1 << total_combos) - 1
    wire_masks = list(_initial_wire_masks(num_cables))

    for input1, input2, upper_func, lower_func in connections:
        m1 = wire_masks[input1]
        m2 = wire_masks[input2]
        wire_masks[input1] = _apply_logic_mask(m1, m2, upper_func, all_ones_mask)
        wire_masks[input2] = _apply_logic_mask(m1, m2, lower_func, all_ones_mask)

    inputs = list(product([0, 1], repeat=num_cables))
    truth_table = []
    for combo_idx, input_combination in enumerate(inputs):
        bit_pos = total_combos - 1 - combo_idx
        outputs = [(wire_masks[c] >> bit_pos) & 1 for c in range(num_cables)]
        truth_table.append((input_combination, outputs))

    return truth_table


def is_ordered_descending(output):
    """
    Vérifier si la liste de sorties (output) est dans un ordre binaire décroissant (par exemple, [1, 1, 0, 0]).
    """
    return output == sorted(output, reverse=True)


def verify_reliability(truth_table):
    """
    Vérifier si le système de câblage est fiable en vérifiant toutes les sorties.
    """
    if not truth_table:
        return True

    num_cables = len(truth_table[0][1])
    valid_masks = _get_descending_bitmasks(num_cables)

    for _, outputs in truth_table:
        out_mask = 0
        for val in outputs:
            out_mask = (out_mask << 1) | (1 if val else 0)
        if out_mask not in valid_masks:
            return False
    return True


def generate_all_connections(num_cables):
    """
    Genere toutes connexions possibles pour les câbles en utilisant uniquement "OR" (supérieur)
    et "AND" (inférieur) pour chaque connexion.
    Chaque connexion = (input1, input2, "OR", "AND").
    """
    return [
        (input1, input2, "OR", "AND")
        for input1, input2 in combinations(range(num_cables), 2)
    ]


def _is_permutation_reliable(num_cables, permuted_subset, init_masks, all_ones_mask, valid_masks):
    wire_masks = list(init_masks)
    for input1, input2, upper_func, lower_func in permuted_subset:
        m1 = wire_masks[input1]
        m2 = wire_masks[input2]
        wire_masks[input1] = _apply_logic_mask(m1, m2, upper_func, all_ones_mask)
        wire_masks[input2] = _apply_logic_mask(m1, m2, lower_func, all_ones_mask)

    total_combos = 1 << num_cables
    for bit_pos in range(total_combos):
        out_mask = 0
        for c in range(num_cables):
            out_mask = (out_mask << 1) | ((wire_masks[c] >> bit_pos) & 1)
        if out_mask not in valid_masks:
            return False
    return True


def test_subset(args):
    num_cables, subset = args
    total_combos = 1 << num_cables
    all_ones_mask = (1 << total_combos) - 1
    init_masks = _initial_wire_masks(num_cables)
    valid_masks = _get_descending_bitmasks(num_cables)

    solutions = []
    for permuted_subset in permutations(subset):
        if _is_permutation_reliable(
            num_cables, permuted_subset, init_masks, all_ones_mask, valid_masks
        ):
            solutions.append(permuted_subset)
    return solutions


def _batched_subsets(all_possible_connections, connection_set_size, batch_size):
    iterator = combinations(all_possible_connections, connection_set_size)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def _search_worker_entry(num_cables, start_size, max_solutions, workers, msg_queue, stop_event):
    """Runs inside a background process so the Tkinter UI never blocks."""
    try:
        msg_queue.put(("log", "[ Launch ] Testing for {} cables, starting from {} connections".format(num_cables, start_size)))
        all_possible_connections = generate_all_connections(num_cables)
        solutions = []
        batch_size = max(workers * 8, 32)

        with Pool(workers) as pool:
            for connection_set_size in range(start_size, len(all_possible_connections) + 1):
                if stop_event.is_set():
                    msg_queue.put(("log", "[ Stop ] Search cancelled by user."))
                    break

                msg_queue.put(("log", "[ Update ] Testing combination subsets of size {}...".format(connection_set_size)))

                for batch in _batched_subsets(all_possible_connections, connection_set_size, batch_size):
                    if stop_event.is_set():
                        break

                    tasks = [(num_cables, subset) for subset in batch]
                    for result in pool.imap_unordered(test_subset, tasks, chunksize=8):
                        if stop_event.is_set():
                            break
                        if result:
                            for sol in result:
                                solutions.append(sol)
                                msg_queue.put(("solution", sol))
                                if len(solutions) >= max_solutions:
                                    msg_queue.put(("done", solutions[:max_solutions]))
                                    return

        msg_queue.put(("done", solutions))
    except Exception as exc:
        msg_queue.put(("error", str(exc)))


class LogicNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Boolean Wiring Explorer (Search & Verify)")
        self.root.geometry("760x620")

        self.ctx = multiprocessing.get_context("spawn")
        self.msg_queue = None
        self.stop_event = None
        self.worker_proc = None
        self.poll_id = None

        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Tab 1: Parallel Search ---
        search_tab = ttk.Frame(notebook, padding=12)
        notebook.add(search_tab, text="Search (MT34)")

        params_frame = ttk.LabelFrame(search_tab, text="Search Parameters", padding=10)
        params_frame.pack(fill=tk.X)

        ttk.Label(params_frame, text="Cables:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.cables_var = tk.StringVar(value="4")
        ttk.Entry(params_frame, textvariable=self.cables_var, width=8).grid(row=0, column=1, padx=(0, 16))

        ttk.Label(params_frame, text="Start Size:").grid(row=0, column=2, sticky=tk.W, padx=(0, 6))
        self.start_size_var = tk.StringVar(value="1")
        ttk.Entry(params_frame, textvariable=self.start_size_var, width=8).grid(row=0, column=3, padx=(0, 16))

        ttk.Label(params_frame, text="Max Solutions:").grid(row=0, column=4, sticky=tk.W, padx=(0, 6))
        self.max_sol_var = tk.StringVar(value="3")
        ttk.Entry(params_frame, textvariable=self.max_sol_var, width=8).grid(row=0, column=5, padx=(0, 16))

        ttk.Label(params_frame, text="Workers:").grid(row=0, column=6, sticky=tk.W, padx=(0, 6))
        self.workers_var = tk.StringVar(value=str(cpu_count() or 1))
        ttk.Entry(params_frame, textvariable=self.workers_var, width=8).grid(row=0, column=7)

        btn_frame = ttk.Frame(search_tab)
        btn_frame.pack(fill=tk.X, pady=8)

        self.start_btn = ttk.Button(btn_frame, text="Start Search", command=self.start_search)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_search, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(btn_frame, text="Clear Output", command=lambda: self.search_log.delete("1.0", tk.END)).pack(
            side=tk.RIGHT
        )

        self.search_log = scrolledtext.ScrolledText(search_tab, wrap=tk.WORD, font=("Consolas", 10))
        self.search_log.pack(fill=tk.BOTH, expand=True)

        # --- Tab 2: Verify Single Wiring ---
        verify_tab = ttk.Frame(notebook, padding=12)
        notebook.add(verify_tab, text="Verify Wiring (T3)")

        v_top = ttk.Frame(verify_tab)
        v_top.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(v_top, text="Cables:").pack(side=tk.LEFT, padx=(0, 6))
        self.verify_cables_var = tk.StringVar(value="5")
        ttk.Entry(v_top, textvariable=self.verify_cables_var, width=8).pack(side=tk.LEFT, padx=(0, 14))

        ttk.Button(v_top, text="Run Truth Table & Check", command=self.run_verify).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(v_top, text="Clear", command=lambda: self.verify_log.delete("1.0", tk.END)).pack(side=tk.RIGHT)

        ttk.Label(
            verify_tab,
            text="Connections (one tuple per line: cable1, cable2, upper_logic, lower_logic):",
        ).pack(anchor=tk.W, pady=(0, 4))

        default_conns = "\n".join([
            "(0, 2, 'OR', 'AND')",
            "(1, 3, 'OR', 'AND')",
            "(0, 1, 'OR', 'AND')",
            "(2, 3, 'OR', 'AND')",
            "(1, 2, 'OR', 'AND')",
        ])
        self.conn_input = scrolledtext.ScrolledText(verify_tab, height=6, font=("Consolas", 10))
        self.conn_input.pack(fill=tk.X, pady=(0, 8))
        self.conn_input.insert("1.0", default_conns)

        self.verify_log = scrolledtext.ScrolledText(verify_tab, wrap=tk.WORD, font=("Consolas", 10))
        self.verify_log.pack(fill=tk.BOTH, expand=True)

    def _append_search_log(self, text):
        self.search_log.insert(tk.END, text + "\n")
        self.search_log.see(tk.END)

    def start_search(self):
        try:
            num_cables = int(self.cables_var.get())
            start_size = int(self.start_size_var.get())
            max_solutions = int(self.max_sol_var.get())
            workers = int(self.workers_var.get())
            if num_cables < 2 or start_size < 1 or max_solutions < 1 or workers < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive integers (cables >= 2, others >= 1).")
            return

        self.msg_queue = self.ctx.Queue()
        self.stop_event = self.ctx.Event()
        self.worker_proc = self.ctx.Process(
            target=_search_worker_entry,
            args=(num_cables, start_size, max_solutions, workers, self.msg_queue, self.stop_event),
        )
        self.worker_proc.start()

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.poll_id = self.root.after(100, self._poll_queue)

    def stop_search(self):
        if self.stop_event is not None:
            self.stop_event.set()
        self.stop_btn.config(state=tk.DISABLED)

    def _finish_search_ui(self):
        if self.poll_id is not None:
            self.root.after_cancel(self.poll_id)
            self.poll_id = None
        if self.worker_proc is not None:
            self.worker_proc.join(timeout=1.0)
            self.worker_proc = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def _poll_queue(self):
        if self.msg_queue is None:
            return

        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "log":
                    self._append_search_log(payload)
                elif kind == "solution":
                    self._append_search_log("Found solution:")
                    for step in payload:
                        self._append_search_log("  {}".format(step))
                elif kind == "done":
                    self._append_search_log("[  End!  ] Total solutions collected: {}".format(len(payload)))
                    self._finish_search_ui()
                    return
                elif kind == "error":
                    self._append_search_log("[ Error ] {}".format(payload))
                    self._finish_search_ui()
                    return
        except queue.Empty:
            pass

        self.poll_id = self.root.after(100, self._poll_queue)

    def run_verify(self):
        self.verify_log.delete("1.0", tk.END)
        try:
            num_cables = int(self.verify_cables_var.get())
            raw_lines = [line.strip() for line in self.conn_input.get("1.0", tk.END).splitlines() if line.strip()]
            connections = []
            for line in raw_lines:
                parsed = eval(line, {"__builtins__": {}})  # noqa: S307
                if not (isinstance(parsed, tuple) and len(parsed) == 4):
                    raise ValueError("Expected 4-tuple, got: {}".format(line))
                connections.append(parsed)

            truth_table = boolean_calculations(num_cables, connections)
            self.verify_log.insert(tk.END, "Truth Table (Inputs -> Outputs):\n")
            for inputs, outputs in truth_table:
                self.verify_log.insert(tk.END, "Inputs: {} -> Outputs: {}\n".format(inputs, outputs))

            if verify_reliability(truth_table):
                self.verify_log.insert(tk.END, "\ncablage fiable.\n")
            else:
                self.verify_log.insert(tk.END, "\ncablage pas fiable.\n")
        except Exception as exc:
            messagebox.showerror("Verification Error", str(exc))


if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = LogicNetworkApp(root)
    root.mainloop()