from Sprites import *
from Levels import *
from Preguntas import *

print("Bienvenido")
print("La tierra está en caos")
time.sleep(1.5)
print("Debemos instanciar un Personaje héroe para salvarla")
print("Dale un nombre para empezar:")
name = input()
while len(name)==0:
    print("nombre es un atributo necesario")
    name = input()

print("Escoge una sub-clase: Tiene todo lo necesario de un Personaje")
print("(1) Guerrero (2) Mago (3) Arquero")
op = input()
n = ["1","2","3"]
while op not in n:
    print("La situación es urgente. Un héroe de la Superclase Personaje no es suficiente")
    op=input()

print("Escoge un arma con que empezar:")
op = int(op)
time.sleep(1)
if op==1:       #nombre, fuerza, inteligencia, defensa, vida
    p1 = guerrero(name,25,5,20,100) 
elif op==2:
    p1 = mago(name,10,20,15,80) 
else:
    p1 = arquero(name, 15,10,15,90) 
print("Ha sido creado un Personaje p1 con nombre",p1.nombre,". Mira tus atributos:")
p1.atributos()
time.sleep(2)
print("Desde otras dimensiones conocidas como Modulos estamos importando para el mundo")
one = Room1(["izquierda","derecha"], 
            "Te encuentras en una cueva oscura, 2 caminos se distinguen",
                 p1, banco1)

dos = Room2(["buscar fogata", "seguir adelante"],
            "Te encuentras enfrente de un bosque tupido y oscuro,una fogata se ve en el fondo"
            ,p1,c)

mundo = World()
mundo.add_level(one)
mundo.add_level(dos)
print("Comenzando...")
time.sleep(0.5)
mundo.start()


