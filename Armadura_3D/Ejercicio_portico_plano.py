import numpy as np
from Nodos import Nodo
from Elementos import Elemento
from Estructura import Estructura

E = 200e6 #kPa

#Columnas
Ac = 0.0088 #m2
Ic = 1.4e-4 #m4


#Vigas
Av = 0.00885 #m2
Iv = 3.5e-4 #m4
Lv = np.sqrt((7.5**2)+(4**2))

w = 24 #kN/m

theta2 = np.arctan2(4,7.5)
theta3 = np.arctan2(-4,7.5)

qx2 = w*np.sin(theta2)
qx3 = w*np.sin(theta3)

qy2 = w*np.cos(theta2)
qy3 = w*np.cos(theta3)

Qf2 = np.array([[qx2*Lv/2],
                [qy2*Lv/2],
                [qy2*(Lv**2)/12],
                [qx2*Lv/2],
                [qy2*Lv/2],
                [-qy2*(Lv**2)/12],
                ])

Qf3 = np.array([[qx3*Lv/2],
                [qy3*Lv/2],
                [qy3*(Lv**2)/12],
                [qx3*Lv/2],
                [qy3*Lv/2],
                [-qy3*(Lv**2)/12],
                ])


modelo = Estructura()

nodos = {
    1: Nodo(1, 0, 0, rx=True, ry=True, rm=True),
    2: Nodo(2, 0, 6),
    3: Nodo(3, 7.5, 10),
    4: Nodo(4, 15, 6),
    5: Nodo(5, 15, 0, rx=True, ry=True, rm=True),
}

for n in nodos.values():
    modelo.ag_nodos(n)

#columnas
Columnas = [
    (1, 1, 2),
    (4, 4, 5)
]

Elemento_columna = []

Elemento_2 = Elemento(2, nodos[2], nodos[3], Av, Iv, E, Qf2)
Elemento_3 = Elemento(3, nodos[3], nodos[4], Av, Iv, E, Qf3)
Elemento_viga = [Elemento_2, Elemento_3]


for eid, ni, nj in Columnas:
    Elemento_columna.append(Elemento(eid, nodos[ni], nodos[nj], Ac, Ic, E)) 

for viga in Elemento_viga:
    modelo.ag_elementos(viga)

for columna in Elemento_columna:
    modelo.ag_elementos(columna)

nodos[2].set_loads(200, 0)

d = modelo.resolver()

modelo.graficar_resultados(tipo='momento', escala=0.004)
modelo.graficar_resultados(tipo='corte', escala=0.005)
modelo.graficar_resultados(tipo='axial', escala=0.005)
modelo.graficar_resultados(tipo='deformada', escala=20)

print("Desplazamientos d: \n", d)

for viga in Elemento_viga:
    viga.imprimir_Qi(d)

for columna in Elemento_columna:
    columna.imprimir_Qi(d) 
