import time
import winsound
from random import randint

class Personaje:

    def __init__(self, nombre, fuerza, inteligencia,defensa,vida):
        """
        Constructor Clase Personaje

        + nombre: nombre del Personaje
        + fuerza: fuerza inicial
        + inteligencia: aumenta por Preguntas, revela secretos
        + defensa: reduce daño recibido
        + vida: si llega a 0 muere
        + nivel: inicial es 1, aumenta con niveles
        + potions: permiten aumentar vida en 10 puntos
        """
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida 
        self.nivel = 1 
        self.potions = 2
    
    def atributos(self):
        """
        Muestra atributos
        """
        print(self.nombre, " : " ,)
        print("-Nivel: ",self.nivel)
        print("-Fuerza: ", self.fuerza)
        print("-Inteligencia: ", self.inteligencia)
        print("-Defensa : " , self.defensa)
        print("-Vida: " , self.vida)
     
    def subir_nivel(self,increase:int):
        """
        Aumenta el nivel del Personaje
        """
        self.nivel+=1
        print("Has subido tu personaje al nivel ",self.nivel)
        time.sleep(1)
        self.fuerza +=  increase
        self.inteligencia += increase
        self.defensa += increase
        
    @property
    def esta_vivo(self):
        """
        Valida si su vida es mayor a 0
        """
        return self.vida > 0 
        
    def morir(self):
        """
        reporta la muerte del Personaje
        """
        self.vida = 0
        print(f" El jugador {self.nombre} esta muerto")
        
        
    def daño(self, enemigo):
        """
        Calculador de daño 
        """
        daño = self.fuerza - enemigo.defensa
        if daño<0:
            return 0
        return daño
    
    def atacar(self,enemigo):
        """
        Aplica daño a enemigo
        Reporta 
        """
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
        if enemigo.esta_vivo:
            print(f"la vida de {enemigo.nombre} es {enemigo.vida} ")
        else:
            enemigo.morir()
           
    def curar(self):
        if self.potions>0:
            self.potions-=1
            self.vida+=10
            print("tu vida es ahora ",self.vida)
            print("Pociones restantes: ",self.potions)
        else:
            print("No hay pociones")

    def usar_habilidad(self,enemigo):
        pass
##PARTE DE HERENCIA
class Guerrero(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.espada = 1
        self.cambiar_arma()

    def cambiar_arma(self):
        while True: 
            try:
                opcion = int(input("Elige un arma: (1) Acero Valkyria, espada +8 defensa +5."+ 
                                        "(2) Matadragones, espada +10 \n"))
                if opcion == 1:
                    self.espada +=8
                    self.defensa+=5
                    break
                elif opcion ==2:
                    self.espada+=10
                    break
                else:
                    print("Numero no valido")
            except:
                print("Se requiere un numero")

    def subir_nivel(self, increase: int):
        super().subir_nivel(increase)
        self.espada += 2
        self.atributos()
        
    def atributos(self):
        super().atributos()
        print(f"-Espada: {self.espada}")
        
    def daño(self,enemigo):
        daño = self.fuerza*self.espada - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0

    def usar_habilidad(self,enemigo):
        """
        Reducir daño
        """
        winsound.PlaySound('img\\warrior.wav',winsound.SND_ALIAS)
        enemigo.fuerza -= 10
        print(f"{self.nombre}  {enemigo.nombre}")
        print(f"{self.nombre} ha bajado en 10 puntos la fuerza a {enemigo.nombre}")
        print(f"su fuerza es ahora {enemigo.fuerza}")

class Mago(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)  
        self.libro = 1
        self.cambiar_arma()    
    
    def cambiar_arma(self):
        while True: 
            try:
                opcion = int(input("Elige un arma: (1) Cetro Vampirico, libro +14."+
                            " (2) Cetro de Valhala , libro +10 vida+5\n"))
                if opcion == 1:
                    self.libro+=14
                    break
                elif opcion ==2:
                    self.libro =10
                    self.vida+=5
                    break
                else:
                    print("Numero no valido")
            except:
                print("Se requiere un numero")  
        
    def atributos(self):
        super().atributos()  
        print(f"-Libro: {self.libro}")

    def subir_nivel(self, increase: int):
        super().subir_nivel(increase)
        self.libro += 2
        self.atributos()

    def daño(self, enemigo):
        daño = self.inteligencia*self.libro - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0

    def usar_habilidad(self,enemigo):
        """
        Baja la defensa en 20 puntos
        """
        winsound.PlaySound('img\\magic.wav',winsound.SND_ALIAS)
        enemigo.defensa -= 20
        print(f"{self.nombre} lanza un hechizo sobre {enemigo.nombre}")
        print(f"{self.nombre} ha bajado en 20 puntos la defensa a {enemigo.nombre}")
        print(f"su defensa es ahora {enemigo.defensa}")

class Arquero(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.critico = 1
        self.gancho = False
        self.cambiar_arma()
    
    def cambiar_arma(self):
         while True: 
            try:
                opcion = int(input("Elige un arma: (1) Arco Ionico, critico +8 vida +5."+
                                             "(2) MataKrakens , critico +12\n "))
                if opcion == 1:
                    self.critico += 8
                    self.vida+=5
                    break
                elif opcion ==2:
                    self.critico += 12
                    break
                else:
                    print("Numero no valido")
            except:
                print("Se requiere un numero")  
    
    def atributos(self):
        super().atributos()
        print(f"-Critico: {self.critico}")

    def subir_nivel(self, increase: int):
        super().subir_nivel(increase)
        self.critico += 5
        self.atributos()

    def usar_habilidad(self,enemigo):
        """
        realiza 20 puntos de daño 
        que ignoran armadura y aumenta 
        probabilidad de fallar
        """
        winsound.PlaySound('img\\arrow.wav',winsound.SND_ALIAS)
        enemigo.vida -= self.critico
        if isinstance(enemigo,Enemigo):
            enemigo.fail+= self.critico
        print(f"{self.nombre} dispara una flecha de fuego a {enemigo.nombre}")
        print(f"{self.nombre} ha reducido en {self.critico} puntos la vida de {enemigo.nombre}")
        print(f"{enemigo.nombre} empieza a enojarse...")

    def atacar (self,enemigo):
        """
        Aplica daño a enemigo
        con probabilidad de daño critico
        de acuerdo a este atributo
        Reporta 
        """
        select = randint(0,100) # Numero de 1 a 100
        daño = self.daño(enemigo) 
        if select<=self.critico: 
            # Si es < o = está dentro rango de crítico (probabilidad)
            print("¡Daño Crítico!")
            daño *= 2
        enemigo.vida = enemigo.vida - daño
        print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
        if enemigo.esta_vivo:
            print(f"la vida de {enemigo.nombre} es {enemigo.vida} ")
        else:
            enemigo.morir()
            
    def daño(self, enemigo):
        daño = self.fuerza * self.critico - enemigo.defensa 
        if daño>0:
            return daño
        else: 
            return 0

class Enemigo(Personaje):
    fail = 5 # Probabilidad de fallar ataque

    def atacar (self,enemigo):
        """
        ataca a enemigo
        calcula antes si falla o no el ataques
        """
        select = randint(0,100) # Numero de 1 a 100
        daño = self.daño(enemigo) 
        if select<=self.fail: 
            print(f"{self.nombre} ha fallado su ataque")
        else:
            enemigo.vida = enemigo.vida - daño
            print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
            if enemigo.esta_vivo:
                print(f"la vida de {enemigo.nombre} es {enemigo.vida} ")
            else:
                enemigo.morir()

    def morir(self):
        self.vida = 0
        print(f" El Enemigo {self.nombre} está muerto")

class Dragon(Personaje):
    def __init__(self,nombre,vida,fuerza):
        """
        Constructor de clase Dragón
        charging: booleano de cargar ataque
        multiplicador: aumentod de daño por multiplicador
        """
        self.nombre = nombre
        self.vida = vida
        self.fuerza = fuerza
        self.defensa = 50
        self.charging = False
        self.multiplicador = 1

    def atributos(self):
        print("nombre ",self.nombre)
        print("vida ",self.vida)
        print("-Fuerza: ", self.fuerza)
        print("-Defensa : " , self.defensa)
        print("-Vida: " , self.vida)
    
    def atacar(self,enemigo):
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
        if enemigo.esta_vivo:
            print(f"la vida de {enemigo.nombre} es {enemigo.vida} ")
        else:
            enemigo.morir()

        if self.charging:
            self.fuerza = int(   self.fuerza/(self.multiplicador))  
            print("Tu fuerza  vuelve a ",self.fuerza)
            self.charging = False
            self.multiplicador = 1

    def bajar_defensa(self,enemigo:Enemigo):
        """
        Reduce en 20 puntos 
        la defensa del enemigo
        """
        enemigo.defensa -= 20
        print(f"{self.nombre} emite una ráfaga de fuego sobre {enemigo.nombre}")
        print(f"{self.nombre} ha bajado en 20 puntos la defensa a {enemigo.nombre}")
        print(f"su defensa es ahora {enemigo.defensa}")
    
    def cargar_ataque(self,enemigo:Enemigo):
        """
        Usa el turno para aumentar el daño
        Se puede hacer hasta 3 veces
        """
        if self.multiplicador == 8:
            print("Suficientes cargas!")
            self.atacar(enemigo)
        else:
            print(self.nombre, "está cargando un ataque poderoso...")
            self.multiplicador *= 2
            print("Multiplicador x",self.multiplicador)
            self.charging = True
            self.fuerza *= 2
            print("Fuerza es ",self.fuerza)

class IceDragon(Dragon):
    def bajar_defensa(self,enemigo:Enemigo):
        """
        Reduce en 30 puntos 
        la defensa del enemigo
        """
        enemigo.defensa -= 30
        print(f"{self.nombre} desata un torbellino de hielo sobre {enemigo.nombre}")
        print(f"{self.nombre} ha bajado en 30 puntos la defensa a {enemigo.nombre}")
        print(f"su defensa es ahora {enemigo.defensa}")

class ElectricDragon(Dragon):   
    def bajar_defensa(self,enemigo:Enemigo):
        """
        Reduce en 40 puntos 
        la defensa del enemigo
        """
        enemigo.defensa -= 40
        print(f"{self.nombre} emite un aura eléctrica  sobre {enemigo.nombre}")
        print(f"{self.nombre} ha bajado en 40 puntos la defensa a {enemigo.nombre}")
        print(f"su defensa es ahora {enemigo.defensa}")


