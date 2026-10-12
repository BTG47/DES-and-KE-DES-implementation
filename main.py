import contextlib
import io
import sys
import time

from utilities import hex_to_binary, binary_to_hex
from key_generator import key_generation, ke_des_generation
from des import des_process, k_des_process

DEBUG = "--debug" in sys.argv
DEMO = "--demo" in sys.argv

DATASETS = [
    ("0123456789ABCDEF", "133457799BBCDFF1"),
    ("A1B2C3D4E5F60718", "0F1E2D3C4B5A6978"),
]

HEX_DIGITS = set("0123456789abcdefABCDEF")

MENU = """=== DES / KE-DES ===
1. DES
2. KE-DES
3. Assignment demo
4. Exit"""


def quiet():
    if DEBUG:
        return contextlib.nullcontext()
    return contextlib.redirect_stdout(io.StringIO())


def bits_to_hex(bits):
    return "".join(binary_to_hex(bits))


def read_hex_64(prompt):
    while True:
        value = input(prompt).strip()
        if len(value) == 16 and all(char in HEX_DIGITS for char in value):
            return value
        print("Error: exactly 16 hexadecimal characters (64 bits) are required.")


def run_algorithm(choice):
    operation = input("Operation:\n1. Encrypt\n2. Decrypt\n> ").strip()
    while operation not in ("1", "2"):
        print("Error: choose 1 or 2.")
        operation = input("Operation:\n1. Encrypt\n2. Decrypt\n> ").strip()

    data = read_hex_64("Input (16 hex characters): ")
    key = read_hex_64("Key   (16 hex characters): ")
    data_bits = hex_to_binary(data)
    key_bits = hex_to_binary(key)

    with quiet():
        if choice == "1":
            keys = key_generation(key_bits)
            if operation == "1":
                result = des_process(data_bits, keys)
            else:
                result = des_process(data_bits, list(reversed(keys)))
        else:
            keys, pc1, pc2 = ke_des_generation(key_bits)
            if operation == "1":
                result = k_des_process(data_bits, keys, pc1, pc2)
            else:
                result = k_des_process(
                    data_bits, list(reversed(keys)), pc1, list(reversed(pc2))
                )

    print(f"Result: {bits_to_hex(result)}")


def run_demo():
    for index, (plaintext, key) in enumerate(DATASETS, start=1):
        plaintext_bits = hex_to_binary(plaintext)
        key_bits = hex_to_binary(key)

        with quiet():
            start = time.perf_counter()
            des_keys = key_generation(key_bits)
            des_key_ms = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            ke_keys, pc1, pc2 = ke_des_generation(key_bits)
            ke_key_ms = (time.perf_counter() - start) * 1000

            des_ciphertext = des_process(plaintext_bits, des_keys)
            des_decrypted = des_process(
                des_ciphertext, list(reversed(des_keys))
            )

            ke_ciphertext = k_des_process(plaintext_bits, ke_keys, pc1, pc2)
            ke_decrypted = k_des_process(
                ke_ciphertext, list(reversed(ke_keys)), pc1, list(reversed(pc2))
            )

        des_decrypted_hex = bits_to_hex(des_decrypted)
        ke_decrypted_hex = bits_to_hex(ke_decrypted)
        des_status = "PASS" if des_decrypted_hex == plaintext else "FAIL"
        ke_status = "PASS" if ke_decrypted_hex == plaintext else "FAIL"

        print(f"=== DATASET {index} ===")
        print(f"Plaintext:  {plaintext}")
        print(f"Key:        {key}")
        print(f"DES    ct:  {bits_to_hex(des_ciphertext)}   -> {des_decrypted_hex}  [{des_status}]")
        print(f"KE-DES ct:  {bits_to_hex(ke_ciphertext)}   -> {ke_decrypted_hex}  [{ke_status}]")
        print(f"Key generation: DES {des_key_ms:.4f} ms | KE-DES {ke_key_ms:.4f} ms")


def main():
    if DEMO:
        run_demo()
        return
    while True:
        print(MENU)
        choice = input("> ").strip()
        if choice in ("1", "2"):
            run_algorithm(choice)
        elif choice == "3":
            run_demo()
        elif choice == "4":
            break
        else:
            print("Error: choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
