# DES and KE-DES

Academic implementation (Computer Security) of **DES** and **KE-DES**
(Key-Based Enhancement of DES, Reyad et al., 2021), written by hand in Python
with no external cryptographic libraries.

KE-DES is a study variant and must **not** be considered cryptographically
secure.

## Files

| File | Purpose |
|------|---------|
| `utilities.py` | hex/binary conversion, `permute`, `xor`, shifts |
| `key_generator.py` | DES and KE-DES key schedules (PC-1, PC-2, rotations, Odd/Even) |
| `function_F.py` | round function: expansion input, S-boxes, P permutation |
| `des.py` | Feistel processing for DES and KE-DES (encrypt/decrypt) |
| `main.py` | command-line menu and assignment demo |
| `tests/` | `unittest` validation suite |

## Requirements

- Python 3 (standard library only).

## How to run

```bash
python3 main.py            # interactive menu
python3 main.py --demo     # run the two assignment datasets and exit
python3 main.py --debug    # same, but show the internal diagnostic prints
```

## How to run the tests

```bash
python3 -m unittest discover -v
```

## DES (summary)

64-bit block, 64-bit key (56 effective), 16 Feistel rounds. Each round uses a
48-bit subkey `Kn` and the function `F` (expansion E, XOR, 8 S-boxes,
permutation P). Decryption reuses the same process with reversed subkeys.

## KE-DES (summary)

Same Feistel structure as DES, with two changes:

1. **Key schedule:** an Odd/Even transformation defines the initial halves.
2. **Expansion:** the standard expansion `E` is replaced by a 48-bit
   **K-D (Key-Distribution)** build: `PC1_KD(8) || R(32) || PC2_KD(8)`,
   where `PC1_KD` is taken from the original key and `PC2_KD` changes per
   round. Decryption reverses the subkeys and the per-round `PC2_KD`
   selections.

## Paper ambiguity (documented interpretation)

The paper is inconsistent about the initial halves:

- The **literal Odd/Even pseudocode** produces `D0 = 0101...`.
- **Table III** of the paper reports `D0 = 1010...` (consistent with the
  published `K1` and `K2`).

This implementation applies a **minimal one-position rotation** to the `D` half
so that `D0`, `K1` and `K2` match the published values exactly.
`odd_even_transformation()` itself follows the paper's pseudocode faithfully.
This is a best-effort interpretation used to reproduce the published results;
it is **not** a claim about what the authors definitively intended.

## Known DES test vector

```
Plaintext:  0123456789ABCDEF
Key:        133457799BBCDFF1
Ciphertext: 85E813540F0AB405
```

## Assignment demo / evidence

Run:

```bash
python3 main.py --demo
```

It prints both deterministic datasets comparing **DES vs KE-DES** on the same
plaintext and key: both ciphertexts, the decrypted roundtrip with PASS/FAIL,
and the key-generation time of each algorithm. To keep a copy of the evidence,
capture the output, for example:

```bash
python3 main.py --demo | tee evidenke-ke-des.txt
```

Dataset 1: plaintext `0123456789ABCDEF`, key `133457799BBCDFF1`.
Dataset 2: plaintext `A1B2C3D4E5F60718`, key `0F1E2D3C4B5A6978`.
