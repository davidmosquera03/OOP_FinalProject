from Sprites import *
from Levels import *

print("Escribe tu nombre")
name = input()
while len(name)==0:
    print("Nombre es necesario")
    name = input()
print("Selecciona una clase")
print("(1) Guerrero (2) Mago (3) Arquero")
op = int(input())
while op<0 or op>3:
    op=int(input())
if op==1:
    p1 = guerrero(name,25,5,20,100)
elif op==2:
    p1 = mago(name,10,20,15,80)
else:
    p1 = arquero(name, 20,10,15,90)
print(p1.atributos())

         
one = Room1(["up","down"], "Castle", p1)
dos = Room1(["west", "south"], "shack",p1)
mundo = World()
mundo.add_level(one)
mundo.add_level(dos)
mundo.start()


