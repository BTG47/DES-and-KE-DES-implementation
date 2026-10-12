# Shared helpers used across the DES and KE-DES implementation.

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

def left_shift_array(array, num_of_times):
    return array[num_of_times:] + array[:num_of_times]

def permute(bits, table):
    output = []

    # Reorganize the bits according to the positions in the given table
    for position in table:
        output.append(bits[position - 1])
    return output

def xor(bits1, bits2):
    result_xor = []
    # Both operands must have the same length
    if len(bits1) != len(bits2):
        raise ValueError(
            f"The bits have different sizes: {len(bits1)} and {len(bits2)}"
        )
    for element in range(len(bits1)):
        xor = int(bits1[element]) ^ int(bits2[element])
        result_xor.append(str(xor))
    return result_xor
