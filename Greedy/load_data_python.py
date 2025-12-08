import re

def load_dat_file(filename):
    """
    Load a .dat file in AMPL-like format and return:
    K, P, R, A, C, N, M
    """

    with open(filename, "r") as f:
        text = f.read()

    text = text.replace("\t", " ")

    # ---------- helper: scalar ----------
    def extract_scalar(name):
        pattern = rf"{name}\s*=\s*(\d+)\s*;"
        match = re.search(pattern, text)
        if not match:
            raise ValueError(f"Scalar {name} not found.")
        return int(match.group(1))

    # ---------- helper: vector ----------
    def extract_vector(name):
        pattern = rf"{name}\s*=\s*\[([^\]]*)\]"
        match = re.search(pattern, text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Vector {name} not found.")
        nums = match.group(1).strip().split()
        return [int(x) for x in nums]

    # ---------- helper: matrix ----------
    def extract_matrix(name):
        # matrix goes from name = [ ... ];
        pattern = rf"{name}\s*=\s*\[([\s\S]*?)\];"
        match = re.search(pattern, text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Matrix {name} not found.")

        body = match.group(1).strip()

        # rows are lines of form [ ... ]
        row_pattern = r"\[([^\]]+)\]"
        row_matches = re.findall(row_pattern, body)

        rows = []
        for row in row_matches:
            nums = row.strip().split()
            rows.append([int(x) for x in nums])

        return rows

    # ---------- extract all fields ----------
    K = extract_scalar("K")
    P = extract_vector("P")
    R = extract_vector("R")
    A = extract_vector("A")
    C = extract_vector("C")
    N = extract_scalar("N")
    M = extract_matrix("M")

    return K, P, R, A, C, N, M
