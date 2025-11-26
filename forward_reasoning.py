# -------------------------------
# Forward Chaining in Python
# For the KB:
#   Parent(x,y) ← Father(x,y)
#   Grandparent(x,z) ← Parent(x,y) ∧ Parent(y,z)
# Facts:
#   Father(John,Mary)
#   Parent(Mary,Susan)
# Query:
#   Grandparent(John,Susan)
# -------------------------------

from copy import deepcopy

def unify(a, b, subst=None):
    """Unify two literals a and b with a substitution."""
    if subst is None:
        subst = {}

    if a == b:
        return subst

    if isinstance(a, str) and a[0].islower():  # variable in a
        return unify_var(a, b, subst)

    if isinstance(b, str) and b[0].islower():  # variable in b
        return unify_var(b, a, subst)

    if isinstance(a, tuple) and isinstance(b, tuple):
        if a[0] != b[0] or len(a) != len(b):
            return None
        for x, y in zip(a[1:], b[1:]):
            subst = unify(x, y, subst)
            if subst is None:
                return None
        return subst

    return None


def unify_var(var, x, subst):
    """Unify variable with another term."""
    if var in subst:
        return unify(subst[var], x, subst)
    elif x in subst:
        return unify(var, subst[x], subst)
    else:
        subst[var] = x
        return subst


def substitute(term, subst):
    """Apply substitution to a literal."""
    if isinstance(term, str):
        return subst.get(term, term)
    return (term[0],) + tuple(substitute(arg, subst) for arg in term[1:])


# Horn Rule = (head, [premises...])
rules = [
    (("Parent", "x", "y"), [("Father", "x", "y")]),
    (("Grandparent", "x", "z"), [("Parent", "x", "y"), ("Parent", "y", "z")])
]

# Initial facts
facts = [
    ("Father", "John", "Mary"),
    ("Parent", "Mary", "Susan")
]

query = ("Grandparent", "John", "Susan")


def forward_chain(rules, facts, query):
    """Perform forward chaining and return True if query is derived."""
    known = set(facts)

    added_new_fact = True

    while added_new_fact:
        added_new_fact = False

        for head, premises in rules:
            # Try to match all premises
            substitutions = [{}]

            for prem in premises:
                new_subs = []
                for subst in substitutions:
                    prem_inst = substitute(prem, subst)
                    for fact in known:
                        s = unify(prem_inst, fact, deepcopy(subst))
                        if s is not None:
                            new_subs.append(s)
                substitutions = new_subs

            # Add new facts derived from head
            for subst in substitutions:
                new_fact = substitute(head, subst)
                if new_fact not in known:
                    print(f"Derived new fact: {new_fact}")
                    known.add(new_fact)
                    added_new_fact = True

                    if new_fact == query:
                        print("\nQuery proven by forward chaining!")
                        return True

    print("\nQuery NOT provable from given KB.")
    return False


# Run forward chaining
forward_chain(rules, facts, query)
