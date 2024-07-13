import random
from structs import *

class VarOrder:
    def __init__(self, assigns, activity):
        self.assigns = assigns
        self.activity = activity
        self.heap = Heap(self.var_lt)
        self.random_seed = 91648253

    def var_lt(self, x, y):
        return self.activity[x] > self.activity[y]

    def new_var(self):
        self.heap.set_bounds(len(self.assigns))
        self.heap.insert(len(self.assigns) - 1)

    def update(self, x):
        if self.heap.in_heap(x):
            self.heap.increase(x)

    def undo(self, x):
        if not self.heap.in_heap(x):
            self.heap.insert(x)

    def select(self, random_var_freq=0.0):
        # Random decision
        if random.random() < random_var_freq and not self.heap.empty():
            next_var = random.randint(0, len(self.assigns) - 1)
            if self.assigns[next_var] is None:
                return next_var

        # Activity based decision
        while not self.heap.empty():
            next_var = self.heap.get_min()
            if self.assigns[next_var] is None:
                return next_var

        return None


class MiniSolver:
    def __init__(self):
        self.reset_setup()

    def reset_setup(self):
        self.ok=True
        self.clauses=[]

        self.activity=[]

        self.watches=[]
        self.assigns=[]
        self.trail=[]
        self.trail_lim=[]
        self.reason=[]
        self.level=[]

        self.qhead=0

        self.order=VarOrder(self.assigns,self.activity)

    def index(self,lit):
        return ((abs(lit) - 1) * 2 + (0 if lit > 0 else 1))

    def var(self,lit):
        return abs(lit)-1

    def var_value(self,var):
        return self.assigns[var]

    def lit_value(self,lit):
        v=self.var_value(self.var(lit))
        if (v is not None) and lit<0:
            return 1 - v
        return v

    def nAssigns(self):
        return len(self.trail)
    def nClauses(self):
        return len(self.clauses)

    def nVars(self):
        return len(self.assigns)
    def decisionLevel(self):
        return len(self.trail_lim)

    def shrink(self,lst,nelem):
        for k in range(nelem):
            lst.pop()

    def newVar(self):
        index=self.nVars()
        self.watches.append([])
        self.watches.append([])
        self.reason.append(None)
        self.assigns.append(None)
        self.level.append(-1)
        self.activity.append(0)
        self.order.new_var()
        return index

    def enqueue(self,lit,reason):
        v=self.var(lit)
        if self.assigns[v] is None:
            self.assigns[v]= 1 if lit>0 else 0
            self.level[v]=self.decisionLevel()
            self.reason[v]=reason
            self.trail.append(lit)
            return True
        else:
            return self.lit_value(lit)!=0

    def assume(self,lit):
        self.trail_lim.append(len(self.trail))
        return self.enqueue(lit,None)

    def propagate(self):
        conf=None
        while self.qhead < len(self.trail):
            p = self.trail[self.qhead]
            self.qhead+=1
            ws=self.watches[self.index(p)]

            i,j,end=0,0,len(ws)

            while i != end:
                c = ws[i]
                i += 1
                # Make sure the false literal is data[1]:
                false_lit = -p
                if c[0] == false_lit:
                    c[0], c[1] = c[1], c[0]

                # If 0th watch is true, then clause is already satisfied.
                first = c[0]
                val = self.lit_value(first)
                if val == 1:
                    ws[j] = c
                    j += 1
                else:
                    # Look for new watch:
                    found_watch = False
                    for k in range(2, len(c)):
                        if self.lit_value(c[k]) != 0:
                            c[1], c[k] = c[k], c[1]
                            self.watches[self.index(-c[1])].append(c)
                            found_watch = True
                            break

                    if not found_watch:
                        # Did not find watch -- clause is unit under assignment:
                        ws[j] = c
                        j += 1
                        if not self.enqueue(first, c):
                            if self.decisionLevel() == 0:
                                self.ok = False
                            conf = c
                            self.qhead = len(self.trail)
                            # Copy the remaining watches:
                            while i < end:
                                ws[j] = ws[i]
                                j += 1
                                i += 1

            # Shrink the list to the new size
            self.shrink(ws,i-j)

        return conf

    def cancelUntil(self, level):
        if self.decisionLevel() > level:
            for c in range(len(self.trail) - 1, self.trail_lim[level] - 1, -1):
                x = self.var(self.trail[c])
                self.assigns[x] = None
                self.reason[x] = None
                self.order.undo(x)

            self.shrink(self.trail,len(self.trail) - self.trail_lim[level])
            self.shrink(self.trail_lim,len(self.trail_lim) - level)
            self.qhead = len(self.trail)

    def search(self):
        if self.ok==False:
            return False

        if self.propagate() is not None:
            return False

        next_var = self.order.select()

        if next_var is None:# all variables are assigned but no conflict has been found
            return True

        next_var=next_var+1

        for phase in [1,-1]:
            curr_level=self.decisionLevel()
            self.assume(phase*next_var)
            if self.search():
                return True
            self.cancelUntil(curr_level)

        return False

    def load_cnf_formula(self,cnf):
        self.clauses=cnf
        max_var=max([max([abs(l) for l in clause]) for clause in cnf])
        for _ in range(max_var):
            self.newVar()

        for clause_idx,clause in enumerate(self.clauses):
            if len(clause)==0:
                self.ok=False
                return self
            elif len(clause)==1:
                if self.enqueue(clause[0], clause) == False:
                    self.ok=False
                    return self
            else:
                l1,l2 = clause[0],clause[1]
                self.watches[self.index(-l1)].append(clause)
                self.watches[self.index(-l2)].append(clause)

        return self








