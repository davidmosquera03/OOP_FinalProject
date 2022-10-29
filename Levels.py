from code import interact
from typing import List
from Sprites import Arquero, Mago, Personaje,Enemigo,Guerrero
import time
import abc
from Preguntas import Pregunta

class Level(abc.ABC):
    def __init__(self, actions : List[str], info : str, player: Personaje, banco: List[Pregunta]) -> None:
        """
        Constructor de clase Abstracta Level

        actions: acciones que puede tomar el Personaje
        info: descripción inicial del escenario
        next: siguiente nivel
        player: Personaje en el nivel
        banco: Banco de preguntas disponibles en el nivel
        """
        self.og_actions = actions
        self.actions=["usar poción","ver atributos"]
        self.actions.extend(actions)

        self.info = info
        self.next = None

        self.player = player
        self.banco = banco
       
    @abc.abstractmethod
    def enter(self):
        """
        Eventos iniciales en un nivel
        """
        ...
    

    def update(self, new_actions: List[str]):
        """
        Da un nuevo grupo de decisiones posibles
        """
        self.actions=["usar poción","ver atributos"]
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
        self.player.subir_nivel(2,2,2)
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
    defeat = False # Derrotar orco
    potion = False  # Hallar poción
    askedr = False  # Pregunta izquierda
    askedl = False  # Pregunta derecha
    # Booleanos para registrar avances en nivel
    def enter(self):
        print(self.info)
        op = self.validar()
        if op == self.actions[2]:

            if(not self.defeat):
                enemigo1 = Enemigo("Orco",40,30,10,400)
                self.notificar(0,"Una figura se acerca...","¡Un orco hambriento!")
                print("Combate")
                vida = self.player.vida
                win = self.combate(self.player,enemigo1)

                if win!=self.player.nombre:
                    self.notificar(1,"El orco te arrastra a la oscuridad...","Intenta de nuevo")
                    self.player.vida=vida
                    self.enter()
                else: 
                    self.defeat = True
                    self.notificar(1,"El orco cae ante tu poder")
                    self.left_path()
            else:
                self.left_path()

        elif op == self.actions[3]:

            self.notificar(0,"Un troll desarmado resguarda una puerta","No te ha visto aun")
            self.update(["atacar","acercarse"])
            op = self.validar()
            if op==self.actions[2]:
                enemigo2 = Enemigo("Guardian",100,20,80,800)
                self.notificar(0,"Del troll emerge una hacha que emana fuego","No hay vuelta atrás...")
                vida = self.player.vida
                win = self.combate(self.player,enemigo2)
                if win!=self.player.nombre:
                    self.notificar(0,"Tu magia es aún muy debil","El troll te aplasta")
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.enter()
            elif op == self.actions[3]:

                if not self.askedr:
                    self.askedr = True 
                    self.notificar(0,"«No enfrentes el mundo sin conocimiento»",
                                "«Puedo por medio de una Pregunta aumentar tu inteligencia...»"
                                    ,"«Cuanto antes aciertes, mayor la recompensa»")
                    self.banco[0].hacer(self.player)
                self.update(["seguir","volver"])
                op = self.validar()

                if op==self.actions[2]: # Seguir
                    self.right_path()

                elif op==self.actions[3]: # Volver
                    self.update(self.og_actions)
                    self.enter()

                
    def left_path(self):
        self.notificar(0,"Una salida de la cueva se ve por el tunel")
        self.update(["revisar cuerpo","seguir","volver", "examinar muros"])
        op = self.validar()

        if op == self.actions[2]: # Revisar cuerpo
            self.notificar(0,"Encuentras una nota:",
                            "\"los lobos guardianes estan listos en el bosque\"",
                            "\"el gris es el mas peligroso\"",
                            "\"cuidado al salir\"")
            if not self.potion:
                self.potion = True
                self.player.potions+=1
                self.notificar(0,"¡Has hallado una poción!","cantidad actual:",self.player.potions)
            self.left_path()

        elif op == self.actions[3]: # seguir
            self.exit()

        elif op == self.actions[4]: # Volver
            self.update(self.og_actions)
            self.enter()

        elif op == self.actions[5]: # Muros
            self.notificar(0,"Dibujos grabados en la pared:"
                            ,"de un templo emerge un dragón"
                            ,"Una frase debajo: Ex Nihilo Ecclesia"
                            ,"El dragón incendia y derriba una torre",
                             "notas runas antiguas...")
            if not self.askedl:
                if self.player.inteligencia>=10:
                    self.notificar(0,"tu inteligencia permite leerlas",
                                    "\"Abstractio, Encapsulation, Hereditas, Polymorphismus\"",
                                    "\"Domina los principios y controlarás los objetos\"")
                else:
                    self.notificar(0,"No logras descifrar su significado")
                self.askedl = True
                self.notificar(0,"Tu presencia activa las runas...")
                self.banco[2].hacer(self.player)
            self.left_path()

    def right_path(self,again = False):
        self.notificar(0,"Ante ti hay un lago profundo",
                        "otro troll cuida la salida al otro lado")
        self.update(["revisar arriba","saltar"])

        if again:
            self.actions.append("usar cuerda")
        op = self.validar()

        if op ==self.actions[2]:
                self.notificar(0,"Una cuerda cuelga del techo")
                self.right_path(again=True)

        elif op == self.actions[3]:
                serpiente = Enemigo("Serpiente marina",50,10,30,400)
                vida = self.player.vida
                win = self.combate(self.player,serpiente)
                if win!=self.player.nombre:
                    self.notificar(1,"Tu magia es aún muy debil","El troll te aplasta")
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.right_path()
                else:
                    self.notificar(1,"sales mojado y cansado frente al troll")
                    self.banco[1].hacer(self.player)
                    

        elif again and op==self.actions[4]: # Usar cuerda
            self.notificar(0,"Llegas a salvo junto al troll")
            if isinstance(self.player,Arquero): # Añadir habilidad?
                pass
            self.banco[1].hacer(self.player)

        self.notificar(0,"\"Puedo hablarte del primer secreto\"",
                            "Abstractio:","Oculta los detalles de la implementación",
                            "facilita la interfaz")
        self.exit()
            

class Room2(Level):
    asked = False
    def enter(self,again:bool = False, alt = False):
        if not alt:
            print(self.info)
            time.sleep(1)
            op = self.validar()
        else:
            op = self.actions[2]

        if op == self.actions[2]:
            self.notificar(1,"un hombre encapuchado reposa junto al fuego")
            self.notificar(0,"\"te he estado esperando\"",
                            "\"acompañame y te guio en crear el Dragón y llegar al castillo\"")
            self.update(["aceptar","negarse"])
            op = self.validar()
            if op == self.actions[2]:
                self.notificar(1.75,"Con un movimiento rapido desaparecen...","se encuentran en una guarida")
                self.left_path()
            elif op == self.actions[3]:
                self.notificar(0,"\"De acuerdo, respeto tu decisión y me iré\"",
                                    "\"Sin embargo, cuidate de las gárgolas en camino...\""
                                    ,"poco despues su ida, notas dos figuras en vuelo sobre ti...")
                g = Enemigo("Gárgola dorada",40,20,60,800)
                g2 = Enemigo("Gárgola plateada",30,10,50,700)
                vida = self.player.vida
                win = self.combate2(self.player,g,g2)
                if win!=self.player.nombre:
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.notificar(0,"Te derrotan")
                    self.enter()
                else:
                    self.notificar(0,"Una gema es extraida de la Gárgola dorada","Más Gárgolas se acercan...")
                    if self.player.inteligencia>=15:
                        self.notificar(0,"Detecas la información que almacena",\
                                        "¡Rompes la encapsulación de las Gárgolas",
                                       "logras reducir a 0 el atributo vida de los enemigos restantes sin combate")
                    else:
                        self.notificar(1,"pero no captas su poder",
                                        "te mueves escondiendote de los restantes")
                    self.notificar(0,"avanzas adelante","ya se ve el castillo...")
                    self.exit()
                
        elif op == self.actions[3]:
            self.notificar(1,"distingues unos aullidos...","se escuchan pisadas...")
            vida = self.player.vida
            lobo1 = Enemigo("lobo negro",35,10,20,50)
            lobo2 = Enemigo("lobo gris ",45,10,20,60)
            win = self.combate2(self.player,lobo1,lobo2)
            if win!=self.player.nombre:
                self.notificar(1,"una jauría de lobos llega para compartir su cena","intenta de nuevo")
                self.player.vida = vida
                self.enter()
            else:
                self.notificar(1,"no puedes evitar correr al oir mas lobos en camino"
                                ,"...")
                self.notificar(0,"Agotado, llegas a una cabaña y cierras la puerta",
                        "los lobos esperan afuera hambrientos",
                        "hay enormes estantes derribados y una ventana rota")
                self.right_path()
                
    def left_path(self, alt=False):
        if alt:
            self.notificar(0,"Un hechichero te recibe en su guarida",
                             "\"No esperaba encontrarte aun\"","\"Bienvenido\"")
        if self.player.vida<=50:
            self.player.potions+=2
            self.notificar(0,"Ante tus heridas recibes 2 pociones","cantidad actual:",self.player.potions)


        self.notificar(0,"\"Tenemos agentes para dejarte entrar\"","\"Ve al fondo del foso\"",
                        "\"Busca un elfo y da la contraseñas: Invicta\"")
        self.banco[1].hacer(self.player)
        self.notificar(0,"")
        self.exit()

    def right_path(self):
        self.update(["levantar librero","atacar desde ventana"])

        if not self.asked:
            self.actions.append("revisar libro")
        op = self.validar()

        if op == self.actions[2]: # Levantar librero
            if isinstance(self.player,Guerrero):
                self.notificar(1,"con tu fuerza logras levantar el librero",
                            "descubres una salida subterránea")
                self.exit()
            else:
                self.notificar(1,"tu fuerza es insuficiente")
                self.right_path()

        elif op == self.actions[3]: # Atacar desde ventana
            if isinstance(self.player,Arquero):
                self.notificar(1,"los lobos son derribados por tus flechas",
                                "los restantes huyen asustados",
                                "corres a la fogata... ")
                self.enter(alt=True)
            else:
                self.notificar(1,"tu rango es insuficiente")
                self.right_path()

        elif not self.asked and op == self.actions[4]:
            self.notificar(0,"El libro está desgastado pero conserva todavia poder",
                            "\"Encapsulation: Guarda a atributos y métodos en clases\"",
                             "\"limita el accesso de las otras clases a ella\"")
            self.asked = True
            self.banco[0].hacer(self.player)
            if isinstance(self.player,Mago):
                self.notificar(2,"notas un espejo mágico con tu inteligencia",
                                "entras antes de que los lobos destrozen la puerta...")
                self.left_path(alt=True)
            else:
                self.right_path()

    def combate2(self, j1: Personaje,j2: Personaje,j3: Personaje):
            """
            Pelea entre dos personajes

            cada turno se atacan entre si
            acaba cuando la vida de uno es 0
            devuelve el nombre del ganador
            """
            wait = 2
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
class Room3(Level):
    def enter(self):
        print(self.info)
        op = self.validar()
        if op == self.actions[2]: # Rodear
            self.notificar(0,"una torre se encuentra del otro lado del foso"
                            ,"un guardia se aproxima desde el bosque...")
        elif op == self.actions[3]: # Saltar
            self.notificar(0,"nadas rapidamente hacia la base del castillo")

        
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
        

