from Sprites import Guerrero,Mago,Arquero
from Levels import Room1,Room2,Room3,World
from Preguntas import banco1,banco2,banco3
import time
import winsound
winsound.PlaySound('img\\intro.wav',winsound.SND_ASYNC) 
time.sleep(2)
print("Bienvenido")
print("La tierra está en caos, el Gran Tirano ha tomado control")
time.sleep(2)
print("Debemos instanciar un Personaje héroe capaz de crear un Dragón para derrotarlo")
print("Dale un nombre para empezar:")
name = input()
while len(name)==0:
    print("nombre es un atributo necesario")
    name = input()

print("Escoge una sub-clase ",name,": Tiene todo lo necesario de un Personaje")
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
    p1 = Guerrero(name,25,5,20,100) 
elif op==2:
    p1 = Mago(name,10,20,15,80) 
else:
    p1 = Arquero(name, 15,10,15,90) 
print("Ha sido creado un Personaje p1 con nombre",p1.nombre,". Mira tus atributos:")
p1.atributos()
time.sleep(1)
print("Desde otras dimensiones conocidas como Modulos estamos importando recursos para el mundo")
one = Room1(["izquierda","derecha"], 
            "Te encuentras en una cueva oscura, 2 caminos se distinguen",
                 p1, banco1)

dos = Room2(["buscar fogata", "seguir adelante"],
            "Te encuentras enfrente de un bosque tupido y oscuro,una fogata se ve en el fondo"
            ,p1,banco2)
tres = Room3(["rodear","saltar"],"El castillo está rodeado por un foso inundado sin puente",p1,banco3)

mundo = World()
mundo.add_level(one)
mundo.add_level(dos)
mundo.add_level(tres)
print("Presiona Enter para Iniciar")
on = input()
while on!="":
    on = input()
print("Comenzando...")
winsound.PlaySound('img\\menu_exit.wav',winsound.SND_ALIAS) 
time.sleep(0.5)
mundo.start()

