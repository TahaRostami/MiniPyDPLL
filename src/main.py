from solver import *
import os

def read_DIMACS(fname):
    nvars,nclauses,cnf=0,0,[]
    with open(fname,'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '').split(' ')
            if line[0]=='p':
                nvars,nclauses=int(line[2]),int(line[3])
            elif line[-1]=='0':
                cnf.append([int(lit) for lit in line if lit!='0'])
    return nvars,nclauses,cnf


if __name__=="__main__":
    base = '../tests/'
    print_found_model = False

    for cnffname in os.listdir(base):
        try:
            nvars, nclauses, cnf = read_DIMACS(base + cnffname)
            mySAT = None
            try:
                msolver = MiniSolver().load_cnf_formula(cnf)
                mySAT = msolver.search()
                print(cnffname, 'SAT' if mySAT else 'UNSAT')
                if print_found_model and mySAT:
                    print(msolver.assigns)
            except Exception as e:
                print(cnffname, e)
        except:
            pass
