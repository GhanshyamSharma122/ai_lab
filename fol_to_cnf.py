# ---------------------------------------------
# Convert First Order Logic (FOL) formula to CNF
# ---------------------------------------------

import itertools

# --------- FOL Expression Classes ----------

class Var:
    def __init__(self, name):
        self.name = name
    def __str__(self): return self.name

class Const:
    def __init__(self, name):
        self.name = name
    def __str__(self): return self.name

class Func:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __str__(self): return f"{self.name}({','.join(map(str,self.args))})"

class Pred:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __str__(self): return f"{self.name}({','.join(map(str,self.args))})"

# Logical connectives

class Not:
    def __init__(self, op):
        self.op = op
    def __str__(self): return f"¬{self.op}"

class And:
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __str__(self): return f"({self.left} ∧ {self.right})"

class Or:
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __str__(self): return f"({self.left} ∨ {self.right})"

class Impl:
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __str__(self): return f"({self.left} → {self.right})"

class Iff:
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __str__(self): return f"({self.left} ↔ {self.right})"

class ForAll:
    def __init__(self, var, body):
        self.var = var
        self.body = body
    def __str__(self): return f"∀{self.var}.{self.body}"

class Exists:
    def __init__(self, var, body):
        self.var = var
        self.body = body
    def __str__(self): return f"∃{self.var}.{self.body}"


# ------------------- CNF Conversion Steps -------------------

def eliminate_iff(formula):
    """Eliminate ↔ and →."""
    if isinstance(formula, Iff):
        A = eliminate_iff(formula.left)
        B = eliminate_iff(formula.right)
        return And(Impl(A, B), Impl(B, A))

    if isinstance(formula, Impl):
        A = eliminate_iff(formula.left)
        B = eliminate_iff(formula.right)
        return Or(Not(A), B)

    if isinstance(formula, (And, Or)):
        return type(formula)(eliminate_iff(formula.left),
                             eliminate_iff(formula.right))

    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.op))

    if isinstance(formula, (ForAll, Exists)):
        return type(formula)(formula.var, eliminate_iff(formula.body))

    return formula


def push_negation(formula):
    """Push negations inward (De Morgan + quantifier switching)."""
    if isinstance(formula, Not):

        if isinstance(formula.op, Not):
            return push_negation(formula.op.op)

        if isinstance(formula.op, And):
            return Or(push_negation(Not(formula.op.left)),
                      push_negation(Not(formula.op.right)))

        if isinstance(formula.op, Or):
            return And(push_negation(Not(formula.op.left)),
                       push_negation(Not(formula.op.right)))

        if isinstance(formula.op, ForAll):
            return Exists(formula.op.var,
                          push_negation(Not(formula.op.body)))

        if isinstance(formula.op, Exists):
            return ForAll(formula.op.var,
                          push_negation(Not(formula.op.body)))

    if isinstance(formula, (And, Or)):
        return type(formula)(push_negation(formula.left),
                             push_negation(formula.right))

    if isinstance(formula, (ForAll, Exists)):
        return type(formula)(formula.var,
                             push_negation(formula.body))

    return formula


skolem_counter = itertools.count()

def skolemize(formula, vars_in_scope=None):
    """Remove ∃ by replacing with Skolem functions."""
    if vars_in_scope is None:
        vars_in_scope = []

    if isinstance(formula, ForAll):
        return ForAll(formula.var,
                      skolemize(formula.body, vars_in_scope + [formula.var]))

    if isinstance(formula, Exists):
        sk_name = f"Sk{next(skolem_counter)}"
        sk_term = Func(sk_name, vars_in_scope)
        return skolemize(substitute_var(formula.body,
                                        formula.var,
                                        sk_term),
                         vars_in_scope)

    if isinstance(formula, (And, Or)):
        return type(formula)(skolemize(formula.left, vars_in_scope),
                             skolemize(formula.right, vars_in_scope))

    if isinstance(formula, Not):
        return Not(skolemize(formula.op, vars_in_scope))

    return formula


def substitute_var(formula, var, term):
    """Replace variable with term."""
    if isinstance(formula, Var):
        return term if formula.name == var.name else formula

    if isinstance(formula, Pred):
        return Pred(formula.name,
                    [substitute_var(a, var, term) for a in formula.args])

    if isinstance(formula, Func):
        return Func(formula.name,
                    [substitute_var(a, var, term) for a in formula.args])

    if isinstance(formula, (And, Or)):
        return type(formula)(substitute_var(formula.left, var, term),
                             substitute_var(formula.right, var, term))

    if isinstance(formula, Not):
        return Not(substitute_var(formula.op, var, term))

    if isinstance(formula, (ForAll, Exists)):
        return type(formula)(formula.var,
                             substitute_var(formula.body, var, term))

    return formula


def drop_universal(formula):
    """Remove universal quantifiers."""
    if isinstance(formula, ForAll):
        return drop_universal(formula.body)

    if isinstance(formula, (And, Or)):
        return type(formula)(drop_universal(formula.left),
                             drop_universal(formula.right))

    if isinstance(formula, Not):
        return Not(drop_universal(formula.op))

    return formula


def distribute_or(formula):
    """Apply distribution: (A ∨ (B ∧ C)) = (A ∨ B) ∧ (A ∨ C)."""
    if isinstance(formula, Or):

        A = distribute_or(formula.left)
        B = distribute_or(formula.right)

        if isinstance(A, And):
            return And(distribute_or(Or(A.left, B)),
                       distribute_or(Or(A.right, B)))

        if isinstance(B, And):
            return And(distribute_or(Or(A, B.left)),
                       distribute_or(Or(A, B.right)))

        return Or(A, B)

    if isinstance(formula, And):
        return And(distribute_or(formula.left),
                   distribute_or(formula.right))

    return formula


def to_cnf(formula):
    formula = eliminate_iff(formula)
    formula = push_negation(formula)
    formula = skolemize(formula)
    formula = drop_universal(formula)
    formula = distribute_or(formula)
    return formula


# ---------------- Example usage -------------------

# ∀x (P(x) → ∃y Q(x,y))

formula = ForAll(Var("x"),
                 Impl(Pred("P", [Var("x")]),
                      Exists(Var("y"),
                             Pred("Q", [Var("x"), Var("y")]))))

cnf = to_cnf(formula)
print("CNF:", cnf)
