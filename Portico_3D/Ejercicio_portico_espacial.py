import numpy as np
from Nodos import Nodo
from Elementos import Elemento
from Estructura import Estructura


E = 200e6 #kPa
G = 80e6 #kPa
A = 13200e-6 #m2
Ix = 400e-6 #m4
Iz = 35e-6 #m4
J = 1.5e-6 #m4

w, L = 50, 6
Qf_viga = np.array([[0],
                    [w*L/2],
                    [0],
                    [0],
                    [0],
                    [w*(L**2)/12],
                    [0],
                    [w*L/2],
                    [0],
                    [0],
                    [0],
                    [-w*(L**2)/12]])

modelo = Estructura()

#Nodos
n1 = Nodo(1, 0, 0, 0, rx=True, ry=True, rz=True, rmx=True, rmy=True, rmz=True)
n2 = Nodo(2, 0, 0, 6, rx=True, ry=True, rz=True, rmx=True, rmy=True, rmz=True)
n3 = Nodo(3, 6, 0, 6, rx=True, ry=True, rz=True, rmx=True, rmy=True, rmz=True)
n4 = Nodo(4, 6, 0, 0, rx=True, ry=True, rz=True, rmx=True, rmy=True, rmz=True)

n5 = Nodo(5, 0, 6, 0)
n6 = Nodo(6, 0, 6, 6)
n7 = Nodo(7, 6, 6, 6)
n8 = Nodo(8, 6, 6, 0)

for n in [n1, n2, n3, n4, n5, n6, n7, n8]:
    modelo.ag_nodos(n)
    
#Cargas nodales
n7.set_loads(fx=200) #kN/m
n8.set_loads(fx=-200) #kN/m


# --- Elementos ---
# Columnas
col1 = Elemento(1, n1, n5, A, Ix, Iz, J, E, G)
col2 = Elemento(2, n2, n6, A, Ix, Iz, J, E, G)
col3 = Elemento(3, n3, n7, A, Ix, Iz, J, E, G)
col4 = Elemento(4, n4, n8, A, Ix, Iz, J, E, G)

# Vigas en dirección X
vig1 = Elemento(5, n5, n8, A, Ix, Iz, J, E, G, Qf=Qf_viga)
vig2 = Elemento(6, n6, n7, A, Ix, Iz, J, E, G, Qf=Qf_viga)  

# Vigas en dirección Z 
vig3 = Elemento(7, n5, n6, A, Ix, Iz, J, E, G, Qf=Qf_viga)
vig4 = Elemento(8, n7, n8, A, Ix, Iz, J, E, G, Qf=Qf_viga)  


for el in [col1, col2, col3, col4, vig1, vig2, vig3, vig4]:
    modelo.ag_elementos(el)
    
d = modelo.resolver()
print(f'\n Desplazamientos nodales en coordenadas globales: \n {d}')

for el in modelo.elementos:
    el.imprimir_Qi(d)
    
modelo.graficar_deformada(escala=5, elev=20, azim=-70)
modelo.graficar_diagrama(tipo = 'momento_z', escala=0.0015)
modelo.graficar_diagrama(tipo = 'momento_y', escala=0.0025)
modelo.graficar_diagrama(tipo = 'axial', escala=0.005)
modelo.graficar_diagrama(tipo = 'corte_y', escala=0.005)