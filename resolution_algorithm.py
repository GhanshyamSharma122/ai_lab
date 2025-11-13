from copy import deepcopy

# ---------- Utility Functions ----------

def is_variable(x):
    """Return True if x is a variable (lowercase string)."""
    return isinstance(x, str) and x[0].islower()

def substitute(term, subs):
    """Apply substitution dictionary subs to a term."""
    if isinstance(term, list):
        return [substitute(t, subs) for t in term]
    elif is_variable(term):
        return subs.get(term, term)
    return term

def unify(x, y, subs=None):
    """Unify two terms with substitution subs."""
    if subs is None:
        subs = {}
    if x == y:
        return subs
    elif is_variable(x):
        return unify_var(x, y, subs)
    elif is_variable(y):
        return unify_var(y, x, subs)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            subs = unify(xi, yi, subs)
            if subs is None:
                return None
        return subs
    else:
        return None

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    elif occurs_check(var, x, subs):
        return None
    else:
        new_subs = deepcopy(subs)
        new_subs[var] = x
        return new_subs

def occurs_check(var, x, subs):
    """Avoid recursive references."""
    if var == x:
        return True
    elif is_variable(x) and x in subs:
        return occurs_check(var, subs[x], subs)
    elif isinstance(x, list):
        return any(occurs_check(var, xi, subs) for xi in x)
    return False

# ---------- Resolution ----------

def negate(literal):
    """Negate a literal string."""
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal

def parse_predicate(pred):
    """Split predicate into name and arguments."""
    name, args = pred.split("(")
    args = args.strip(")").split(",")
    return name.strip(), [a.strip() for a in args]

def apply_subs_to_clause(clause, subs):
    """Apply substitution to all literals in a clause."""
    new_clause = []
    for lit in clause:
        neg = lit.startswith("~")
        pred = lit[1:] if neg else lit
        name, args = parse_predicate(pred)
        new_args = substitute(args, subs)
        new_clause.append(("~" if neg else "") + name + "(" + ",".join(new_args) + ")")
    return new_clause

def resolve(ci, cj):
    """Try to resolve two clauses (FOL version)."""
    resolvents = []
    for di in ci:
        for dj in cj:
            neg_di = negate(di)
            name1, args1 = parse_predicate(di if not di.startswith("~") else di[1:])
            name2, args2 = parse_predicate(dj if not dj.startswith("~") else dj[1:])
            if negate(di).split("(")[0] == dj.split("(")[0]:  # same predicate
                subs = unify(args1, args2, {})
                if subs is not None:
                    new_clause = list(set(apply_subs_to_clause(
                        [x for x in ci if x != di] + [x for x in cj if x != dj],
                        subs)))
                    resolvents.append(new_clause)
    return resolvents

def resolution(kb, query):
    """Main resolution refutation loop."""
    clauses = deepcopy(kb)
    clauses.append([negate(query)])
    new = []

    print("Initial clauses:")
    for c in clauses:
        print("  ", c)

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                 for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for r in resolvents:
                if [] in r or r == []:
                    print("\nDerived empty clause: contradiction found!")
                    return True
                if r not in clauses and r not in new:
                    new.append(r)
        if not new:
            print("\nNo new clauses — cannot prove.")
            return False
        clauses.extend(new)
        new.clear()

# ---------- Example KB ----------

KB = [
    ["Man(Marcus)"],
    ["~Man(x)", "Human(x)"],
    ["~Human(x)", "Mortal(x)"]
]

query = "Mortal(Marcus)"

print("Proving:", query)
result = resolution(KB, query)
print("\nResult:", "Proved ✅" if result else "Not provable ❌")
