from typing import List
from Sprites import Personaje
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

a = Pregunta("¿Cuál es un metodo ?",
                [" vida "," cambiar_arma()"," defensa"],1,10) 

b = Pregunta("¿Qué expresión se refiere a la clase madre?"
                ,["parent.()","ultra.()","super.()"],2,10)   

c = Pregunta("Cual es mejor para encapsular",
            ["Herencia","Composición"],1,2)

banco1 =[a,b]