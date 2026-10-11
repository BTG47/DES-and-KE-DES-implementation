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

def binary_to_hex(binary):
    if len(binary) % 4 != 0:
        raise ValueError("The number of bits must be a multiple of 4")

    hexadecimal = []
    for index in range(0, len(binary), 4):
        bits = binary[index:index + 4]
        if any(bit not in ("0", "1") for bit in bits):
            raise ValueError("The array must contain only strings with bits")
        hexadecimal.append(format(int("".join(bits), 2), "X"))
    return hexadecimal

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

def xor(bits1, bits2):
    result_xor = []
    # Check that bots bits have the same lenght
    if len(bits1) != len(bits2):
        print(f"len bits 1: {len(bits1)}")
        print(f"len bits 2: {len(bits2)}")
        raise ValueError ("The bits have different sizes")
    for element in range(len(bits1)):
        xor = int(bits1[element]) ^ int(bits2[element])
        result_xor.append(str(xor))
    return result_xor
