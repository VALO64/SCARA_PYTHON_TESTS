import matplotlib.pyplot as plt
import numpy as np
import math as m
from mpl_toolkits import mplot3d

# Hace que la gráfica sea interactiva y poder mover el punto de perspectiva.
# Importante seguir esta secuencia de datos theta, d, alpha y a para las matrices que se van a probar.
th = [ 0,   0,   0,     0]            # Parámetros cinemáticos del robot, las distancias están en cm y los
d  = [50,  20,  30,   -20]            # ángulos en grados
al = [ 0, 180, 180,   180]
a  = [40,  40,   0,     0]
def tranmat(th,d,al,a):
    th = th*m.pi/180  #Las funciones trigonométricas reciben el ángulo en radianes, se realiza una conversión
    al = al*m.pi/180  #Al ser alpha dada en grados tambien se combierte
    T = np.array([[m.cos(th), -m.sin(th)*m.cos(al),  m.sin(th)*m.sin(al),  a*m.cos(th)],
                  [m.sin(th),  m.cos(th)*m.cos(al), -m.cos(th)*m.sin(al),  a*m.sin(th)],
                  [      0,         m.sin(al),              m.cos(al),          d     ],       
                  [      0,              0,                    0,               1     ]])
    return T # Regresa T en este caso seria una traslación
# Impresión de matrices
T10=tranmat(0,50,0,40)
print(T10)
hombro=tranmat(th[0],d[0],al[0],a[0])
codo=np.dot(hombro,tranmat(th[1],d[1],al[1],a[1]))
wrist=np.dot(codo,tranmat(th[2],d[2],al[2],a[2]))
tool=np.dot(wrist,tranmat(th[3],d[3],al[3],a[3]))

f=np.dot(tool,[0, 0, -10, 1])   #     Localizacion de los puntos para dibujar la herramienta
                                #
b=np.dot(tool,[0, -5, -10, 1])  #               b --- c
                                #              |
c=np.dot(tool,[0, -5, 0, 1])    #   wrist ---- f     tool    El ancho de la herremienta y la longitud 
g=np.dot(tool,[0, 5, -10, 1])   #             |             de los dedoses de 10 unidades, por lo que
                                #             g --- e       se recomienda usar d4 > = 15 unidades
e=np.dot(tool,[0, 5, 0, 1])     #
# Comentarios personales de la herramienta, en el comentario de arriba aparecen 5 letras las cuales representan los puntos o 
# estremidades de la herramienta para su posterior graficación
print(tool)
fig = plt.figure(figsize=(8,8))

ax=plt.axes(projection='3d')
ax.set_xlabel('Eje x')
ax.set_ylabel('Eje y')
ax.set_zlabel('Eje z')
 
ax.plot3D([10, 10, -10, -10, 10], [10, -10, -10, 10, 10],[0, 0, 0, 0, 0], color = 'k', lw=2)       
                    # Líneas que representan la placa base del robot

ax.plot3D([0, 0], [0, 0], [0, d[0]], color = 'k', lw=2)   # Línea del torso del robot
ax.plot3D([0, hombro[0,3]], [0, hombro[1,3]], [d[0], hombro[2,3]], color = 'k', lw=2)  

ax.plot3D([hombro[0,3], hombro[0,3]], [hombro[1,3], hombro[1,3]],[hombro[2,3], hombro[2,3]+d[1]], color = 'b', lw=2) # Línea del brazo
ax.plot3D([hombro[0,3], codo[0,3]], [hombro[1,3], codo[1,3]],[hombro[2,3]+d[1], codo[2,3]], color = 'b', lw=2) # del robot
    
    
ax.plot3D([codo[0,3], wrist[0,3]], [codo[1,3], wrist[1,3]],[codo[2,3], wrist[2,3]], color = 'r', lw=2) # Línea del antebrazo
                                                                                          # del robot
# Dibujo de las líneas que forman la herramienta (tenaza)
        
ax.plot3D([wrist[0,3], f[0]], [wrist[1,3], f[1]],[wrist[2,3], f[2]], color = 'k', lw=2)
ax.plot3D([b[0], g[0]], [b[1], g[1]], [b[2], g[2]], color = 'k', lw=2)
ax.plot3D([b[0], c[0]], [b[1], c[1]], [b[2], c[2]], color = 'k', lw=2)
ax.plot3D([e[0], g[0]], [e[1], g[1]], [e[2], g[2]], color = 'b', lw=2)

ax.set_xlim(-80,80) # Dimenciones que queremos en el eje x en este caso de -80 a 80
ax.set_ylim(-80,80) # Dimenciones que queremos en el eje y en este caso de -80 a 80
ax.set_zlim(0,80) #Dimenciones que queremos en el eje z en este caso de 0 a 80 siendo el cero el suelo
ax.set_title('Robot tipo SCARA 4 GdL') # Sirve para mostrar en la parte superior el titulo de la grafica
plt.show()  # Comando para mostrar el plot (Gráfica)
