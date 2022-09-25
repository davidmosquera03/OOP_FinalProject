from typing import List
from tkinter import *
from PIL import ImageTk, Image
from Sprites import *

class Pregunta:
    def __init__(self,q:str,opciones: List[str], correcta: int) -> None:
        self.q = q
        self.opciones = opciones
        self.correcta = correcta
    def hacer(self,player: Personaje):
        print(self.q)

class Level:
    def __init__(self, actions : List, info : str, player: Personaje) -> None:
        self.actions = actions
        self.info = info
        self.next = None
    def enter(self):
        pass
    def exit(self):
        pass
class Room1(Level):
    def enter(self):
        onRoom = True
        print(self.info)
        while onRoom:
            print(self.actions)
            print("Decision")
            op = input()
            while op not in self.actions:
                print("decision no válida")
                op = input()
            if op==self.actions[0]:
                print("No hay nada aqui")
            elif op == self.actions[1]:
                print("Mision cumplida")
                onRoom = False

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
