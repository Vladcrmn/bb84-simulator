# BB84 Quantum Key Distribution Simulator

A simple educational simulation of the **BB84 quantum key distribution protocol**, implemented in Python.

The goal of this project is to understand the fundamental mechanisms behind quantum key distribution by implementing the protocol step by step.

## Current Version — V3

The current version implements the BB84 protocol between Alice and Bob, an optional **intercept-resend attack by Eve**, and **Quantum Bit Error Rate (QBER) estimation**.

The simulation includes:

* Random bit generation for Alice
* Random selection of Z and X bases
* Quantum state preparation
* Random basis selection by Bob
* Quantum measurement simulation
* Basis reconciliation (sifting)
* Optional Eve intercept-resend attack
* Public sampling of the sifted key
* QBER estimation
* Removal of publicly revealed sample bits
* QBER threshold verification
* Protocol continuation or abort decision

## BB84 States

The simulation uses the following correspondence:

| Basis | Bit | Quantum state |
| ----- | --- | ------------- |
| Z     | 0   | `|H⟩`         |
| Z     | 1   | `|V⟩`         |
| X     | 0   | `|+⟩`         |
| X     | 1   | `|-⟩`         |

with

$$
|+\rangle = \frac{|H\rangle + |V\rangle}{\sqrt{2}}
$$

and

$$
|-\rangle = \frac{|H\rangle - |V\rangle}{\sqrt{2}}
$$

When a state is measured in the same basis in which it was prepared, the corresponding bit is obtained deterministically.

When it is measured in the other basis, the result is simulated as random:

$$
P(0) = P(1) = \frac{1}{2}
$$

## V2 — Eavesdropping

Eve can perform an **intercept-resend attack**.

For every transmitted state, Eve:

1. intercepts Alice's quantum state,
2. randomly chooses a measurement basis,
3. measures the state,
4. prepares a new state according to her measurement,
5. sends the newly prepared state to Bob.

If Eve chooses the wrong basis, her measurement can disturb the transmitted quantum state.

This disturbance can later appear as errors in Alice and Bob's sifted keys.

## V3 — QBER

Alice and Bob estimate the **Quantum Bit Error Rate (QBER)** by publicly revealing a random sample of their sifted keys.

The QBER is defined as:

$$
QBER =
\frac{\text{number of different sampled bits}}
{\text{number of sampled bits}}
$$

The revealed bits are then discarded and are not used as part of the remaining secret key.

In this educational simulator, a threshold of approximately **11%** is used as a reference value for ideal BB84 under asymptotic one-way post-processing assumptions.

If the estimated QBER exceeds the threshold, the protocol is aborted.

Otherwise, Alice and Bob may continue to the next post-processing stages.

A full intercept-resend attack is expected to introduce a significant error rate, making the attack detectable statistically.

A high QBER indicates that the quantum channel has been disturbed. This may be caused by eavesdropping, channel noise, or implementation imperfections; therefore QBER does not by itself prove that Eve is present.

## Protocol Flow

```text
Alice
  │
  ├── Generate random bits
  ├── Choose random bases
  └── Prepare quantum states
          │
          ▼
      Eve enabled?
       /       \
     no         yes
     │           │
     │       Intercept
     │       Measure
     │       Resend
     │           │
     └──────┬────┘
            ▼
           Bob
            │
      Choose bases
      Measure states
            │
            ▼
          Sifting
            │
            ▼
    Public sample selection
            │
            ▼
      QBER estimation
            │
            ▼
     Discard sample bits
            │
            ▼
     QBER acceptable?
       /          \
     yes           no
      │             │
   Continue        Abort
```

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

`main.py` executes complete BB84 simulations.

## Run

Clone the repository and run:

```bash
python src/main.py
```

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

## Roadmap

### V1 — Core BB84 Protocol ✅

* Alice bit generation
* Random basis selection
* Quantum state preparation
* Bob measurement
* Basis reconciliation
* Sifted key generation

### V2 — Eavesdropping ✅

* Eve intercept-resend attack
* Random Eve measurement bases
* State re-preparation and retransmission

### V3 — QBER ✅

* Public sampling of the sifted key
* QBER estimation
* Removal of revealed bits
* QBER threshold verification
* Protocol continuation or abort

### V4 — Error Correction

Reconcile discrepancies that may remain between Alice and Bob's keys while minimizing the information revealed over the public classical channel.

### Later

Possible extensions include:

* Privacy amplification
* More realistic channel noise
* Partial interception by Eve
* Statistical experiments
* Interactive visualization of the BB84 protocol

## Purpose

This project is intended for educational purposes.

It focuses on understanding the principles of quantum key distribution and BB84 rather than reproducing a complete physical QKD implementation.
