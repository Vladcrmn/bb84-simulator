# BB84 Quantum Key Distribution Simulator

A simple educational simulation of the **BB84 quantum key distribution protocol**, implemented in Python.

The goal of this project is to understand the fundamental mechanisms behind quantum key distribution by implementing the protocol step by step.

## Current Version — V1

The current version simulates BB84 communication between Alice and Bob without an eavesdropper.

The simulation includes:

* Random bit generation for Alice
* Random selection of Z and X bases
* Quantum state preparation
* Random basis selection by Bob
* Quantum measurement simulation
* Basis reconciliation (sifting)
* Shared key generation

When Alice and Bob use the same basis, Bob obtains the corresponding bit deterministically.

When Bob measures using a different basis, the result is randomly generated with probability:

$$
P(0) = P(1) = \frac{1}{2}
$$

## BB84 States

The simulation uses the following correspondence:

| Basis | Bit | Quantum state |
| ----- | --- | ------------- |
| Z | 0 | \|H⟩ |
| Z | 1 | \|V⟩ |
| X | 0 | \|+⟩ |
| X | 1 | \|-⟩ |

with

$$
|+\rangle = \frac{|H\rangle + |V\rangle}{\sqrt{2}}
$$

$$
|-\rangle = \frac{|H\rangle - |V\rangle}{\sqrt{2}}
$$

## Project Structure

```text
bb84-simulator/
│
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── bb84.py
│
└── tests/
    ├── __init__.py
    └── test_bb84.py

```

`bb84.py` contains the implementation of the protocol operations.

`main.py` executes a complete BB84 simulation.

## Run

Clone the repository and run:

```bash
python src/main.py
```

## Example

```text
Alice bits   : [1, 0, 1, 0, 1]
Alice bases  : [Z, X, Z, X, Z]
Alice states : [V, +, V, +, V]

Bob bases    : [Z, Z, Z, X, X]
Bob results  : [1, 1, 1, 0, 0]

Alice key    : [1, 1, 0]
Bob key      : [1, 1, 0]
```
## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests -v

```

## Roadmap

### V2 — Eavesdropping

Add Eve using an **intercept-resend attack**.

Eve will:

1. intercept Alice's quantum states,
2. randomly choose measurement bases,
3. measure the states,
4. prepare new states according to her measurements,
5. send them to Bob.

### V3 — QBER

Calculate the **Quantum Bit Error Rate (QBER)** and demonstrate how Alice and Bob can detect the presence of an eavesdropper.

### Later

Possible extensions include error correction, privacy amplification and more detailed visualization of the BB84 protocol.

## Purpose

This project is intended for educational purposes and focuses on understanding the principles of quantum key distribution rather than simulating a complete physical quantum communication system.
