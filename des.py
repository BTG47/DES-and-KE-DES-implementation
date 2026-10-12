from function_F import function_F
from utilities import xor, permute
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

EXPANSION_PERMUTATION = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

def expansion_des(original_bit_array):
    return permute(original_bit_array, EXPANSION_PERMUTATION)

def expansion_kd(original_bit_array, pc1_kd_selection, pc2_kd_selection):
    return pc1_kd_selection + original_bit_array + pc2_kd_selection

def des_round(ln, rn, key):
    # Apply the expansion of bits
    expanded_rn = expansion_des(rn)
    # Apply the function
    result_of_functionF= function_F(expanded_rn, key)

    # Apply XOR with ln
    xor_with_ln = xor(ln, result_of_functionF)

    # Assign new values
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

def k_des_round(ln, rn, key, round, pc1_kd_selection, pc2_kd_selections):
    # Apply the expansion of bits
    expanded_rn = expansion_kd(rn,pc1_kd_selection, pc2_kd_selections[round])
    # Apply the function
    result_of_functionF= function_F(expanded_rn, key)

    # Apply XOR with ln
    xor_with_ln = xor(ln, result_of_functionF)

    # Assign new values
    ln = rn
    rn = xor_with_ln
    return ln, rn

def k_des_process(data, keys, pc1_kd_selections, pc2_kd_selections):
    # First, we apply the initial permutation
    permuted_data = permute(data, INITIAL_PERMUTATION)

    # Then, the data is split on two parts:
    ln = permuted_data[:32]
    rn = permuted_data[32:]

    # For all keys, the round it's made (16 rounds)
    for index, key in enumerate(keys):
        ln, rn = k_des_round(ln, rn, key, index, pc1_kd_selections, pc2_kd_selections)

    # The values are rearrenged as rn + ln
    swap = rn + ln

    # Finally, the inverse permutation it's applied
    return permute(swap, INVERSE_INITIAL_PERMUTATION)
