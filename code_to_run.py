from Sprites import *
from Levels import *
from Preguntas import *

print("Bienvenido")
print("La tierra está en caos")
time.sleep(3)
print("Debemos instanciar un Personaje héroe")
print("Escribe tu nombre para empezar")
name = input()
while len(name)==0:
    print("El Nombre es un atributo necesario")
    name = input()

print("Ahora selecciona una sub-clase de Personaje")
print("(1) Guerrero (2) Mago (3) Arquero")
op = input()
n = ["1","2","3"]
while op not in n:
    print("Introduce una opción valida")
    op=input()

print("A continuación escogeras tu arma inicial")
op = int(op)
time.sleep(1)
if op==1:       #nombre, fuerza, inteligencia, defensa, vida
    p1 = guerrero(name,25,5,20,100) 
elif op==2:
    p1 = mago(name,10,20,15,80) 
else:
    p1 = arquero(name, 15,10,15,90) 
print("Ha sido creado, mira tus atributos")
p1.atributos()

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


