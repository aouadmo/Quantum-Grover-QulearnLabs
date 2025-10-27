# Capstone Project – Grover’s Algorithm (4 Qubits)

A hands-on capstone to implement **Grover’s search** on **4 qubits** using only a small, fixed gate set. You’ll build a generic oracle for any 4-bit solution string (e.g., `"0010"`) and apply the Grover **diffuser** the optimal number of times to amplify the target state.

---

## 🎯 Learning Objectives

- Construct **uniform superposition** using Hadamards.
- Encode an **arbitrary 4-bit oracle** as a **phase flip** using only `X`, `H`, and **multi-controlled X** (`mcx`).
- Implement the **Grover diffuser** as inversion about the mean (again using only `X`, `H`, `mcx`).
- Choose the **optimal iteration count** for a 4-qubit search (**N = 16**).

---

## 🗂️ Project Structure

```
capstone-project/
├── capstone_project.py          # Your implementation lives here
├── test_capstone_project.py     # Unit tests
├── README.md                    # This document
└── (optional) requirements.txt
```

Key functions in `capstone_project.py`:

- `two_qubit_grover_11()`  
  Provided example of Grover on 2 qubits (solution = `11`). Uses `cz` for clarity.
- `four_qubit_grover(solution: str)`  ⟵ **Implement this**  
  Builds a 4-qubit Grover circuit that marks any 4-bit solution string.

**Constraints**

- Allowed gates: **Hadamard (`h`)**, **Pauli-X (`x`)**, and **multi-controlled X (`mcx`)**.
- **No measurements** inside the function.
- Do **not** modify code outside the marked block.

---

## 🧩 How Grover Works (Concise)

For a search space of size \(N=2^n\) (here **N = 16**, **n = 4**):

1. **Initialization**  
   Apply `H` to every qubit → uniform superposition over all \(2^4\) basis states.

2. **Oracle \(O_s\)** (phase flip only on the marked state \(|sangle\))  
   - **Mask** zeros: for each bit \(s[i]=0\), apply `X(i)` so that \(|sangle \mapsto |1111angle`.  
   - **Apply CZ on \(|1111angle\)** using only `H`/`mcx`:  
     `H(target) → MCX(controls, target) → H(target)`  
     This acts like a **phase flip** on \(|1111angle\).  
   - **Unmask**: reapply the same `X` gates where \(s[i]=0\).

3. **Diffuser \(D\)** (inversion about the mean)  
   Standard construction using the same trick to phase-flip \(|0000angle\):
   ```
   H on all
   X on all
   H on last;  MCX(controls=[0,1,2], target=3);  H on last
   X on all
   H on all
   ```

4. **Iterations**  
   Optimal number ≈ \(\left\lfloor \frac{\pi}{4}\sqrt{N} \right\rfloor\).  
   For **N = 16**, \(\sqrt{N}=4 \Rightarrow \frac{\pi}{4}\sqrt{N} \approx \pi \approx 3.14\) → **3 iterations**.

---

## ✅ Requirements

- **Python** ≥ 3.8
- **Qiskit** 1.x (Terra)

Install (minimal):
```bash
pip install qiskit
```

Optional (simulators/plots):
```bash
pip install qiskit-aer matplotlib
```

If the project includes a `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🏃 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or
   pip install qiskit qiskit-aer
   ```

2. **Run tests**
   ```bash
   python -m unittest test_capstone_project.py
   ```

You should see all tests pass. One test checks that, for `solution="0000"`, the output distribution has **≥ 0.93** probability on the marked state after your Grover iterations.

---

## 🔧 Implementation Guide (4-Qubit)

### 1) Oracle for an arbitrary 4-bit `solution`
- **Mask zeros** with `X` so that \(|\text{solution}\rangle\) becomes \(|1111\rangle\).
- Convert `CZ` on \(|1111\rangle\) into `H–MCX–H` on the **last qubit**:
  ```python
  last = num_qubits - 1
  qc.h(last)
  qc.mcx([0,1,2], last)
  qc.h(last)
  ```
- **Unmask** by applying the same `X` gates again on bits where `solution[i]=='0'`.

### 2) Diffuser
- Same `H–X–H–MCX–H–X–H` pattern, but applied to flip the phase of \(|0000\rangle\).

### 3) Iteration Count
- Repeat: **Oracle → Diffuser** exactly **3 times** for 4 qubits.

---

## 🧪 Example Usage (statevector check)

*(Not required for grading, but useful for inspection.)*
```python
from qiskit.quantum_info import Statevector
from capstone_project import four_qubit_grover

qc = four_qubit_grover("0010")
sv = Statevector.from_instruction(qc)
probs = sv.probabilities_dict()
print(sorted(probs.items(), key=lambda kv: kv[1], reverse=True)[:5])
```

---

## 🔍 Troubleshooting

- **“return outside function”**  
  Ensure all lines between the “ONLY EDIT UNDER HERE / ABOVE HERE” markers are **indented inside** the `four_qubit_grover` function.
- **Low success probability (< 0.93)**  
  - Check that you **masked** zeros correctly before the oracle’s `H–MCX–H`.  
  - Ensure you **unmask** after the oracle.  
  - Confirm you run **3 full iterations** (Oracle→Diffuser) after the initial Hadamards.
- **Gate restrictions**  
  Use **only** `h`, `x`, and `mcx`. No `z`, `cz`, `measure`, or transpile tricks.

---

## 🧠 Why 3 Iterations?

The amplitude amplification angle is \(	heta\) with \(\sin(	heta)=1/\sqrt{N}=1/4\).  
Each Grover iteration rotates by \(2\theta\). After \(k\) iterations, the success probability is \(\sin^2((2k+1)\theta)\). The value \(k\approx \frac{\pi}{4}\sqrt{N}\) maximizes this; for **N = 16**, **k = 3** is optimal.

---

## 📚 References

- L. K. Grover, *A fast quantum mechanical algorithm for database search*, STOC’96.  
- Qiskit Textbook: *Grover’s algorithm* (quantum amplitude amplification).  
- Qiskit API: `QuantumCircuit.mcx` (multi-controlled X).

---

## 🏁 Deliverable Checklist

- [ ] `four_qubit_grover(solution)` generates a 4-qubit Grover circuit.  
- [ ] Uses only **H**, **X**, **MCX**.  
- [ ] No measurements.  
- [ ] 3 Grover iterations.  
- [ ] Unit tests pass (`≥ 0.93` success probability for `"0000"`).
