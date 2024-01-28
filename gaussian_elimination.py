import numpy as np

def main(mat: np.ndarray):
    n = np.size(mat, 0) # number of equations
    m = np.size(mat, 1) - 1 # number of variables
    print(f"num eqns: {n}\nnum variables: {m}")

    used = np.zeros(n, int)
    for check_pos in range(m):
        # Find first equation that has a non-zero factor and that has not been used before
        choice = None
        for i, eqn in enumerate(mat):
            if used[i] == 1: # the eqn has already been used
                continue  
            # Check if value in check_pos is non-zero and those before are
            if eqn[check_pos] != 0:
                non_zero_found = False
                for val in eqn[0:check_pos]:
                    if val != 0:
                        non_zero_found = True

                if not non_zero_found: # the first eqn that stisfies the conditions is found
                    choice = eqn
                    used[i] = 1
                    break

        # Substract the chosen equation from the rest
        for i in range(n):
            if used[i] == 1:
                continue
            if mat[i][check_pos] == 0:
                continue

            # Calculate multiplication factor
            factor = mat[i][check_pos]/choice[check_pos]
            mat[i] = mat[i] - factor*choice

        print(f"Step {check_pos + 1}:")
        print(mat)

    np.savetxt(fname='matrix.out', X=mat, header='Gaussian elimination')

if __name__ == '__main__':
    mat = np.loadtxt('matrix.in')
    main(mat)
