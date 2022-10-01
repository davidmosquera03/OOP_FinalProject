from typing import List
from tkinter import *
from PIL import ImageTk, Image
from Sprites import *
import time
import abc

class Pregunta:
    def __init__(self,enunciado:str,opciones: List[str], correcta: int, bono: int) -> None:
        self.enunciado = enunciado
        self.opciones = opciones
        if correcta>=len(self.opciones): # validar creación de Pregunta
            raise ValueError("Excede el indice maximo")
        self.correcta = correcta
        self.intentos = 1
        self.bono = bono
        """
        Constructor de clase de Pregunta

        enunciado: pregunta
        opciones: opciones de respuesta
        correcta: indice de respuesta correcta
        intentos: numero de intentos realizados
        bono: recompensa en inteligencia 
        """
        for i in range(len(self.opciones)): # Agregar numeración a pregunta
            self.opciones[i]=" <"+str(i+1)+">"+self.opciones[i]

    def hacer(self,player: Personaje):
        """
        Realizar pregunta a player
        """
        print(self.enunciado)
        print(self.opciones)
        res = input()
        while res!=str(self.correcta+1):
            print("Incorrecto")
            self.intentos+=1
            res = input()
        player.inteligencia+= (self.bono)-(self.intentos-1)
        player.atributos()
        
    def __repr__(self) -> str:
        return f"{self.enunciado}"
        

class Level(abc.ABC):
    def __init__(self, actions : List, info : str, player: Personaje, banco: List[Pregunta]) -> None:
        self.og_actions = actions
        self.actions=["cambiar arma","ver atributos"]
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
        self.actions=["cambiar arma","ver atributos"]
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
        - cambiar arma
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
                self.player.cambiar_arma()
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
    def enter(self,again:bool = False):
        print(self.info)
        op = self.validar()
        if op == self.actions[2]:

            if(not again):
                enemigo1 = Enemigo("Orco",20,30,10,400)
                self.notificar(1,"Una figura se acerca...","¡Un orco hambriento!")
                print("Combate")
                win = self.combate(self.player,enemigo1)

                if win!=self.player.nombre:
                    self.notificar(1,"El orco te arrastra a la oscuridad...","Intenta de nuevo")
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
                self.notificar(0,"Del troll emerge una hacha de fuego","No hay vuelta atrás...")
                win = self.combate(self.player,enemigo2)
                if win!=self.player.nombre:
                    self.notificar(1,"Tu magia es aún muy debil","El troll te aplasta")
                    self.update(self.og_actions)
                    self.enter()
            elif op == self.actions[3]:
                self.notificar(1,"«El mundo de afuera está en caos»",
                              "«Si no conoces lo suficiente no podrás pasar »"
                                ,"« »")
                self.banco[0].hacer(self.player)
                self.exit()
            

    def left_path(self):
        self.update(["revisar cadaver","seguir por tunel","volver"])
        op = self.validar()
        if op==self.actions[2]:
            self.notificar(1,"Encuentras una nota")
            self.exit()
        elif op == self.actions[3]:
            self.exit()
        elif op == self.actions[4]:
            self.update(self.og_actions)
            self.enter(again=True)

    def right_path(self):
        pass

class Room2(Level):
    def enter(self,again:bool = False, exit:bool=False):
        op = self.validar()
        if op == self.actions[2]:
            self.notificar(1,"Una bolsa se encuentra junto al fuego")
            self.left_path()
        elif op == self.actions[3]:
           self.notificar(1,"distingues unos aullidos...","se escuchan pisadas...")

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
        

