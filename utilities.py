# Code that will be used along the full developmente of the Key-DES
# Some of this utilies includes: 

def print_matrix(matrix, description):
    print(f"Matrix: {description}")
    for row in matrix:
        for value in row:
            print(value, end="")
        print("")

def print_array(array):
    for element in array:
        print(element, end="")
    print("")

def hex_to_decimal(hex):
    return int(hex, 16)

def decimal_to_binary(dec, bit_length=None):
    if bit_length is None:
        bit_length = max(1, dec.bit_length())
    if dec < 0 or dec >= 2 ** bit_length:
        raise ValueError(f"{dec} does not fit in {bit_length} bits")
    return format(dec, f"0{bit_length}b")

def hex_to_binary(hex_value, bit_length=None):
    if bit_length is None:
        bit_length = len(hex_value.removeprefix("0x")) * 4
    decimal = hex_to_decimal(hex_value)
    return decimal_to_binary(decimal, bit_length)

def transform_64_binary_into_matrix_8x8(original_binary):
    new_matrix = [[col for col in range(8)] for row in range (8)]
    column = 0
    row = 0
    for element in original_binary:
        if column == 8:
            row += 1
            column = 0
        
        new_matrix[row][column] = element
        column += 1
    return new_matrix

def transform_matrix_into_array(matrix):
    output_array = []
    for row in matrix:
        for value in row:
            output_array.append(value)
    return output_array

def left_shift_array(array, num_of_times):
    return array[num_of_times:] + array[:num_of_times]


def permute(bits, table):
    output = []

    # Take the already made tables for DES and reorganize the bits according to
    # those positions
    for position in table:
        output.append(bits[position -1])
    return output
