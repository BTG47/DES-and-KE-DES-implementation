from utilities import (transform_64_binary_into_matrix_8x8, 
                       hex_to_binary, 
                       print_matrix,
                       print_array, 
                       transform_matrix_into_array, 
                       left_shift_array,
                       permute)

PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_SCHEDULE = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]

def key_round(c0, d0, round_number):
    # apply left_schedule
    c0 = left_shift_array(c0, round_number)
    d0 = left_shift_array(d0, round_number)

    combined = c0 + d0

    pc2_permutation = permute(combined, PC_2)
    return pc2_permutation, c0, d0

def key_generation(original_key):
    # Applay transformation PC_1
    # Input: 64 bits, Output: 56 bits
    print(original_key)
    pc_1 = permute(original_key, PC_1)

    # DEBUG:
    print("The PC1 transmutation: ")
    print_array(pc_1)

    # Divide each in half
    c0 = pc_1[:28] 
    d0 = pc_1[28:]

    print("C0: ")
    print_array(c0)

    print("D0: ")
    print_array(d0)

    #Obtain for each round, its key
    keys = []
    for round in SHIFT_SCHEDULE:
        round_result, c0, d0 = key_round(c0, d0, round)
        keys.append(round_result)

    assert len(keys) == 16
    assert all(len(key) == 48 for key in keys)

    return keys

if __name__ == "__main__":
    # Obtain the main data:
    test_key_input = '133457799BBCDFF1'
    binary_form = hex_to_binary(test_key_input)
    print(f"Binary: {binary_form}")
    original_key_matrix = transform_64_binary_into_matrix_8x8(binary_form)
    print("Original key matrix")
    print_matrix(original_key_matrix, "Original Key Matrix")

    print("Doing key generation ....")
    keys = key_generation(binary_form)
    print("First key:")
    print_array(keys[0])

    print("Total keys:", len(keys))
    print("K1:")
    print_array(keys[0])

    print("K16:")
    print_array(keys[15])