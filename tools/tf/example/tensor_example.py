import tensorflow as tf

# Making a constant tensor A, that does not change
A = tf.constant([[3, 2],
                 [5, 2]])

# Making a Variable tensor VA, which can change. Notice it's .Variable
VA = tf.Variable([[3, 2],
                 [5, 2]])

# Making another tensor B
B = tf.constant([[9, 5],
                 [1, 3]])

AB_concatenated = tf.concat(values=[A, B], axis=1)
print(('Adding B\'s columns to A:\n{0}').format(
    AB_concatenated.numpy()
))

# Concatenate rows
AB_concatenated = tf.concat(values=[A, B], axis=0)
print(('\nAdding B\'s rows to A:\n{0}').format(
    AB_concatenated.numpy()
))

# Making a tensor filled with zeros. shape=[rows, columns]
tensor = tf.zeros(shape=[3, 4], dtype=tf.int32)
print(('Tensor full of zeros as int32, 3 rows and 4 columns:\n{0}').format(
    tensor.numpy()
))

# Making a tensor filled with zeros with data type of float32
tensor = tf.ones(shape=[5, 3], dtype=tf.float32)
print(('\nTensor full of ones as float32, 5 rows and 3 columns:\n{0}').format(
    tensor.numpy()
))

# Making a tensor for reshaping
tensor = tf.constant([[3, 2],
                      [5, 2],
                      [9, 5],
                      [1, 3]])

# Reshaping the tensor into a shape of: shape = [rows, columns]
reshaped_tensor = tf.reshape(tensor = tensor,
                             shape = [1, 8])

print(('Tensor BEFORE reshape:\n{0}').format(
    tensor.numpy()
))
print(('\nTensor AFTER reshape:\n{0}').format(
    reshaped_tensor.numpy()
))

# Making a tensor
tensor = tf.constant([[3.1, 2.8],
                      [5.2, 2.3],
                      [9.7, 5.5],
                      [1.1, 3.4]], 
                      dtype=tf.float32)

tensor_as_int = tf.cast(tensor, tf.int32)

print(('Tensor with floats:\n{0}').format(
    tensor.numpy()
))
print(('\nTensor cast from float to int (just remove the decimal, no rounding):\n{0}').format(
    tensor_as_int.numpy()
))

# Some Matrix A
A = tf.constant([[3, 7],
                 [1, 9]])

A = tf.transpose(A)

print(('The transposed matrix A:\n{0}').format(
    A
))

# Some Matrix A
A = tf.constant([[3, 7],
                 [1, 9]])

# Some vector v
v = tf.constant([[5],
                 [2]])

# Matrix multiplication of A.v^T
Av = tf.matmul(A, v)

print(('Matrix Multiplication of A and v results in a new Tensor:\n{0}').format(
    Av
))

# Element-wise multiplication
Av = tf.multiply(A, v)

print(('Element-wise multiplication of A and v results in a new Tensor:\n{0}').format(
    Av
))

# Some Matrix A
A = tf.constant([[3, 7],
                 [1, 9],
                 [2, 5]])

# Get number of dimensions
rows, columns = A.shape
print(('Get rows and columns in tensor A:\n{0} rows\n{1} columns').format(
    rows, columns
))

# Making identity matrix
A_identity = tf.eye(num_rows = rows,
                    num_columns = columns,
                    dtype = tf.int32)
print(('\nThe identity matrix of A:\n{0}').format(
    A_identity.numpy()
))

# Reusing Matrix A
A = tf.constant([[3, 7],
                 [1, 9]])

# Determinant must be: half, float32, float64, complex64, complex128
# Thus, we cast A to the data type float32
A = tf.dtypes.cast(A, tf.float32)

# Finding the determinant of A
det_A = tf.linalg.det(A)

print(('The determinant of A:\n{0}').format(
    det_A
))

# Defining a 3x3 matrix
A = tf.constant([[32, 83, 5],
                 [17, 23, 10],
                 [75, 39, 52]])

# Defining another 3x3 matrix
B = tf.constant([[28, 57, 20],
                 [91, 10, 95],
                 [37, 13, 45]])

# Finding the dot product
dot_AB = tf.tensordot(a=A, b=B, axes=1).numpy()

print(('Dot product of A.B^T results in a new Tensor:\n{0}').format(
    dot_AB
))

# Which is the same as matrix multiplication in this instance (axes=1)
# Matrix multiplication of A and B
AB = tf.matmul(A, B)

print(('\nMatrix Multiplication of A.B^T results in a new Tensor:\n{0}').format(
    AB
))
