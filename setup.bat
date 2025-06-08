@echo off
SETLOCAL

set PROJECT_DIR=Version1

echo [1/6] Creating project structure...
if exist "%PROJECT_DIR%" (
    echo Deleting existing "%PROJECT_DIR%" directory...
    rmdir /s /q "%PROJECT_DIR%"
)

mkdir "%PROJECT_DIR%"
mkdir "%PROJECT_DIR%\core"
mkdir "%PROJECT_DIR%\utils"
mkdir "%PROJECT_DIR%\interfaces"
mkdir "%PROJECT_DIR%\venv"

cd /d "%PROJECT_DIR%"

echo [2/6] Creating virtual environment...
python -m venv venv

echo [3/6] Installing required dependencies into venv...
call venv\Scripts\pip.exe install numpy streamlit

echo [4/6] Writing core/matrix_ops.py...
(
echo from typing import List, Union
echo.
echo def multiply_matrices(A: List[List[Union[int, float, str]]], B: List[List[Union[int, float, str]]]) -> List[List[Union[int, float, str]]]:
echo     rows_A = len(A)
echo     cols_A = len(A[0])
echo     rows_B = len(B)
echo     cols_B = len(B[0])
echo.
echo     result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
echo.
echo     for i in range(rows_A):
echo         for j in range(cols_B):
echo             total = 0
echo             for k in range(cols_A):
echo                 a = A[i][k]
echo                 b = B[k][j]
echo.
echo                 if isinstance(a, (int, float)) and isinstance(b, (int, float)):
echo                     total += a * b
echo                 elif isinstance(a, str) and isinstance(b, str):
echo                     total = str(total) + (a + b if total != 0 else a + b)
echo                 else:
echo                     raise TypeError(f"Unsupported operation between '%%s' and '%%s'." %% (type(a).__name__, type(b).__name__))
echo             result[i][j] = total
echo     return result
) > "core\matrix_ops.py"

echo [5/6] Writing utils/validator.py...
(
echo def is_valid_matrix(matrix):
echo     if not isinstance(matrix, list) or not matrix:
echo         return False, "Input must be a non-empty list."
echo.
echo     num_cols = len(matrix[0])
echo     for row in matrix:
echo         if not isinstance(row, list):
echo             return False, "Each row must be a list."
echo         if len(row) != num_cols:
echo             return False, "All rows must have the same number of columns."
echo         if not row:
echo             return False, "No row can be empty."
echo     return True, ""
echo.
echo def can_multiply(A, B):
echo     _, cols_A = len(A), len(A[0])
echo     rows_B, _ = len(B), len(B[0])
echo     if cols_A != rows_B:
echo         return False, f"Cannot multiply: Inner dimensions mismatch (%%d vs %%d)." %% (cols_A, rows_B)
echo     return True, ""
) > "utils\validator.py"

echo [6/6] Writing interfaces/cli.py...
(
echo import ast
echo.
echo def input_matrix(name):
echo     print(f"Enter Matrix %%s (row-wise, comma-separated values):" %% name)
echo     matrix = []
echo     while True:
echo         line = input("Row (empty to finish): ")
echo         if not line.strip():
echo             break
echo         try:
echo             row = ast.literal_eval(line)
echo             if not isinstance(row, list):
echo                 raise ValueError("Each row must be a list.")
echo             matrix.append(row)
echo         except Exception as e:
echo             print(f"Invalid input: %%s. Please try again." %% e)
echo     return matrix
) > "interfaces\cli.py"

echo Writing main.py...
(
echo from interfaces.cli import input_matrix
echo from utils.validator import is_valid_matrix, can_multiply
echo from core.matrix_ops import multiply_matrices
echo.
echo def pretty_print(matrix):
echo     for row in matrix:
echo         print(row)
echo.
echo def main():
echo     print("=== Universal Matrix Multiplication Engine ===")
echo.
echo     A = input_matrix("A")
echo     B = input_matrix("B")
echo.
echo     valid_a, msg_a = is_valid_matrix(A)
echo     valid_b, msg_b = is_valid_matrix(B)
echo.
echo     if not valid_a:
echo         print(f"Matrix A invalid: %%s" %% msg_a)
echo         return
echo     if not valid_b:
echo         print(f"Matrix B invalid: %%s" %% msg_b)
echo         return
echo.
echo     compatible, msg = can_multiply(A, B)
echo     if not compatible:
echo         print(msg)
echo         return
echo.
echo     try:
echo         result = multiply_matrices(A, B)
echo         print("\\nResult of A × B:")
echo         pretty_print(result)
echo     except Exception as e:
echo         print(f"Error during multiplication: %%s" %% e)
echo.
echo if __name__ == "__main__":
echo     main()
) > "main.py"

echo.
echo Setup complete! Created project in '%cd%' with virtual environment.
echo.
echo To run the CLI version:
echo     cd ..
echo     %cd%\venv\Scripts\python.exe main.py
echo.
echo To run the Streamlit web UI (optional future feature):
echo     %cd%\venv\Scripts\streamlit.exe run ui\web_app.py
echo.
pause