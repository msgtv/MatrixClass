from ast import literal_eval


class MatrixDimensionError(Exception):
    def __init__(self, message='The operation cannot be performed.'):
        self.message = message
        super().__init__(self.message)


class Matrix:

    def __init__(self, matrix=None):
        self.matrix = matrix if matrix else self.create_matrix()
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def __str__(self):
        def is_integer_num(n):
            if isinstance(n, int):
                return True
            if isinstance(n, float):
                return n.is_integer()
            return False
        return '\nThe result is:\n' + '\n'.join([' '.join(map(lambda x: str(int(x)) if is_integer_num(x)
                                            else str(round(x, 3)), row)) for row in self.matrix]) + '\n'

    def __add__(self, other):
        if self.rows == other.rows and self.columns == other.rows:
            result_matrix = [[x + y for x, y in zip(self.matrix[i], other.matrix[i])] for i in range(self.rows)]
            return Matrix(result_matrix)
        else:
            raise MatrixDimensionError

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            matrix = [list(map(lambda x: x * other, i)) for i in self.matrix]
            return Matrix(matrix)
        elif isinstance(other, Matrix):
            if self.columns == other.rows:
                return Matrix(self.multi_matrix(other))
            else:
                raise MatrixDimensionError
        else:
            raise TypeError

    def __rmul__(self, other):
        return self.__mul__(other)

    def multi_matrix(self, other):
        rotate_other = self.transpose_main(other).matrix
        def calculate_cells(row, col):
            return sum([x * y for x, y in zip(row, col)])
        return [[calculate_cells(self.matrix[i], rotate_other[j])
                for j in range(other.columns)] for i in range(self.rows)]

    def transpose_main(self, other=None):
        matrix = self.matrix if other is None else other.matrix
        rotated = [[*r][::1] for r in zip(*matrix)]
        return Matrix(rotated)

    def transpose_side(self):
        return Matrix([[*r][::-1] for r in zip(*self.matrix[::-1])])

    def transpose_hor(self):
        return Matrix(self.matrix[::-1])

    def transpose_vert(self):
        return Matrix(list(map(lambda x: x[::-1], self.matrix)))

    def determinant(self):
        if len(self.matrix) == len(self.matrix[0]):
            return "The result is:\n" + str(self.get_determinant()) + "\n"
        else:
            raise MatrixDimensionError

    def inverse_matrix(self):
        det_matrix = self.get_determinant()
        if det_matrix != 0:
            cofactor_matrix = [[pow(-1, i + j) * self.get_determinant(self.minor(self.matrix, i, j))
                                for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
            transpose_cofactor = [[*r][::1] for r in zip(*cofactor_matrix)]
            return Matrix(transpose_cofactor) * (1 / det_matrix)
        else:
            return "This matrix doesn't have an inverse."

    def get_determinant(self, matrix=None):
        value = 0
        if matrix is None:
            matrix = self.matrix
        if len(matrix) == 1:
            value = matrix[0][0]
        else:
            for num in range(len(matrix)):
                value += pow(-1, num) * matrix[0][num] * self.get_determinant(self.minor(matrix, 0, num))
        return value

    @staticmethod
    def minor(matrix, i, j):
        return [row[:j] + row[j + 1:] for row in matrix[:i] + matrix[i + 1:]]

    @staticmethod
    def create_matrix():
        rows, columns = map(int, input("\nEnter size of matrix: ").split())
        matrix = []
        print("\nEnter matrix:")
        for i in range(rows):
            while True:
                row = input(f"{i + 1} row: ").split()
                if len(row) == columns:
                    row = [literal_eval(i) for i in row]
                    matrix.append(row)
                    break
        return matrix


def menu():
    while True:
        print('1. Add matrices', '2. Multiply matrix by a constant', '3. Multiply matrices',
              '4. Transpose matrix', '5. Calculate a determinant', '6. Inverse matrix', '0. Exit', sep='\n')
        user_input = input('Your choice: ')
        if user_input == '0':
            exit()
        elif user_input == '1':
            print(Matrix() + Matrix())
        elif user_input == '2':
            print(Matrix() * literal_eval(input()))
        elif user_input == '3':
            print(Matrix() * Matrix())
        elif user_input == '4':
            transpose_menu()
        elif user_input == '5':
            print(Matrix().determinant())
        elif user_input == '6':
            print(Matrix().inverse_matrix())


def transpose_menu():
    while True:
        print('\n1. Main diagonal', '2. Side diagonal', '3. Vertical line', '4. Horizontal line', sep='\n')
        user_input = input('Your choice: ')
        if user_input == '1':
            print(Matrix().transpose_main())
        elif user_input == '2':
            print(Matrix().transpose_side())
        elif user_input == '3':
            print(Matrix().transpose_vert())
        elif user_input == '4':
            print(Matrix().transpose_hor())


if __name__ == '__main__':
    menu()
