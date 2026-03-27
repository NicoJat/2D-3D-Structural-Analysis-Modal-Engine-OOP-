from Nodos import Nodo
from Elementos import Elemento
from Estructura import Estructura

armadura3D = Estructura()

E = 200e6 #kPa
A = 0.004 #m2

nodos_3d = {
    1: Nodo(1, -4,0,4, restriccion_x=True, restriccion_y=True, restriccion_z=True),
    2: Nodo(2, 4,0,4, restriccion_x=True, restriccion_y=True, restriccion_z=True),
    3: Nodo(3, 4,0,-4, restriccion_x=True, restriccion_y=True, restriccion_z=True),
    4: Nodo(4, -4,0,-4, restriccion_x=True, restriccion_y=True, restriccion_z=True),
    5: Nodo(5, -2,10,2),
    6: Nodo(6, 2,10,2),
    7: Nodo(7, 2,10,-2),
    8: Nodo(8, -2,10,-2)
}

for n in nodos_3d.values():
    armadura3D.ag_nodo(n)
    
elementos_3d = [
    #Diagonales externas
    (1, 1, 5), (2, 2, 6), (3, 7, 3), (4, 4, 8),
    #Diasgonales intermedias
    (5, 1, 6), (6, 7, 2), (7, 8, 3), (8, 4, 5),
    #Elementos tope
    (9, 5, 6), (10, 7, 6), (11, 8, 7), (12, 8, 5),
]

for eid, ni, nj in elementos_3d:
    armadura3D.ag_elemento(Elemento(eid, nodos_3d[ni], nodos_3d[nj], A, E))
    
nodos_3d[5].set_loads(45, -90, 0)
nodos_3d[6].set_loads(0, -90, 0)
nodos_3d[7].set_loads(0, -90, 0)
nodos_3d[8].set_loads(45, -90, 0)

#Resolver
armadura3D.solve()
armadura3D.impimir_desplazamintos()
armadura3D.impimir_fuerzas_elementos()
armadura3D.plot_structure(scale=250, elev=-10, azim=250)