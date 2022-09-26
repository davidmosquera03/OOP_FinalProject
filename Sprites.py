import time
class Personaje:

    def __init__(self, nombre, fuerza, inteligencia,defensa,vida):
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida 
        self.nivel = 1 
    
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
                    
    ##get y set 
    def get_fuerza(self):
        return self.fuerza

    def set_fuerza(self, fuerza):
        if fuerza < 0:
            print("Error, has introducido un valor negativo")
        else:
            self.fuerza = fuerza
    def cambiar_arma(self):
        pass
  
##PARTE DE HERENCIA
class guerrero(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.espada = 1
        self.cambiar_arma()

    def cambiar_arma(self):
        opcion = int(input("Elige un arma: (1) Acero Valkyria, daño +8 defensa +5. (2) Matadragones, daño +10 \n"))
        if opcion == 1:
            self.espada = 8 
            self.defensa += 2
        elif opcion == 2 :
            self.espada = 10
        else:
            print("Numero de arma incorrecto")
        
    def atributos(self):
        super().atributos()
        return (f"-Espada: {self.espada}")
        
    def daño(self,enemigo):
        daño = self.fuerza*self.espada - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0
        

class mago(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)  
        self.libro = 1
        self.cambiar_arma()    
    
    def cambiar_arma(self):
            opcion = int(input("Elige un arma: (1) Cetro Vampirico, libro +14. (2) Cetro de valhala , libro +10 vida+5\n"))
            if opcion == 1:
                self.libro = 14
            elif opcion == 2 :
                self.libro = 10
                self.vida +=5
            else:
                print("Numero de arma incorrecto")    
        
    def atributos(self):
        super().atributos()  
        return(f"-Libro: {self.libro}")
        
    def daño(self, enemigo):
        daño = self.inteligencia*self.libro - enemigo.defensa
        if daño>0 :
             return daño
        else:
            return 0
        
class arquero(Personaje):
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.critico = 1
        self.cambiar_arma()
    
    def cambiar_arma(self):
            opcion = int(input("Elige un arma: (1) Arco Ionico, critico +8 vida +5. (2) Matacraquens , critico +19\n "))
            if opcion == 1:
                self.critico = 8
                self.vida+=5
            elif opcion == 2 :
                self.critico = 19
            else:
                print("Numero de arma incorrecto")    
    
    def atributos(self):
        super().atributos()
        return(f"-Critico: {self.critico}")
    
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


