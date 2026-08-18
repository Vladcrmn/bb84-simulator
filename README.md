# BB84 Quantum Key Distribution Simulator

A simple educational simulation of the **BB84 quantum key distribution protocol**, implemented in Python.

The goal of this project is to understand the fundamental mechanisms behind quantum key distribution by implementing the protocol step by step.

## Current Version — V4

The current version implements the BB84 protocol between Alice and Bob, an optional **intercept-resend attack by Eve**, **Quantum Bit Error Rate (QBER) estimation**, educational error correction, and privacy amplification.

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
* Parity-based error detection by blocks
* Dichotomic error localization
* Correction of Bob's erroneous bits
* Reconciled-key verification
* SHA-256-based privacy amplification
* Final shared secret key generation

## BB84 States

The simulation uses the following correspondence:

| Basis | Bit | Quantum state |
| ----- | --- | ------------- |
| Z     | 0   | \|H⟩           |
| Z     | 1   | \|V⟩           |
| X     | 0   | \|+⟩           |
| X     | 1   | \|-⟩           |

with

$$
|+\rangle =
\frac{|H\rangle + |V\rangle}{\sqrt{2}}
$$

and

$$
|-\rangle =
\frac{|H\rangle - |V\rangle}{\sqrt{2}}
$$

When a state is measured in the same basis in which it was prepared, the corresponding bit is obtained deterministically.

When it is measured in the other basis, the result is simulated as random:

$$
P(0) = P(1) = \frac{1}{2}
$$

## V1 — Core BB84 Protocol

Alice generates a random sequence of bits and randomly chooses either the Z or X basis for every bit.

The bits and bases determine the quantum states sent through the quantum channel.

Bob independently chooses random measurement bases. If Bob uses the same basis as Alice, he obtains the correct bit. If he uses the other basis, the result is random.

Alice and Bob then publicly compare only their bases. They keep the bits corresponding to positions where their bases were identical.

This process is called **sifting**.

## V2 — Eavesdropping

Eve can perform an **intercept-resend attack**.

For every transmitted state, Eve:

1. intercepts Alice's quantum state,
2. randomly chooses a measurement basis,
3. measures the state,
4. prepares a new state according to her result,
5. sends the newly prepared state to Bob.

If Eve chooses the wrong basis, her measurement can disturb the transmitted quantum state.

This disturbance can later appear as errors in Alice and Bob's sifted keys.

## V3 — QBER Estimation

Alice and Bob estimate the **Quantum Bit Error Rate** by publicly revealing a random sample of their sifted keys.

The QBER is defined as:

$$
QBER =
\frac{\text{number of different sampled bits}}
{\text{number of sampled bits}}
$$

The publicly revealed sample bits are discarded and are not used in the remaining key.

In this educational simulator, a threshold of approximately **11%** is used as a reference value for ideal BB84 under asymptotic one-way post-processing assumptions.

If the estimated QBER exceeds the threshold, the protocol is aborted.

A high QBER indicates that the quantum channel has been disturbed. This may be caused by eavesdropping, channel noise, or implementation imperfections. Therefore, the QBER does not by itself prove that Eve is present.

## V4 — Error Correction and Privacy Amplification

If the estimated QBER is acceptable, Alice and Bob continue with classical post-processing.

### Error Correction

The remaining keys are divided into blocks of eight bits.

Alice and Bob compare the parity of corresponding blocks:

$$
parity(block) =
\left(\sum block_i\right) \bmod 2
$$

If the parities are identical, the simulator assumes that the block does not contain a detectable error.

If the parities differ, the simulator uses a dichotomic search:

1. divide the block into two parts,
2. compare the parity of the left halves,
3. keep the half containing the error,
4. repeat the process until one bit remains,
5. flip Bob's incorrect bit.

The local position of the error inside the block is converted into a global position in Bob's complete key.

The protocol continues only if Bob's corrected key is identical to Alice's remaining key.

### Limitations of the Error-Correction Method

This is a simplified educational correction method.

It works mainly when there is one detectable error per block. More generally, a parity difference detects an odd number of errors.

An even number of errors in the same block may remain undetected because the two blocks can have identical parity.

A production QKD system would use a complete reconciliation protocol such as **Cascade**, **Winnow**, or an error-correcting code such as an **LDPC code**.

### Privacy Amplification

Even after error correction, Eve may possess partial information about the reconciled key.

Alice and Bob therefore independently:

1. convert the corrected bit sequence into text,
2. compute its SHA-256 digest,
3. convert the hexadecimal digest into 256 bits,
4. keep a shorter final key.

For this educational simulation, the length of the final key is:

```python
min(256, len(reconciled_key) // 2)
```

For example:

| Reconciled key | Final key |
| -------------- | --------- |
| 100 bits       | 50 bits   |
| 400 bits       | 200 bits  |
| 1,000 bits     | 256 bits  |

Because Alice and Bob hash identical reconciled keys, they obtain identical final keys.

The SHA-256 construction and the fixed one-half reduction are pedagogical choices.

A real BB84 implementation requires:

* a rigorously calculated secret-key length,
* public-information leakage accounting,
* finite-key security analysis,
* a formally specified universal-hash privacy-amplification procedure.

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
      │           Abort
      ▼
 Split key into blocks
      │
      ▼
 Compare block parities
      │
      ▼
 Locate and correct errors
      │
      ▼
 Reconciled keys identical?
       /          \
     yes           no
      │             │
      │           Abort
      ▼
 Privacy amplification
      │
      ▼
 Final shared secret key
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

`test_bb84.py` contains unit tests for all four versions of the project.

## Run

Clone the repository and run:

```bash
python src/main.py
```

## Tests

Run the complete test suite with:

```bash
python -m unittest discover -s tests -v
```

The current version contains **21 unit tests** covering:

* bit and basis generation,
* quantum-state preparation,
* quantum measurement,
* sifting,
* QBER calculation and estimation,
* parity calculation,
* block splitting,
* error detection and localization,
* error correction,
* key conversion and hashing,
* digest conversion,
* privacy amplification.

## Roadmap

### V1 — Core BB84 Protocol ✅

* Alice bit generation
* Random basis selection
* Quantum state preparation
* Bob measurement
* Basis reconciliation
* Sifted-key generation

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

### V4 — Error Correction and Privacy Amplification ✅

* Block parity calculation
* Detection of blocks with different parity
* Dichotomic error localization
* Correction of Bob's erroneous bits
* Reconciled-key verification
* SHA-256 hashing
* Digest conversion to bits
* Shortened final shared key

### Possible Extensions

* More realistic quantum-channel noise
* Partial interception by Eve
* Statistical experiments over many simulations
* Complete Cascade reconciliation with several shuffled passes
* Public-information leakage accounting
* Universal-hash privacy amplification
* Finite-key security analysis
* Interactive visualization of the complete protocol

## Educational Purpose

This project is intended for educational purposes.

It focuses on understanding the principles of quantum key distribution and the BB84 protocol rather than reproducing a production-ready physical QKD system.
