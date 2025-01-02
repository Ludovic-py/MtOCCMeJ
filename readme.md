# Cable v4.1

Cable v4.1 is a graphical cabling application designed for interactive circuit layout and logical cable management. Users can create, modify, and analyze cable configurations to determine reliability and integrity within the system. The program features a user-friendly graphical interface developed with **Tkinter**, accompanied by essential features like cable linking, visualization of logical states, and simplification tools such as Boolean expressions and functions.

---

## Features

### Main Features:
- **Dynamic Cable Creation**:
  - Users input the number of cables during initialization.
  - The program automatically adjusts the spacing and appearance of cables in the graphical interface.

- **Cable Linking**:
  - Connect cables through vertical links to represent logical relationships.
  - **Left-click** to:
    - Create links between two cables (one above the other).
    - Remove existing links by clicking directly on the link.

- **Graphical Output**:
  - Right-click on a cable to open a separate window displaying its logical state in either:
    - **Boolean expressions**
    - **Function mode**

- **Boolean Algebra Simplification**:
  - Several simplification options are available:
    - **Development**: Expanding logical expressions.
    - **Factorization**: Compacting logical expressions.
    - **Raw Output**: Displaying unsimplified expressions.

- **Reliability Analysis**:
  - Automatically checks cabling reliability to confirm logical soundness.
  - Displays the reliability status:
    - `"Le cablage est fiable."` (Cabling is reliable).
    - `"Le cablage n'est pas fiable."` (Cabling is not reliable).

- **User-Friendly Interface**:
  - Dynamic resizing of elements adapts the graphical interface to the screen size.
  - Adjustable display modes for logical expressions and cables.

---

## How to Use

### Running the Program:
1. Launch `Cable v4.1` from the terminal or Python IDE.
2. A dialog box will appear allowing you to input the desired number of cables.
3. Once entered, the main graphical interface will display the cables.

### Operations:
1. **Creating Links**:
   - Click on a cable and then on another cable directly above or below to form a logical link.
2. **Deleting Links**:
   - Click on an existing vertical link to remove it.
3. **Viewing Cable Outputs**:
   - Right-click on a cable to open a new window displaying its logical state as either Boolean or Function output.
   - Customize the display mode or simplify the outputs using the available options in the pop-up window.
4. **Reliability Analysis**:
   - A reliability status will be displayed at the bottom of the main interface, dynamically updated as changes are made.

---

## Application Design

Cable v4.1 is built with modularity and flexibility in mind. Below are the primary components of the program:

### **1. Graphical Interface (Tkinter)**
- Handles the graphical layout of cables and associated elements in the


- **The way the connections are ordered matters** within the test, but the connections themselves are undirected.
    - For example, the sequence of `(1,2)` then `(3,2)` is different from `(3,2)` then `(1,2)`, even though the individual connections `(1,2)` or `(3,2)` are treated as the same regardless of direction (since they are undirected).

In other words, we are **testing specific sequences of how the connections are applied**, while still treating individual connections like `(1,2)` and `(2,1)` as identical.



1. 
    - Each cable has an **output** that depends on boolean logic applied to the inputs it receives.
    - For example:
        - The **upper cable's output** might be calculated using `OR` (`max` in boolean terms).
        - The **lower cable's output** might be calculated using `AND` (`min` in boolean terms).
1. **Reliability via Outputs:**
    - The system can be tested for reliability by checking if the boolean outputs on each cable match the expected outputs under specific input conditions.
    - If all outputs follow the expected boolean logic, the system is considered reliable.


### Example Case:
Consider **2 cables** (`C1` and `C2`) and **1 connection** between them:
- The **boolean inputs** to the cables are: `input1` and `input2`.

#### Logic:
1. Outputs for the **upper cable (C1)**:
**C1_output = input1 OR input2**
(This uses the boolean `OR` logic).
2. Outputs for the **lower cable (C2)**:
**C2_output = input1 AND input2**
(This uses the boolean `AND` logic).

#### Truth Table:
To validate the reliability, you can create a truth table for all possible inputs to the system and verify if the outputs match the expected behavior.

| `input1` | `input2` | `C1_output` (OR) | `C2_output` (AND) |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 |
- If the system reliably produces these outputs under every input condition, it is considered **functional and reliable**.





-To expand the testing process for a system with **`c` cables**, allowing for **`n` connections** (from 1 to `((c-1)c)/2` possible connections), we need to:
1. Dynamically handle a varying number of cables (`c`) and their connections (`n`).
2. Allow for testing **every possible order** of applying the connections while respecting the total number of cables.
3. Compute the outputs for the system based on boolean logic (`AND`, `OR`, etc.) for every permutation of the connections.
4. Validate outputs against the generated truth table under all possible input combinations.




1. **Eliminate Testing Beyond the Boundary:**
    - For `c` cables, calculate the **useful connection boundary** (using the expression `((c-1)c)/2`).
    - Only test subsets **with fewer connections than this boundary**.

2. **Focus on Finding the Smallest Reliable Subset:**
    - Start from the smallest possible connection subsets (e.g., `n = 1`) and incrementally test larger subsets until a reliable one is found.
    - Stop testing subsets entirely **if adding more connections isn’t required**.

3. **Testing Every Input Combination:**
    - Use the truth table as a reference to test each subset of connections across all possible input values for `c` cables.
    - If a subset of connections reliably produces outputs that match the expected truth table, mark it as reliable.

4. **Outputting Results:**
    - Return the **smallest reliable subset of connections**, along with the truth table for verification.
























exemple de tableau input/output pour un cablage avec 6 cables (C=6)
Tableau de vérité dynamique (Entrées -> Sorties attendues) :
((0, 0, 0, 0, 0, 0), [0, 0, 0, 0, 0, 0])
((0, 0, 0, 0, 0, 1), [1, 0, 0, 0, 0, 0])
((0, 0, 0, 0, 1, 0), [1, 0, 0, 0, 0, 0])
((0, 0, 0, 0, 1, 1), [1, 1, 0, 0, 0, 0])
((0, 0, 0, 1, 0, 0), [1, 0, 0, 0, 0, 0])
((0, 0, 0, 1, 0, 1), [1, 1, 0, 0, 0, 0])
((0, 0, 0, 1, 1, 0), [1, 1, 0, 0, 0, 0])
((0, 0, 0, 1, 1, 1), [1, 1, 1, 0, 0, 0])
((0, 0, 1, 0, 0, 0), [1, 0, 0, 0, 0, 0])
((0, 0, 1, 0, 0, 1), [1, 1, 0, 0, 0, 0])
((0, 0, 1, 0, 1, 0), [1, 1, 0, 0, 0, 0])
((0, 0, 1, 0, 1, 1), [1, 1, 1, 0, 0, 0])
((0, 0, 1, 1, 0, 0), [1, 1, 0, 0, 0, 0])
((0, 0, 1, 1, 0, 1), [1, 1, 1, 0, 0, 0])
((0, 0, 1, 1, 1, 0), [1, 1, 1, 0, 0, 0])
((0, 0, 1, 1, 1, 1), [1, 1, 1, 1, 0, 0])
((0, 1, 0, 0, 0, 0), [1, 0, 0, 0, 0, 0])
((0, 1, 0, 0, 0, 1), [1, 1, 0, 0, 0, 0])
((0, 1, 0, 0, 1, 0), [1, 1, 0, 0, 0, 0])
((0, 1, 0, 0, 1, 1), [1, 1, 1, 0, 0, 0])
((0, 1, 0, 1, 0, 0), [1, 1, 0, 0, 0, 0])
((0, 1, 0, 1, 0, 1), [1, 1, 1, 0, 0, 0])
((0, 1, 0, 1, 1, 0), [1, 1, 1, 0, 0, 0])
((0, 1, 0, 1, 1, 1), [1, 1, 1, 1, 0, 0])
((0, 1, 1, 0, 0, 0), [1, 1, 0, 0, 0, 0])
((0, 1, 1, 0, 0, 1), [1, 1, 1, 0, 0, 0])
((0, 1, 1, 0, 1, 0), [1, 1, 1, 0, 0, 0])
((0, 1, 1, 0, 1, 1), [1, 1, 1, 1, 0, 0])
((0, 1, 1, 1, 0, 0), [1, 1, 1, 0, 0, 0])
((0, 1, 1, 1, 0, 1), [1, 1, 1, 1, 0, 0])
((0, 1, 1, 1, 1, 0), [1, 1, 1, 1, 0, 0])
((0, 1, 1, 1, 1, 1), [1, 1, 1, 1, 1, 0])
((1, 0, 0, 0, 0, 0), [1, 0, 0, 0, 0, 0])
((1, 0, 0, 0, 0, 1), [1, 1, 0, 0, 0, 0])
((1, 0, 0, 0, 1, 0), [1, 1, 0, 0, 0, 0])
((1, 0, 0, 0, 1, 1), [1, 1, 1, 0, 0, 0])
((1, 0, 0, 1, 0, 0), [1, 1, 0, 0, 0, 0])
((1, 0, 0, 1, 0, 1), [1, 1, 1, 0, 0, 0])
((1, 0, 0, 1, 1, 0), [1, 1, 1, 0, 0, 0])
((1, 0, 0, 1, 1, 1), [1, 1, 1, 1, 0, 0])
((1, 0, 1, 0, 0, 0), [1, 1, 0, 0, 0, 0])
((1, 0, 1, 0, 0, 1), [1, 1, 1, 0, 0, 0])
((1, 0, 1, 0, 1, 0), [1, 1, 1, 0, 0, 0])
((1, 0, 1, 0, 1, 1), [1, 1, 1, 1, 0, 0])
((1, 0, 1, 1, 0, 0), [1, 1, 1, 0, 0, 0])
((1, 0, 1, 1, 0, 1), [1, 1, 1, 1, 0, 0])
((1, 0, 1, 1, 1, 0), [1, 1, 1, 1, 0, 0])
((1, 0, 1, 1, 1, 1), [1, 1, 1, 1, 1, 0])
((1, 1, 0, 0, 0, 0), [1, 1, 0, 0, 0, 0])
((1, 1, 0, 0, 0, 1), [1, 1, 1, 0, 0, 0])
((1, 1, 0, 0, 1, 0), [1, 1, 1, 0, 0, 0])
((1, 1, 0, 0, 1, 1), [1, 1, 1, 1, 0, 0])
((1, 1, 0, 1, 0, 0), [1, 1, 1, 0, 0, 0])
((1, 1, 0, 1, 0, 1), [1, 1, 1, 1, 0, 0])
((1, 1, 0, 1, 1, 0), [1, 1, 1, 1, 0, 0])
((1, 1, 0, 1, 1, 1), [1, 1, 1, 1, 1, 0])
((1, 1, 1, 0, 0, 0), [1, 1, 1, 0, 0, 0])
((1, 1, 1, 0, 0, 1), [1, 1, 1, 1, 0, 0])
((1, 1, 1, 0, 1, 0), [1, 1, 1, 1, 0, 0])
((1, 1, 1, 0, 1, 1), [1, 1, 1, 1, 1, 0])
((1, 1, 1, 1, 0, 0), [1, 1, 1, 1, 0, 0])
((1, 1, 1, 1, 0, 1), [1, 1, 1, 1, 1, 0])
((1, 1, 1, 1, 1, 0), [1, 1, 1, 1, 1, 0])
((1, 1, 1, 1, 1, 1), [1, 1, 1, 1, 1, 1])