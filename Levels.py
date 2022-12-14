from typing import List
from Sprites import Arquero, Mago, Personaje,Enemigo,Guerrero,Dragon,ElectricDragon,IceDragon
import time
import abc
from Preguntas import Pregunta
import winsound
from visual import *

class Level(abc.ABC):
    def __init__(self, actions : List[str], info : str, player: Personaje, banco: List[Pregunta]) -> None:
        """
        Constructor de clase Abstracta Level

        + actions: acciones que puede tomar el Personaje
        + info: descripción inicial del escenario
        + next: siguiente nivel
        + player: Personaje en el nivel
        + banco: Banco de preguntas disponibles en el nivel
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
        - usar pocion
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
            self.player.subir_nivel(4)
            self.next.enter()   
        else: 
            pass
    def combate(self,j1: Personaje,j2: Personaje):
        """
        Pelea entre dos personajes

        cada turno se atacan entre si
        acaba cuando la vida de uno es 0
        devuelve el nombre del ganador

        + j1: Personaje del usuario que decide acciones
        + j2: Contrincante del usuario
        """
        wait = 0
        turno = 1
        ganador = None
        print(j1.nombre," vs. ",j2.nombre)
        while j1.esta_vivo and j2.esta_vivo: # Condición de ciclo principal
            print("\nTurno" , turno )
            print(f">>>> Accion de {j1.nombre} : ", sep="")
            print("1 atacar, 2 usar habilidad")
            op = input()
            while op not in ["1","2"]:
                op = input()
            if op =="1":
                j1.atacar(j2)
                winsound.PlaySound('img\\attack.wav',winsound.SND_ALIAS)
                # Sonido básico de ataque
            elif op =="2":
                j1.usar_habilidad(j2)
            time.sleep(wait)
            if(j2.esta_vivo):
                print(f"\n>>>> Accion de {j2.nombre} : ", sep="")
                j2.atacar(j1)
                winsound.PlaySound('img\\attack.wav',winsound.SND_ALIAS)
                turno += 1
                time.sleep(wait)
        if j1.esta_vivo:
            print(f"\nHa ganado: {j1.nombre}")
            ganador = j1.nombre
        elif j2.esta_vivo:
            print(f"\nHa ganado: {j2.nombre} ")
            ganador = j2.nombre
        else:
            print(f"\nEmpate entre: {j1.nombre} y {j2.nombre}")
        return ganador

    def combate2(self, j1: Personaje,j2: Personaje,j3: Personaje):
            """
            Pelea 1 vs 2 personajes

            cada turno se atacan entre si
            acaba cuando la vida de uno es 0
            devuelve el nombre del ganador

            + j1: Personaje del usuario que decide acciones
            + j2 y j3: Contrincantes del usuario
            """

            wait = 0
            turno = 1
            ganador = None
            print(j1.nombre," vs. ",j2.nombre," y ",j3.nombre)

            while j1.esta_vivo and (j2.esta_vivo or j3.esta_vivo):
                print("\nTurno" , turno )
                print(f">>>> Accion de {j1.nombre} : ", sep="")

                if j2.esta_vivo and j3.esta_vivo:
                    print("atacar a (1) "+j2.nombre+" o (2) "+j3.nombre)
                    op = input()
                    while op!="1" and op!="2":
                        op = input("opcion invalida:")
                    if op=="1":
                        target = j2
                    else:
                        target = j3
                elif not j2.esta_vivo:
                    target = j3
                elif not j3.esta_vivo:
                    target = j2
                print("1 atacar, 2 usar habilidad")
                op = input()
                while op not in ["1","2"]:
                    op = input()
                if op =="1":
                    j1.atacar(target)
                    winsound.PlaySound('img\\attack.wav',winsound.SND_ALIAS)
                elif op =="2":
                    j1.usar_habilidad(target)
                time.sleep(wait)
                if(j2.esta_vivo):
                    print(f"\n>>>> Accion de {j2.nombre} : ", sep="")
                    j2.atacar(j1)
                    turno += 1
                    winsound.PlaySound('img\\attack.wav',winsound.SND_ALIAS)
                    time.sleep(wait)
                if(j3.esta_vivo):
                    print(f">>>> Accion de {j3.nombre} : ", sep="")
                    j3.atacar(j1)
                    turno += 1
                    winsound.PlaySound('img\\attack.wav',winsound.SND_ALIAS)
                    time.sleep(wait)
            if j1.esta_vivo:
                print(f"\nHa ganado: {j1.nombre}")
                ganador = j1.nombre
            elif j2.esta_vivo:
                print(f"\nHa ganado: {j2.nombre} ")
                ganador = j2.nombre
            else:
                print(f"\nHa ganado: {j3.nombre} ")
                ganador = j3.nombre

            return ganador 

class Room1(Level):
    """
    Primer nivel
    Cuartos con opción de regresar

    booleanos de actividades
    + defeat: Derrotar orco
    + potion: Hallar poción
    + askedr: Pregunta izquierda
    + askedl: Pregunta derecha
    
    """
    defeat = False # Derrotar orco
    potion = False  # Hallar poción
    askedr = False  # Pregunta izquierda
    askedl = False  # Pregunta derecha
    # Booleanos para registrar avances en nivel
    def enter(self):
        print(self.info)
        foto("img\\Room1.png",3)
        print("Escribe la opción")
        op = self.validar()
        if op == self.actions[2]:

            if(not self.defeat):
                enemigo1 = Enemigo("Orco",40,30,10,400)
                foto("img\\Room2.png")
                self.notificar(0,"Una figura se acerca...","¡Un orco hambriento!")
                print("Combate")
                foto("img\\Room3.png",2)
                vida = self.player.vida
                win = self.combate(self.player,enemigo1)

                if win!=self.player.nombre:
                    ###>>>>
                    self.notificar(1,"El orco te arrastra a la oscuridad...","Intenta de nuevo")
                    self.player.vida=vida
                    self.enter()
                else: 
                    self.defeat = True
                    ###3>>>>>>
                    self.notificar(1,"El orco cae ante tu poder")
                    self.left_path()
            else:
                self.left_path()

        elif op == self.actions[3]:
            foto("img\\Room13.png")
            self.notificar(0.5,"Un troll desarmado resguarda una puerta","No te ha visto aun")
            self.update(["atacar","acercarse"])
            op = self.validar()
            if op==self.actions[2]:
                enemigo2 = Enemigo("Guardian",100,20,80,800)
                foto("img\\Room14.png")
                self.notificar(2,"Del troll emerge un hacha que emana fuego","No hay vuelta atrás...")
                vida = self.player.vida
                win = self.combate(self.player,enemigo2)
                if win!=self.player.nombre:
                    foto("img\\Room16.png")
                    self.notificar(1.5,"Tu magia es aún muy debil","El troll te aplasta")
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.enter()
            elif op == self.actions[3]:

                if not self.askedr:
                    self.askedr = True 
                    foto("img\\Room17.png")
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
        """
        Tras derrotar orco
        """
        foto("img\\Room4.png")
        self.notificar(1,"Una salida de la cueva se ve por el tunel")
        self.update(["revisar cuerpo","seguir","volver", "examinar muros"])
        op = self.validar()

        if op == self.actions[2]: # Revisar cuerpo
            foto("img\\Room5.png")
            self.notificar(0,"Encuentras una nota:",
                            "\"los lobos guardianes estan listos en el bosque\"",
                            "\"el gris es el mas peligroso\"",
                            "\"cuidado al salir\"")
            if not self.potion:
                self.potion = True
                self.player.potions+=1
                foto("img\\Room6.png")
                self.notificar(2,"¡Has hallado una poción!","cantidad actual:",self.player.potions)
            self.left_path()

        elif op == self.actions[3]: # seguir
            self.exit()

        elif op == self.actions[4]: # Volver
            self.update(self.og_actions)
            self.enter()

        elif op == self.actions[5]: # Muros
            foto("img\\Room7.png",6)
            self.notificar(0,"Dibujos grabados en la pared:"
                            ,"de un templo emerge un dragón"
                            ,"Una frase debajo: Ex Nihilo Ecclesia"
                            ,"El dragón incendia y derriba una torre",
                             "notas runas antiguas...")
            if not self.askedl:
                if self.player.inteligencia>=10:
                    foto("img\\Room8.png")
                    self.notificar(0,"tu inteligencia permite leerlas",
                                    "\"Abstractio, Encapsulation, Hereditas, Polymorphismus\"",
                                    "\"Domina los principios y controlarás los objetos\"")
                else:
                    foto("img\\Room9.png")
                    self.notificar(0,"No logras descifrar su significado")
                self.askedl = True
                foto("img\\Room10.png")
                self.notificar(0,"Tu presencia activa las runas...")
                
                foto("img\\Room12.png")
                self.banco[2].hacer(self.player)
            self.left_path()

    def right_path(self,again = False):
        """
        Gruta con lago
        """
        foto("img\\Room20.png")
        self.notificar(0,"Ante ti hay un lago profundo",
                        "otro troll cuida la salida al otro lado")
        self.update(["revisar arriba","saltar"])

        if again:
            self.actions.append("usar cuerda")
        op = self.validar()

        if op ==self.actions[2]: # Revisar arriba
                foto("img\\Room21.png")
                self.notificar(0,"Una cuerda cuelga del techo")
                self.right_path(again=True)

        elif op == self.actions[3]: # Saltar
            
                serpiente = Enemigo("Serpiente marina",50,10,30,400)
                foto("img\\Room23.png")
                vida = self.player.vida
                win = self.combate(self.player,serpiente)
                if win!=self.player.nombre:
                    self.notificar(1,"Tu magia es aún muy debil","La serpiente te aplasta")
                    self.update(self.og_actions)
                    self.player.vida = vida
                    self.right_path()
                else:
                    foto("img\\Room24.png",2)
                    self.notificar(0,"sales mojado y cansado frente al troll")
                    foto("img\\Room25.png",2)
                    self.banco[1].hacer(self.player)
                    

        elif again and op==self.actions[4]: # Usar cuerda
            foto("img\\Room22.png")
            self.notificar(1,"Llegas a salvo junto al troll")
            if isinstance(self.player,Arquero): # Añadir habilidad?
                
                self.notificar(1,"Guardas la cuerda","puede ser util para luego")
                self.player.gancho = True
            self.banco[1].hacer(self.player)

        if op == self.actions[3] or op == self.actions[4]:
            
            self.notificar(1.2,"\"Puedo hablarte del primer secreto\"",
                            "Abstractio:","Oculta los detalles de la implementación",
                            "facilita la interfaz")
            self.exit()
            

class Room2(Level):
    """
    Segundo Nivel
    Camino principal con alternativa
    conectada
    """
    asked = False
    def enter(self,again:bool = False, alt = False):
        if not alt:
            print(self.info)
            video_gif("img\\Room2_1.mp4")
            op = self.validar()
        else:
            op = self.actions[2]

        if op == self.actions[2]: # Buscar fogata
            video_gif("img\\Room2_18.mp4")
            self.notificar(1,"un hombre encapuchado reposa junto al fuego")
            self.notificar(0,"\"te he estado esperando\"",
                    "\"acompañame y te ayudo en tu misión\"")
            self.update(["aceptar","negarse"])
            op = self.validar()
            if op == self.actions[2]: # Aceptar
                video_gif("img\\Room2_23.mp4")
                self.notificar(0,"Con un movimiento rapido desaparecen...",
                                "se encuentran en una guarida")
                self.left_path()
            elif op == self.actions[3]: # Negarse
                video_gif("img\\Room2_19.mp4",6)
                self.notificar(0,"\"De acuerdo, respeto tu decisión y me iré\"",
                                    "\"Sin embargo, cuidate de las gárgolas en camino...\""
                                    ,"poco despues su ida, notas dos figuras en vuelo sobre ti...")
                g = Enemigo("Gárgola dorada",40,20,60,600)
                g2 = Enemigo("Gárgola plateada",30,10,50,400)
                vida = self.player.vida
                video_gif("img\\Room2_20.mp4")
                win = self.combate2(self.player,g,g2)
                if win!=self.player.nombre:
                    self.update(self.og_actions)
                    self.player.vida = vida
                    video_gif("img\\Room2_22.mp4")
                    self.notificar(0,"Te derrotan")
                    self.enter()
                else:
                    self.notificar(1.5,"Una gema es extraida de la Gárgola dorada",
                                "Más Gárgolas se acercan...")
                    if self.player.inteligencia>=15:
                        video_gif("img\\Room2_21.mp4")
                        self.notificar(0,"Detectas la información que almacena",\
                            "¡Rompes la encapsulación de las Gárgolas",
                            "logras reducir a 0 el atributo vida de los enemigos")
                    else:
                        self.notificar(0,"pero no captas su poder",
                                        "te mueves escondiendote de los restantes")
                    self.notificar(0.5,"avanzas adelante","ya se ve el castillo...")
                    self.exit()
                
        elif op == self.actions[3]: # Seguir adelante
            video_gif("img\\Room2_2.mp4")
            self.notificar(0,"distingues unos aullidos...","se escuchan pisadas...")
            vida = self.player.vida
            lobo1 = Enemigo("lobo negro",35,10,20,50)
            lobo2 = Enemigo("lobo gris ",45,10,20,60)
            video_gif("img\\Room2_3.mp4")
            win = self.combate2(self.player,lobo1,lobo2)
            if win!=self.player.nombre:
                video_gif("img\\Room2_5.mp4")
                self.notificar(0,"una jauría de lobos llega para compartir su cena",
                            "intenta de nuevo")
                self.player.vida = vida
                self.enter()
            else:
                video_gif("img\\Room2_4.mp4")
                self.notificar(0,"no puedes evitar correr al oir mas lobos en camino"
                                ,"...")
                video_gif("img\\Room2_6.mp4")
                video_gif("img\\Room2_7.mp4")
                self.notificar(0,"Agotado, llegas a una cabaña y cierras la puerta",
                        "los lobos esperan afuera hambrientos",
                        "hay enormes estantes derribados y una ventana rota")
                self.right_path()
                
    def left_path(self, alt=False):
        """
        Guarida hechicero
        """
        if alt:
            video_gif("img\\Room2_13.mp4")
            self.notificar(0,"Un hechichero te recibe en su guarida",
                             "\"No esperaba encontrarte aun\"","\"Bienvenido\"")
        if self.player.vida<=60:
            self.player.potions+=2
            self.notificar(1.4,"Ante tus heridas recibes 2 pociones",
                        "cantidad actual:",self.player.potions)

        video_gif("img\\Room2_24.mp4")
        self.notificar(0,"\"Tenemos agentes para dejarte entrar\"",
                            "\"Ve al fondo del foso\"",
                        "\"Busca un elfo y da la contraseñas: Invictus\"")
        self.notificar(1,"\"¿Deseas algo más?\"",
                        "\"puedes irte si no deseas  indagar más sobre objetos\"")

        self.update(["irse","indagar"])
        op = self.validar()
        if op == self.actions[2]:
            self.exit()

        elif op == self.actions[3]:
            video_gif("img\\Room2_26.mp4")
            self.notificar(1,"\"Bien\"","\"recibe mi Pregunta...\"")
            self.banco[1].hacer(self.player)
            video_gif("img\\Room2_27.mp4")
            self.notificar(0,"Segundo secreto","Encapsulation",
                    "restringe el acceso directo entre clases")
            self.exit()

    def right_path(self):
        """
        Cabaña alternativa
        """
        self.update(["levantar librero","atacar desde ventana"])
        
        if not self.asked:
            self.notificar(1,"Encuentras una poción en el piso")
            self.player.potions += 1
            self.actions.append("revisar libro")
        op = self.validar()

        if op == self.actions[2]: # Levantar librero
            if isinstance(self.player,Guerrero):
                video_gif("img\\Room2_15.mp4")
                self.notificar(0,"con tu fuerza logras levantar el librero",
                            "descubres una salida subterránea")
                self.exit()
            else:
                self.notificar(1,"tu fuerza es insuficiente")
                self.right_path()

        elif op == self.actions[3]: # Atacar desde ventana
            if isinstance(self.player,Arquero):
                video_gif("img\\Room2_8.mp4")
                self.notificar(0,"los lobos son derribados por tus flechas",
                                "los restantes huyen asustados",
                                "corres a la fogata... ")
                self.enter(alt=True)
                video_gif("img\\Room2_9.mp4")
            else:
                self.notificar(1,"tu rango es insuficiente")
                self.right_path()

        elif not self.asked and op == self.actions[4]:
            video_gif("img\\Room2_10.mp4")
            self.notificar(0.5,"El libro está desgastado pero conserva todavia poder",
                            "\"Encapsulation: Guarda a atributos y métodos en clases\"",
                             "\"limita el accesso de las otras clases a ella\"")
            self.asked = True
            video_gif("img\\Room2_11.mp4")
            self.banco[0].hacer(self.player)
            if isinstance(self.player,Mago):
                video_gif("img\\Room2_12.mp4")
                self.notificar(0,"notas un espejo mágico con tu inteligencia",
                            "entras antes de que los lobos destrozen la puerta...")
                self.left_path(alt=True)
            else:
                self.right_path()

    

class Room3(Level):
    """
    Último nivel

    ice,fire,lighting: booleanos sobre tipo de dragon válido
    
    guia: diccionario de instanciación
    """
    ice = False 
    fire = True
    lighting = False
    guia = {"clase":"class Dragon:",
            "atributos":"def __init__(self,nombre,vida,fuerza):"+
            "\nself.nombre = nombre\nself.vida = vida\nself.fuerza = fuerza",
            "metodos":"def curar(self,cant)...\ndef volar(self,lugar)...\ndef atacar(self)...",
            "usar poción": "aumentas la vida inicial del dragón",
             "ver atributos":"no disponible durante hechizo"}

    def enter(self):
        print(self.info)
        op = self.validar()
        if op == self.actions[2]: # Rodear
            video_gif("img\\Room3_1.mp4")
            self.notificar(0,"una torre se encuentra del otro lado del foso"
                            ,"un guardia se aproxima desde el bosque...")
            self.update(["atacar","saltar"])
            if isinstance(self.player,Arquero) and self.player.gancho:
                self.actions.append("usar gancho")
            op = self.validar()

            if op == self.actions[2]:
                video_gif("img\\Room3_2.mp4")
                guardia = Enemigo("guardia acorazado",45,40,120,350)
                vida = self.player.vida 
                win = self.combate(self.player,guardia)
                if win!=self.player.nombre:
                    video_gif("img\\Room3_3.mp4")
                    self.notificar(0,"El guardia rie","HAHAHA",
                                    "\"Subestimas los Herederos del Tirano\""
                                    "\"Nuestros atributos provienen de él\"")
                    self.player.vida = vida
                    self.enter()
                else:
                    video_gif("img\\Room3_4.mp4")
                    video_gif("img\\Room3_5.mp4")
                    self.notificar(0,"Te pones el uniforme del guardia caido",
                                "saludando ante la puerta te abre un guardia")
                    self.left_path()
            elif op == self.actions[3]: # Saltar
                self.right_path()

            elif op == self.actions[4]:
                video_gif("img\\Room3_6.mp4")
                self.notificar(0,"atas la cuerda a una flecha especial",
                                "la disparas contra la cima de la torre y escalas")
                self.notificar(0,"en la cima descubres un pergamino que brilla",
                        "describe los metodos de un dragón eléctrico")
                self.lighting = True
                video_gif("img\\Room3_7.mp4")
                self.notificar(0,"en el fondo distingues Ex Nihil por su cupula dorada..."
                        "saltas por las murallas hasta llegar")
                self.ex_nihil()
        elif op == self.actions[3]:
            self.right_path()

    def left_path(self): 
        """
        Trama de Inflitración
        Construcción del transfondo del mundo
        
        """
        video_gif("img\\Room3_8.mp4")
        self.notificar(0,"avanzas por las calles","las casas están siendo vaciadas",
        "los habitantes remplazados por gente idéntica al guardia que acabaste...")

        self.update(["investigar","seguir"])
        op = self.validar()
        if op == self.actions[2]:
            video_gif("img\\Room3_9.mp4")
            video_gif("img\\Room3_10.mp4")
            self.notificar(0,"entras a una casa",
            "otro soldado igual te habla mirando un número en tu uniforme",
            "\"Inheritus 154 vuelve a tu puesto\"",
            "\"Suprimir los humanos polimorfos no ha acabado\"",
            "\"Debo recordarte la importancia de la Herencia en nuestro orden...\"")
            video_gif("img\\Room3_11.mp4")
            self.banco[0].hacer(self.player)
            video_gif("img\\Room3_14.mp4")
            self.notificar(0,"\"Nuestra clase madre es Humano, y el tirano su mejor objeto\"",
            "\"piensa en como invocar su herencia en ti\"") 
            video_gif("img\\Room3_13.mp4")
            self.banco[2].hacer(self.player)
            video_gif("img\\Room3_15.mp4")
            self.notificar(1.3,"Aguantas el descontento de su ideología y te retiras",
            "detener el Tirano y sus Herederos salvará la gente")   
        video_gif("img\\Room3_16.mp4")
        self.notificar(0,"Sigues el camino hasta llegar frente a una iglesia",
        "su cupula dorada y el engravado: Ex Nihil Ecclesia")
        self.ex_nihil()

    def right_path(self): 
        """
        Trama en el foso
        """
        self.update(["explorar"])
        op = self.validar()
        video_gif("img\\Room3_17.mp4")
        video_gif("img\\Room3_18.mp4")
        self.notificar(0,"encuentras a un elfo junto a una alcantarilla",
        "detrás cientas de ratas detienen el camino",
                        "\"Dime la clave y sabré que eres el indicado\"")
        txt = input()
        if txt == "Invictus":
            self.ice = True
            video_gif("img\\Room3_19.mp4")
            self.notificar(0.5,"\"Perfecto\"",
                    "\"te has ganado el pergamino de Hielo\"",
                    "acompañame y pasamos las Ratas Eternas")
            video_gif("img\\Room3_20.mp4")
            self.notificar(1,"El elfo lanza un hechizo y congela las ratas...")
            video_gif("img\\Room3_21.mp4")
            video_gif("img\\Room3_22.mp4")
            self.notificar(0,"avanzas hasta el fondo...",
            "encuentras un generador \"Inheritas Ad Infinitum\"",
            "lo destruyes y ves como cada rata desaparece...",
            "subes la escalera y descubres una iglesia...")
            self.ex_nihil()
        else:
            video_gif("img\\Room3_23.mp4")
            self.notificar(0,"\"Aún puedes probarte\"",
                        "\"sobrevive por tu cuenta\"")
            vida = self.player.vida
            video_gif("img\\Room3_24.mp4")
            ratag = Enemigo("rata gigante",40,0,35,700)
            rata = Enemigo("rata poseida",60,1,50,450)
            win = self.combate2(self.player,ratag,rata)
            if win!=self.player.nombre:
                self.player.vida = vida
                self.right_path()
            video_gif("img\\Room3_25.mp4")
            self.notificar(1.5,"Huyes antes de que las demás ratas se acercan",
            "al subir descubres una iglesia de domo dorado")
            self.ex_nihil()
            
        
            
        

    def ex_nihil(self):
        """
        Iglesia de Instanciación
        """
        video_gif("img\\Room3_12.mp4")
        self.banco[1].hacer(self.player)
        video_gif("img\\Room3_26.mp4")
        self.notificar(0,"Te acercas al atrio","¡Es hora de crear un dragón!",
                        "escribe cada parte de la Clase para crearla")
        self.actions =["clase","atributos","metodos"]
        # Sección de demostración de código
        while len(self.actions)!=0:
            print(self.actions)
            op = input()

            if op in self.actions:
                self.notificar(1,self.guia[op])
                # evita condicional usando diccionario
                del self.guia[op]  
                self.actions.remove(op) 
        video_gif("img\\Room3_27.mp4")
        self.notificar(1,"¿Qué nombre le darás?")
        name = input()

        if self.ice or self.lighting:
            # Si posee algun pergamino
            video_gif("img\\Room3_28.mp4")
            self.notificar(0.5,"Ultimos Secretos","Inheritas y Polymorphismus:",
            "Obten los métodos y atributos de una clase madre",
            "Modificalos a tu voluntad")
            video_gif("img\\Room3_29.mp4")
            print("mostrando booleanos de poder válido")
            print(self.ice,self.fire,self.lighting)
            self.update(["hielo","fuego","electricidad"])

            op = self.validar()

            if op == self.actions[2] and self.ice:
                dragon = IceDragon(name,1000,150)

            elif op == self.actions[3]:
                dragon = Dragon(name, 800,100)

            elif op == self.actions[4] and self.lighting:
                dragon = ElectricDragon(name, 900,200)
            else:
                self.notificar(1,"Sin pergamino","creando dragon base")
                dragon = Dragon(name, 800,100)
        else:
            dragon = Dragon(name, 800,100)
        dragon.atributos()
        self.end(dragon)
            
    def end(self,dragon:Dragon):
        """
        Batalla Final
        """
        video_gif("img\\Room3_30.mp4")
        self.notificar(0.5,"montas "+dragon.nombre+" y se elevan",
        "descienden al palacio destruyendo el techo","el trono está vacío",
        "pero un rugido se escucha...")
        winsound.PlaySound('img\\roar.wav',winsound.SND_ALIAS)
        video_gif("img\\Room3_31.mp4") 
        self.notificar(0,"y emerge otro dragón desde el suelo",
            "El gran tirano ha instanciado su propio dragón")
        video_gif("img\\Room3_32.mp4") 
        boss = Dragon("Balerion",1200,120)
        winsound.PlaySound('img\\end.wav',winsound.SND_ASYNC)
        win = self.combate3(dragon,boss)
        if win!=dragon.nombre:
            video_gif("img\\Room3_33.mp4") 
            video_gif("img\\Room3_34.mp4") 
            video_gif("img\\Room3_35.mp4") 
            self.notificar(0.5,"intentas descender de tu dragon muerto...",
            "la rafaga de fuego que te atraviesa no deja ni huesos que enterrar",
            "tú y tu dragón son las primeras muertes de la nueva Era de Terror del Gran Tirano")

        else:
            video_gif("img\\Room3_36.mp4") 
            video_gif("img\\Room3_37.mp4") 
            self.notificar(0,dragon.nombre+" aterriza sobre el cuerpo de "+boss.nombre,
            "el gran Tirano es aplastado",
            "mientras la vida se le escapa, ve como retiras su corona...")
            self.notificar(1,"¿Te coronas como líder?",
            "¿O destituyes la monarquía?","Aprovecha lo que has ganado")

        self.exit()

    def combate3(self,j1: Dragon,j2: Dragon):
        """
        Pelea entre dos dragones

        Cada turno el dragón principal j1
        y el contrincante j2 se atacan hasta
        reducir a 0 la vida del oponente.

        j1 puede realizar un ataque básico,
        reducir la defensa del oponente o 
        cargar un ataque que aumenta su fuerza hasta 
        8 veces
        """
        wait = 2
        turno = 1
        ganador = None
        print(j1.nombre," vs. ",j2.nombre)
        while j1.esta_vivo and j2.esta_vivo:

            print("\nTurno" , turno )
            print(f">>>> Accion de {j1.nombre} : ", sep="")
            print("1 rasguño, 2 incendiar, 3 cargar ataque aereo")
            op = input()
            while op not in ["1","2","3"]:
                op = input()
            if op =="1":
                j1.atacar(j2)
            elif op =="2":
                j1.bajar_defensa(j2)
            elif op == "3":
                j1.cargar_ataque(j2)
            time.sleep(wait)
            if(j2.esta_vivo):
                print(f"\n>>>> Accion de {j2.nombre} : ", sep="")
                j2.atacar(j1)
                turno += 1
                time.sleep(wait)

        if j1.esta_vivo:
            print(f"\nHa ganado: {j1.nombre}")
            ganador = j1.nombre
        elif j2.esta_vivo:
            print(f"\nHa ganado: {j2.nombre} ")
            ganador = j2.nombre
        else:
            print(f"\nEmpate entre: {j1.nombre} y {j2.nombre}")
        return ganador

class World:

    def __init__(self):
        """
        Constructor de Mundo

        + PTR: primer elemento 
        (pointer)
        + ULT: ultimo elemento
        (tail)
        """
        self.PTR= None
        self.ULT = None

    def add_level(self, lvl: Level):
        """
        Añade un nivel a la cola

        + lvl: nivel por añadir
        """
        if self.PTR is None:
            self.PTR = lvl
            self.ULT = lvl
        else:
            self.ULT.next = lvl
            self.ULT = lvl

    def start(self):
        """
        Empieza a recorrer
        los niveles
        """
        L = self.PTR
        L.enter()
        print("Ha terminado el juego")
        # Mensaje final
        

