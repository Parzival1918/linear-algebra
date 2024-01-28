import numpy as np
import sys

def main(mat: np.ndarray):
    print(mat)
    n = np.size(mat, 0) # num of eqns
    m = np.size(mat, 1) - 1 # num of variables
    # Count how many degrees of freedom has every equation in the matrix
    dof = np.zeros(n)
    for i, eqn in enumerate(mat):
        idx = m
        for val in eqn:
            if val != 0:
                break
            idx = idx - 1

        dof[i] = idx

    # For every dof, check that there is only one eqn
    # If there is more than one check that they are consistent and eliminate one of them
    for dof_val in range(1, m+1):
        eqn_idxs = []
        for i in range(len(dof)):
            if dof[i] == dof_val:
                eqn_idxs.append(i)

        if len(eqn_idxs) > 1: # case there is more than one eqn with same num dof
            inconsistent = False
            b_first = mat[eqn_idxs[0]][-1]
            for eqn_idx in eqn_idxs[1:]:
                b_eqn = mat[eqn_idx][-1]
                if b_first == 0 or b_eqn == 0:
                    if b_first != b_eqn:
                        inconsistent = True
                        break
                else:
                    factor = b_first / b_eqn
                    if not np.allclose(mat[eqn_idxs[0]], factor*mat[eqn_idx]):
                        inconsistent = True
                        break

            if inconsistent:
                print("Inconsistent eqns in the system:")
                for eqn_idx in eqn_idxs:
                    print(mat[eqn_idx])
                sys.exit(1)

            # Delete all repetitions except the first one
            mat = np.delete(mat, eqn_idxs[1:], axis=0)
            dof = np.delete(dof, eqn_idxs[1:], axis=0)
        elif len(eqn_idxs) == 0:
            sys.exit("The system of eqns has multiple solutions. This is not yet implemented")

    print(mat) # there are no more than 1 eqn with same dof

    sol = np.zeros(m)
    for dof_val in range(1, m+1):
        eqn_idx = 0
        for i in range(m):
            if dof[i] == dof_val:
                eqn_idx = i
                break

        current = mat[eqn_idx]
        subs_values = np.dot(sol, current[0:-1])
        right_hand = current[-1] - subs_values
        res = right_hand / current[-(1 + dof_val)]

        sol[-(dof_val)] = res

    print("The solution is ", sol)

    # Check the solution
    for eqn in mat:
        res = np.dot(eqn[0:-1], sol)
        is_close = np.allclose(res, eqn[-1])
        print(f"eqn {eqn[0:-1]} has result {res}. Matches initial matrix: {is_close}")

if __name__ == '__main__':
    mat = np.loadtxt('matrix.out')
    main(mat)
