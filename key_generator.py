# This code contains the implementation of both normal key DES generation and
# KE-DES key generation

from utilities import left_shift_array, permute

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

PC1_KD_SELECTION = [
    8, 16, 24, 32, 40, 48, 56, 64
]

PC2_KD_SELECTION = [
    9, 18, 27, 36, 15, 22, 29, 4
]


# Original DES key generator
def key_round(c0, d0, round_number):
    # apply left_schedule
    c0 = left_shift_array(c0, round_number)
    d0 = left_shift_array(d0, round_number)

    combined = c0 + d0

    pc2_permutation = permute(combined, PC_2)
    return pc2_permutation, c0, d0

def key_generation(original_key):
    # Apply transformation PC_1
    # Input: 64 bits, Output: 56 bits
    pc_1 = permute(original_key, PC_1)
    print("PC-1:", "".join(pc_1))

    # Divide each half
    c0 = pc_1[:28]
    d0 = pc_1[28:]

    print("C0:", "".join(c0))
    print("D0:", "".join(d0))

    # Obtain, for each round, its key
    keys = []
    for round in SHIFT_SCHEDULE:
        round_result, c0, d0 = key_round(c0, d0, round)
        keys.append(round_result)

    assert len(keys) == 16
    assert all(len(key) == 48 for key in keys)

    return keys

# KE-DES generation

def ke_key_round(c0, d0, round_number):
    # apply left_schedule (rotations are cumulative across rounds, as in DES)
    c0 = left_shift_array(c0, round_number)
    d0 = left_shift_array(d0, round_number)

    combined = c0 + d0

    pc2_permutation = permute(combined, PC_2)

    # Obtain the bits for the K-D function from the pc2 permutation
    pc2_kd_selection = permute(pc2_permutation, PC2_KD_SELECTION)

    return pc2_permutation, pc2_kd_selection, c0, d0

def odd_even_transformation(input_array):
    result_array = []

    for position in range(1, len(input_array) + 1):
        if position % 2 == 0:
            result_array.append('1')
        else:
            result_array.append('0')

    return result_array

def ke_des_generation(original_key):
    # First, extract the 8 bits used for the K-D function from the original key
    pc1_kd_selection = permute(original_key, PC1_KD_SELECTION)

    # Apply transformation PC_1
    # Input: 64 bits, Output: 56 bits
    pc_1 = permute(original_key, PC_1)
    print("PC-1:", "".join(pc_1))
    print("PC1-KD:", "".join(pc1_kd_selection))

    input_56_bits = pc_1

    # Paper-compatible workaround: the literal Odd/Even split gives D0=0101...,
    # while Table III publishes D0=1010...; rotating the D half once is the
    # minimal transformation that reproduces the paper's D0, K1 and K2.
    odd_even_result = odd_even_transformation(input_56_bits)
    c0 = odd_even_result[:28]
    d0 = left_shift_array(odd_even_result[28:], 1)

    # Obtain, for each round, its key
    keys = []
    pc2_kd_selections = []
    for round in SHIFT_SCHEDULE:
        round_result, pc2_kd_selection, c0, d0 = ke_key_round(c0, d0, round)
        keys.append(round_result)
        pc2_kd_selections.append(pc2_kd_selection)

    assert len(keys) == 16
    assert all(len(key) == 48 for key in keys)

    return keys, pc1_kd_selection, pc2_kd_selections
