

#multiply 3D vector by 4x4 matrix
def MultiplyMatrixVector(input, matrix):
    output = [0, 0, 0]
    w =0
    output[0] = input[0] * matrix[0][0] + input[1] * matrix[1][0] + input[2] * matrix[2][0] + matrix[3][0]
    output[1] = input[0] * matrix[0][1] + input[1] * matrix[1][1] + input[2] * matrix[2][1] + matrix[3][1]
    output[2] = input[0] * matrix[0][2] + input[1] * matrix[1][2] + input[2] * matrix[2][2] + matrix[3][2]
    w = input[0] * matrix[0][3] + input[1] * matrix[1][3] + input[2] * matrix[2][3] + matrix[3][3]

    if w != 0:
        output[0] /= w
        output[1] /= w
        output[2] /= w
    return(output)
