import time

class Personaje:

    def __init__(self, nombre, fuerza, inteligencia,defensa,vida):
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida 
        self.nivel = 1 
        self.potions = 2
    
    def atributos(self):
        print(self.nombre, " : " ,)
        print("-Nivel: ",self.nivel)
        print("-Fuerza: ", self.fuerza)
        print("-Inteligencia: ", self.inteligencia)
        print("-Defensa : " , self.defensa)
        print("-Vida: " , self.vida)
     
    def subir_nivel(self, fuerza, inteligencia, defensa):
        self.nivel+=1
        print("Has subido tu personaje al nivel ",self.nivel)
        time.sleep(1)
        self.fuerza +=  fuerza
        self.inteligencia += inteligencia
        self.defensa += defensa
        self.atributos()
     
    def esta_vivo(self):
        return self.vida > 0 
        
    def morir(self):
        self.vida = 0
        print(f" El jugador {self.nombre} esta muerto")
        
        
    def daño(self, enemigo):
        daño = self.fuerza - enemigo.defensa
        if daño<0:
            return 0
        return daño
    
    def atacar (self,enemigo):
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
        if enemigo.esta_vivo():
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

        
        
    def atributos(self):
        super().atributos()
        print(f"-Espada: {self.espada}")
        
    def daño(self,enemigo):
        daño = self.fuerza*self.espada - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0
        

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
        
    def daño(self, enemigo):
        daño = self.inteligencia*self.libro - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0
        
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
     
    
    def daño(self, enemigo):
        daño = self.fuerza * self.critico - enemigo.defensa 
        if daño>0:
            return daño
        else: 
            return 0

class Enemigo(Personaje):
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

    def daño(self, enemigo):
        daño = self.fuerza - enemigo.defensa
        if daño<0:
            return 0
        return daño
    
    def atacar (self,enemigo):
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(f"{self.nombre} ha realizado {daño} puntos de daño a {enemigo.nombre}")
        if enemigo.esta_vivo():
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
    pass

class ElectricDragon(Dragon):   
    pass



