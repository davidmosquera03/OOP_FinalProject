from typing import List
from Sprites import *
import time
import abc
from Preguntas import Pregunta

class Level(abc.ABC):
    def __init__(self, actions : List, info : str, player: Personaje, banco: List[Pregunta]) -> None:
        self.og_actions = actions
        self.actions=["usar pocion","ver atributos"]
        self.actions.extend(actions)

        self.info = info
        self.next = None

        self.player = player
        self.banco = banco
        """
        Constructor de clase Abstracta Level

        actions: acciones que puede tomar el Personaje
        info: descripción inicial del escenario
        next: siguiente nivel
        player: Personaje en el nivel
        banco: Banco de preguntas disponibles en el nivel
        """
    @abc.abstractmethod
    def enter(self):
        ...
    

    def update(self, new_actions: List[str]):
        """
        Da un nuevo grupo de decisiones posibles
        """
        self.actions=["usar pocion","ver atributos"]
        for x in new_actions:
            self.actions.append(x)

    def notificar(self,pause: float, *datos):
        """
        Brinda información al usuario con tiempo para leer
        """
        for x in datos:
            print(x)
            time.sleep(pause)

    def validar(self):
        """
        recibe la decision del jugador
        valida si esta en lista de acciones

        mantiene en ciclo para acciones basicas:
        -usar pocion
        - ver atributos 
        """
        on = True
        while on:
            print(self.actions)
            op = input()
            op = op.lower()
            while op not in self.actions:
                print("decision no válida")
                op = input()
            if op == self.actions[0]:
                self.player.curar()
            elif op == self.actions[1]:
                self.player.atributos()
            else:
                on = False
        return op

    def exit(self):
        """
        Entrar al siguiente nivel en el Mundo
        """
        if(self.next is not None):
            self.next.enter()
        else: 
            pass

    def combate(self, j1: Personaje,j2: Personaje):
        """
        Pelea entre dos personajes

        cada turno se atacan entre si
        acaba cuando la vida de uno es 0
        devuelve el nombre del ganador
        """
        wait = 0
        turno = 1
        ganador = None
        print(j1.nombre," vs. ",j2.nombre)
        while j1.esta_vivo() and j2.esta_vivo():
            print("\nTurno" , turno )
            print(f">>>> Accion de {j1.nombre} : ", sep="")
            j1.atacar(j2)
            time.sleep(wait)
            if(j2.esta_vivo()):
                print(f">>>> Accion de {j2.nombre} : ", sep="")
                j2.atacar(j1)
                turno += 1
                time.sleep(wait)
        if j1.esta_vivo():
            print(f"\nHa ganado: {j1.nombre}")
            ganador = j1.nombre
        elif j2.esta_vivo():
            print(f"\nHa ganado: {j2.nombre} ")
            ganador = j2.nombre
        else:
            print(f"\nEmpate entre: {j1.nombre} y {j2.nombre}")
        return ganador

class Room1(Level):
    def enter(self,again:bool = False, again1:bool=False):
        print(self.info)
        op = self.validar()
        if op == self.actions[2]:

            if(not again):
                enemigo1 = Enemigo("Orco",40,30,10,400)
                self.notificar(1,"Una figura se acerca...","¡Un orco hambriento!")
                print("Combate")
                vida = self.player.vida
                win = self.combate(self.player,enemigo1)

                if win!=self.player.nombre:
                    self.notificar(1,"El orco te arrastra a la oscuridad...","Intenta de nuevo")
                    self.player.vida=vida
                    self.enter()
                else: 
                    self.notificar(1,"El orco cae ante tu poder")
                    self.left_path()
            else:
                self.left_path()

        elif op == self.actions[3]:

            self.notificar(0,"Un troll desarmado resguarda una puerta","No te ha visto aun")
            self.update(["atacar","acercarse con cuidado"])
            op = self.validar()
            if op==self.actions[2]:
                enemigo2 = Enemigo("Guardian",100,20,80,800)
                self.notificar(0,"Del troll emerge una hacha que emana fuego","No hay vuelta atrás...")
                vida = self.player.vida
                win = self.combate(self.player,enemigo2)
                if win!=self.player.nombre:
                    self.notificar(1,"Tu magia es aún muy debil","El troll te aplasta")
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.enter()
            elif op == self.actions[3]:
                if not again1: 
                    self.notificar(1,"«No enfrentes el mundo sin conocimiento»",
                                "«Puedo por medio de una Pregunta aumentar tu inteligencia...»"
                                    ,"«Cuanto antes aciertes, mayor la recompensa»")
                    self.banco[0].hacer(self.player)
                self.update(["seguir adelante","volver"])
                op = self.validar()
                if op==self.actions[2]:
                    self.right_path()
                elif op==self.actions[3]:
                    self.update(self.og_actions)
                    self.enter(again1=True)

                
    def left_path(self):
        self.update(["revisar cuerpo","seguir por tunel","volver"])
        op = self.validar()
        if op==self.actions[2]:
            self.notificar(1,"Encuentras una nota:",
                            "\"los lobos guardianes estan listos en el bosque\"",
                            "\"el gris es el mas peligroso\"",
                            "\"cuidado al salir\"")
            self.left_path()
        elif op == self.actions[3]:
            self.exit()
        elif op == self.actions[4]:
            self.update(self.og_actions)
            self.enter(again=True)

    def right_path(self):
        self.exit()

class Room2(Level):
    def enter(self,again:bool = False, exit:bool=False):
        print(self.info)
        time.sleep(1)
        op = self.validar()
        if op == self.actions[2]:
            self.notificar(1,"Un viejo encapuchado duerme junto al fuego",
                            "una bolsa de viaje reposa a sus pies")
            self.left_path()
        elif op == self.actions[3]:
            self.notificar(1,"distingues unos aullidos...","se escuchan pisadas...")
            vida = self.player.vida
            lobo1 = Enemigo("lobo negro",35,10,20,50)
            lobo2 = Enemigo("lobo gris ",45,10,20,60)
            win = self.combate2(self.player,lobo1,lobo2)
            if win!=self.player.nombre:
                self.notificar("una jauria de lobos llega para compartir su cena","intenta de nuevo")
                self.player.vida = vida
                self.enter()
            else:
                self.notificar(0.5,"no puedes evitar correr al oir mas lobos en camino"
                                ,"...")
                self.right_path()
    def left_path(self):
        self.exit()
    def right_path(self):
        self.exit()


    def combate2(self, j1: Personaje,j2: Personaje,j3: Personaje):
            """
            Pelea entre dos personajes

            cada turno se atacan entre si
            acaba cuando la vida de uno es 0
            devuelve el nombre del ganador
            """
            wait = 0
            turno = 1
            ganador = None
            print(j1.nombre," vs. ",j2.nombre," y ",j3.nombre)

            while j1.esta_vivo() and (j2.esta_vivo() or j3.esta_vivo()):
                print("\nTurno" , turno )
                print(f">>>> Accion de {j1.nombre} : ", sep="")

                if j2.esta_vivo() and j3.esta_vivo():
                    op = input("atacar a (1) "+j2.nombre+" o (2) "+j3.nombre)
                    while op!="1" and op!="2":
                        op = input("opcion invalida:")
                    if op=="1":
                        j1.atacar(j2)
                    else:
                        j1.atacar(j3)
                elif not j2.esta_vivo():
                    j1.atacar(j3)
                elif not j3.esta_vivo():
                    j1.atacar(j2)
                time.sleep(wait)
                if(j2.esta_vivo()):
                    print(f">>>> Accion de {j2.nombre} : ", sep="")
                    j2.atacar(j1)
                    turno += 1
                    time.sleep(wait)
                if(j3.esta_vivo()):
                    print(f">>>> Accion de {j3.nombre} : ", sep="")
                    j3.atacar(j1)
                    turno += 1
                    time.sleep(wait)
            if j1.esta_vivo():
                print(f"\nHa ganado: {j1.nombre}")
                ganador = j1.nombre
            elif j2.esta_vivo():
                print(f"\nHa ganado: {j2.nombre} ")
                ganador = j2.nombre
            else:
                print(f"\nHa ganado: {j3.nombre} ")
                ganador = j3.nombre

            return ganador    


    def left_path(self):
        self.exit()

    def right_path(self):
        self.exit()
        
class World:
    def __init__(self):
        self.PTR= None
        self.ULT = None
    def add_level(self, lvl: Level):
        if self.PTR is None:
            self.PTR = lvl
            self.ULT = lvl
        else:
            self.ULT.next = lvl
            self.ULT = lvl
    def start(self):
        L = self.PTR
        L.enter()
        print("Ha ganado el juego")
        

