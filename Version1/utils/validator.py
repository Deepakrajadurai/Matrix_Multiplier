# umme/utils/validator.py

def is_valid_matrix(matrix):
    if not isinstance(matrix, list) or not matrix:
        return False, "Input must be a non-empty list of lists."

    num_cols = len(matrix[0])
    for row in matrix:
        if not isinstance(row, list):
            return False, "Each row must be a list."
        if not row:
            return False, "No row can be empty."
        if len(row) != num_cols:
            return False, "All rows must have the same number of columns."
    return True, ""


def can_multiply(A, B):
    _, cols_A = len(A), len(A[0])
    rows_B, _ = len(B), len(B[0])
    if cols_A != rows_B:
        return False, f"Cannot multiply: Inner dimensions mismatch ({cols_A} vs {rows_B})."
    return True, ""