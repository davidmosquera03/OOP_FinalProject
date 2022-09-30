
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
        if correcta>=len(self.opciones):
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
        for i in range(len(self.opciones)):
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
        self.actions = actions
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
    def enter(self):
        print(self.info)
        time.sleep(1.5)
    
    def update(self, new_actions: List[str]):
        """
        Da un nuevo grupo de decisiones posibles
        """
        self.actions=["cambiar arma","ver atributos"]
        for x in new_actions:
            self.actions.append(x)
    def notificar(self, datos: List[str],pause: float):
        """
        Brinda información al usuario con tiempo para leer
        """
        for x in datos:
            print(x)
            time.sleep(pause)
    def validar(self):
        op = input()
        op = op.lower()
        while op not in self.actions:
            print("decision no válida")
            op = input()
        return op

    def combate(self, j1: Personaje,j2: Personaje):
        turno = 1
        ganador = None
        print(j1.nombre," vs. ",j2.nombre)
        while j1.esta_vivo() and j2.esta_vivo():
            print("\nTurno" , turno )
            print(f">>>> Accion de {j1.nombre} : ", sep="")
            j1.atacar(j2)
            time.sleep(2.5)
            if(j2.esta_vivo()):
                print(f">>>> Accion de {j2.nombre} : ", sep="")
                j2.atacar(j1)
                turno += 1
                time.sleep(2.5)
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
        super().enter()
        print("again ",again)
        onRoom  = True
        while onRoom:
            print(self.actions)
            print("Decision")

            op = self.validar()

            if op==self.actions[2]:
                self.notificar(["Una figura en el fondo se acerca","¡Es un orco listo para pelear!"],1.25)
                enemigo1 = Enemigo("Orco",20,30,10,400)
                win = self.combate(self.player,enemigo1)
                if win!=self.player.nombre:
                    self.notificar(["El Orco sonrie victorioso","Has fallado","Intentando de nuevo..."],1.25)
                    self.enter()
                else:
                    self.left_path() 
            elif op==self.actions[0]:
                self.player.cambiar_arma()
            elif op==self.actions[1]:
                self.player.atributos()
            elif op == self.actions[3]:
                self.notificar(["Un troll bloquea una puerta",
                                "Promete dejarte pasar si respondes correctamente",
                                "..."],1.25)
                self.banco[0].hacer(self.player)
                print("Mision cumplida")
                self.player.subir_nivel(5,5,5)
                onRoom = False

    def left_path(self):
        self.update(["revisar cadaver","seguir por tunel","volver"])
        on_left = True
        while on_left:
            print(self.actions)
            op = self.validar()
            if op == self.actions[4]:
                self.enter(again = True)
            elif op== self.actions[2]:
                self.notificar(["Has hallado una poción","y una nota que dice:"],1)
                self.actions.remove("revisar cadaver")
            elif op == self.actions[3]:
                self.banco[1].hacer(self.player)
                on_left = False
        
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
        while(L!=None):
            L.enter()
            L = L.next
        print("Ha ganado el juego")
        

