from Sprites import *
from Levels import *
print("Bienvenido")
time.sleep(0.5)
print("Escribe tu nombre para empezar")
name = input()
while len(name)==0:
    print("El Nombre es necesario")
    name = input()
print("Ahora selecciona una clase")
print("(1) Guerrero (2) Mago (3) Arquero")
op = int(input())
while op<0 or op>3:
    print("Introduce una opción valida")
    op=int(input())
print("A continuación escogeras tu arma inicial")
time.sleep(1)
if op==1:
    p1 = guerrero(name,25,5,20,100) #nombre, fuerza, inteligencia, defensa, vida
elif op==2:
    p1 = mago(name,10,20,15,80) 
else:
    p1 = arquero(name, 15,10,15,90) 
p1.atributos()

a = Pregunta("¿Cuál es un metodo ?",[" vida "," subir_nivel()"," defensa"],1,10) 
b = Pregunta("¿Qué expresión se refiere a la clase madre?",["parent.()","ultra.()","super.()"],2,10)
banco =[a,b]       
c = Pregunta("Cual es mejor para encapsular",["Herencia","Composición"],1,2)
one = Room1(["izquierda","derecha"], "Te encuentras en una cueva oscura, 2 caminos se distinguen", p1, [c])
dos = Room1(["subir", "bajar"], "Shack",p1,banco)
mundo = World()
mundo.add_level(one)
mundo.add_level(dos)
print("Comenzando...")
time.sleep(2)
mundo.start()


