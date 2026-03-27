from Nodo import Nodo
from Elementos import Elemento
from Estructura import Estructura

armadura = Estructura()

nodos = {
    1: Nodo(1, 0, 0, restriccion_x=True, restriccion_y=True),
    2: Nodo(2, 3, 0),
    3: Nodo(3, 6, 0, restriccion_x=False, restriccion_y=True),
    4: Nodo(4, 9, 0, restriccion_x=False, restriccion_y=True),
    5: Nodo(5, 3, 4),
    6: Nodo(6, 6, 4)
}

for n in nodos.values():
    armadura.ag_nodo(n)
    
E = 200e6 #kPa
A = 0.003 #m2

elementos = [
    (1, 1, 2),
    (2, 2, 3),
    (3, 3, 4),
    (4, 5, 6),
    (5, 5, 2),
    (6, 6, 3),
    (7, 1, 5),
    (8, 5, 3),
    (9, 6, 4)
]

for eid, ni, nj in elementos:
    armadura.ag_elemento(
        Elemento(eid, nodos[ni], nodos[nj], A, E)
    )
    
nodos[2].set_loads(0, -150)
nodos[5].set_loads(50, 0)
nodos[6].set_loads(0, -150)

armadura.solve()
armadura.impimir_desplazamintos()
armadura.impimir_fuerzas_elementos()
armadura.plot_structure(scale=140)

print(armadura.S)