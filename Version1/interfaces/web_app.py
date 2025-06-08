import streamlit as st
import ast


# -----------------------------
# Utility Functions (Embedded)
# -----------------------------

def is_valid_matrix(matrix):
    if not isinstance(matrix, list) or not matrix:
        return False, "Input must be a non-empty list."
    num_cols = len(matrix[0])
    for row in matrix:
        if not isinstance(row, list):
            return False, "Each row must be a list."
        if len(row) != num_cols:
            return False, f"Row '{row}' has inconsistent length."
        if not row:
            return False, "No row can be empty."
    return True, ""


def can_multiply(A, B):
    _, cols_A = len(A), len(A[0])
    rows_B, _ = len(B), len(B[0])
    if cols_A != rows_B:
        return False, f"Inner dimensions mismatch ({cols_A} vs {rows_B})."
    return True, ""


def multiply_matrices(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            total = 0
            for k in range(cols_A):
                a = A[i][k]
                b = B[k][j]

                # Numeric multiplication
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    total += a * b
                # Symbolic string-based multiplication
                elif isinstance(a, str) and isinstance(b, str):
                    if total == 0:
                        total = f"{a}*{b}"
                    else:
                        total = f"{total} + {a}*{b}"
                else:
                    raise TypeError(f"Unsupported operation between '{type(a).__name__}' and '{type(b).__name__}'.")
            result[i][j] = total
    return result


# -----------------------------
# UI Setup
# -----------------------------

st.set_page_config(page_title="UMME - Matrix Multiplication", layout="centered")

st.title("🧮 Universal Matrix Multiplication Engine")
st.markdown("Enter two matrices below and see the result instantly.")

with st.form("matrix_form"):
    col1, col2 = st.columns(2)

    with col1:
        mat_a = st.text_area("Matrix A", value='[[1, 2], [3, 4]]', height=150)

    with col2:
        mat_b = st.text_area("Matrix B", value='[[5, 6], [7, 8]]', height=150)

    submit = st.form_submit_button("Multiply Matrices 🔢")

if submit:
    try:
        A = ast.literal_eval(mat_a.strip())
        B = ast.literal_eval(mat_b.strip())

        valid_a, msg_a = is_valid_matrix(A)
        valid_b, msg_b = is_valid_matrix(B)

        if not valid_a:
            st.error(f"Invalid Matrix A: {msg_a}")
        elif not valid_b:
            st.error(f"Invalid Matrix B: {msg_b}")
        else:
            compatible, msg = can_multiply(A, B)
            if not compatible:
                st.error(msg)
            else:
                result = multiply_matrices(A, B)
                st.success("✅ Multiplication Successful!")

                # Display result as a table
                st.markdown("### Result Matrix:")
                st.table(result)

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.warning("Tip: Make sure the input is correctly formatted like [[1, 2], [3, 4]]")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | UMME v1.0")