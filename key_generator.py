from utilities import (transform_64_binary_into_matrix_8x8, 
                       hex_to_binary, 
                       print_matrix,
                       print_array, 
                       transform_matrix_into_array, 
                       left_shift_array)


def shift_values(matrix, value):
    pass

def next_row_column_original(row_original, column_original, isLeftProcedure):
    next_row_original = (row_original -1) % 8 

    if next_row_original== 7: # It ended a cycle on row
        if isLeftProcedure == True:
            next_column_orignal = column_original + 1
        else:
            next_column_orignal = column_original - 1
    else:
        next_column_orignal = column_original
    return next_row_original, next_column_orignal

def next_row_column_output(row_output, column_original):
    next_row_output = row_output
    next_column_output = (column_original + 1) % 7
    if next_column_output == 0:
        next_row_output = row_output + 1
    return next_row_output, next_column_output

def pc_1_key(original_matrix):
    # Input: 64 bits matrix
    # Output: 56 bis matrix
    output_matrix = [[column for column in range(7)] for row in range(8)]

    # First, the four movements of the left
    left_original_row = len(original_matrix) -1
    left_original_column = 0
    output_row = 0
    output_column = 0
    for premutation_step in range(4):
        for move in range(7):
            original_left_value = original_matrix[left_original_column][left_original_row]
            output_matrix[output_row][output_column] = original_left_value
            # Obtain the next moves for traverse the original matrix:
            left_original_row, left_original_column = next_row_column_original(left_original_row, 
                                                                               left_original_column, 
                                                                               True)
            # Obtain the next moves for traverse the output matrix:
            output_row, output_column = next_row_column_output(output_row, output_column)

    # Now, do the same four movements but from the right
    right_original_row = len(original_matrix) -1
    right_original_column = len(original_matrix[0]) -1

    for premutation_step in range(4):
        for move in range(7):
            original_right_value = original_matrix[right_original_column][right_original_row]
            output_matrix[output_row][output_column] = original_right_value
            # Obtain the next moves for traverse the original matrix:
            right_original_row, right_original_column = next_row_column_original(right_original_row, 
                                                                                   right_original_column, 
                                                                                   False)
            # Obtain the next moves for traverse the output matrix:
            output_row, output_column = next_row_column_output(output_row, output_column)
    return output_matrix

def division_c_d(matrix):
    copy_matrix = matrix.copy()
    return copy_matrix[:][:4], copy_matrix[:][4:]  

if __name__ == "__main__":
    test_key_input = '133457799BBCDFF1'
    binary_form = hex_to_binary(test_key_input)
    print(f"Binary: {binary_form}")
    original_key_matrix = transform_64_binary_into_matrix_8x8(binary_form)
    print("Original key matrix")
    print_matrix(original_key_matrix, "Original Key Matrix")
    pc_1_key_matrix = pc_1_key(original_key_matrix)
    print_matrix(pc_1_key_matrix, "PC 1 key matrix")
    c0, d0 = division_c_d(pc_1_key_matrix)
    print_matrix(c0, "C0")
    print_matrix(d0, "D0")
    # For applying the left_shift rotation, it's changed back into an array
    c0 = transform_matrix_into_array(c0)
    d0 = transform_matrix_into_array(d0)
    print("C0 and D0 arrays:")
    print_array(c0)
    print_array(d0)
    # Apply shift
    c0 = left_shift_array(c0, 1)
    d0 = left_shift_array(d0, 1)
    print("Shifted arrays: ")
    print_array(c0)
    print_array(d0)

    pass