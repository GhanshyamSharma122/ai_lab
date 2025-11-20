p=[True]*4+[False]*4
q=[True]*2+[False]*2+[True]*2+[False]*2
r=[True,False,True,False,True,False,True,False]
def imply(a,b):
    if a and not b:
        return False
    return True
def Or(a,b):
    return a or b
def And(a,b,c):
    return a and b and c
q_imply_p=[imply(q[i],p[i]) for i in range(len(p))]
p_implynot_q=[imply(p[i],not q[i]) for i in range(len(p))]
q_or_r=[Or(q[i],r[i]) for i in range(len(p))]
r_imply_p=[imply(r[i],p[i]) for i in range(len(p))]
q_imply_r=[imply(q[i],r[i]) for i in range(len(p))]
kb=[And(q_imply_p[i],p_implynot_q[i],q_or_r[i]) for i in range(len(p))]
kb_reduced=[i for i,j in enumerate(kb) if j]
r_entails=[True for i in kb_reduced if r[i]]
r_imply_p_entails=[True for i in kb_reduced if r_imply_p[i]]
q_imply_r_entails=[True for i in kb_reduced if q_imply_r[i]]
print("q_imply_p")
print(q_imply_p)
print("p_implynot_q")
print(p_implynot_q)
print("q_or_r")
print(q_or_r)
print("r_imply_p")
print(r_imply_p)
print("q_imply_r")
print(q_imply_r)
print("r")
print(r)
print("kb")
print(kb)
print("r entails" if r_entails.count(True)==len(kb_reduced) else "r doesnot entail")
print("r_imply_p_entails" if r_imply_p_entails.count(True)==len(kb_reduced) else "r_imply_p doesnot entail")
print("q_imply_r_entails" if q_imply_r_entails.count(True)==len(kb_reduced) else "q_imply_r doesnot entail")



