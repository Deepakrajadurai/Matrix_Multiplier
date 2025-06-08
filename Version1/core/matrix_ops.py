# import streamlit as st
# import ast
# from utils.validator import is_valid_matrix, can_multiply
#
#
# # Set page configuration
# st.set_page_config(
#     page_title="UMME - Matrix Multiplication Engine",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#
# # Sidebar for instructions
# st.sidebar.title("Instructions")
# st.sidebar.markdown("""
# - Enter matrices A and B below.
# - Ensure compatible dimensions for multiplication.
# - Click "Multiply Matrices" to get the result.
# """)
#
# # Main content
# st.title("Universal Matrix Multiplication Engine")
# st.markdown("Enter two matrices below and see the result!")
#
# with st.form("matrix_form"):
#     st.subheader("Matrix A")
#     matrix_a_input = st.text_area("Enter Matrix A (row-wise, comma-separated):", "[[1, 2], [3, 4]]")
#
#     st.subheader("Matrix B")
#     matrix_b_input = st.text_area("Enter Matrix B:", "[[5, 6], [7, 8]]")
#
#     submitted = st.form_submit_button("Multiply Matrices")
#
# if submitted:
#     try:
#         # Parse inputs
#         A = ast.literal_eval(matrix_a_input.strip())
#         B = ast.literal_eval(matrix_b_input.strip())
#
#         # Validate matrices
#         valid_a, msg_a = is_valid_matrix(A)
#         valid_b, msg_b = is_valid_matrix(B)
#
#         if not valid_a:
#             st.error(f"Matrix A invalid: {msg_a}")
#         elif not valid_b:
#             st.error(f"Matrix B invalid: {msg_b}")
#         else:
#             compatible, msg = can_multiply(A, B)
#             if not compatible:
#                 st.error(msg)
#             else:
#                 # Perform multiplication
#                 result, err = multiply_matrices(A, B)
#                 if err:
#                     st.error(err)
#                 else:
#                     # Display success message
#                     st.success("Multiplication Successful!")
#
#                     # Display result in a clean table format
#                     st.subheader("Result:")
#                     st.table(result)
#
#                     # Optional: Download button for result
#                     st.download_button(
#                         label="Download Result as CSV",
#                         data="\n".join([",".join(map(str, row)) for row in result]),
#                         file_name="result.csv",
#                         mime="text/csv"
#                     )
#     except Exception as e:
#         st.error(f"Invalid input format: {e}")
#
# # Footer
# st.markdown("---")
# st.write("Developed by UMME Team | © 2025")
# core/matrix_ops.py

from typing import List, Union

def multiply_matrices(A: List[List[Union[int, float, str]]], B: List[List[Union[int, float, str]]]) -> List[List[Union[int, float, str]]]:
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

                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    total += a * b
                elif isinstance(a, str) and isinstance(b, str):
                    total = str(total) + (a + b if total != 0 else a + b)
                else:
                    raise TypeError(f"Unsupported operation between '{type(a).__name__}' and '{type(b).__name__}'.")
            result[i][j] = total
    return result