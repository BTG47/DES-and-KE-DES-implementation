from function_F import function_F
from key_generator import key_generation
from utilities import xor, permute, hex_to_binary, print_array, binary_to_hex
INITIAL_PERMUTATION = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

INVERSE_INITIAL_PERMUTATION = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

def des_round(ln, rn, key):
    #Apply the function
    result_of_functionF= function_F(rn, key)

    # Apply XOR with ln
    xor_with_ln = xor(ln, result_of_functionF)

    #Assing new values
    ln = rn
    rn = xor_with_ln
    return ln, rn

def des_process(data, keys):
    # First, we apply the initial permutation
    permuted_data = permute(data, INITIAL_PERMUTATION)

    # Then, the data is split on two parts:
    ln = permuted_data[:32]
    rn = permuted_data[32:]

    # For all keys, the round it's made (16 rounds)
    for key in keys:
        ln, rn = des_round(ln, rn, key)

    # The values are rearrenged as rn + ln
    swap = rn + ln

    # Finally, the inverse permutation it's applied
    return permute(swap, INVERSE_INITIAL_PERMUTATION)

if __name__ == "__main__":
    text_input = "0123456789ABCDEF"
    key = "133457799BBCDFF1"

    binary_text = hex_to_binary(text_input)
    binary_key = hex_to_binary(key)

    # First: obtain the keys:
    keys = key_generation(binary_key)
    print(f"Total lenght of the keys: {len(keys)}")

    # Then, obtain the cipher text applying des
    ciphertext = des_process(
        binary_text,
        keys
    )

    hex_ciphertext = binary_to_hex(ciphertext)
    print("Ciphertext:")
    print_array(hex_ciphertext)

    # To decript the text, the same procedure it's made but using
    # the keys on reverse
    decrypted_text = des_process(
        ciphertext,
        list(reversed(keys))
    )

    hex_decrypted_text = binary_to_hex(decrypted_text)
    print("Decrypted text:")
    print_array(hex_decrypted_text)

