from tkinter import *
from tkvideo import *

def foto(path,wait:int=5):
    ventana = Tk()
    ventana.geometry("850x450")
    ventana.title("Lynx Game")
    ventana.iconbitmap("img\\1_lynx-lynx.ico")
    ventana.resizable(False, False)
    ventana.overrideredirect(True)
        
    imagen = PhotoImage(file = path)
    Lblimagen = Label(ventana, image = imagen).place(x=0, y=0)
        
    def destruir_ventana():
        ventana.destroy()
        
    ventana.after(wait*1000,destruir_ventana)
        
    ventana.mainloop()
        
def video_gif(path:str,wait:int=5):
    ventana = Tk()
    ventana.geometry("800x450")
    ventana.title("Lynx Game")
    ventana.iconbitmap("img\\1_lynx-lynx.ico")
    ventana.resizable(False, False)
    ventana.overrideredirect(True)
    my_label = Label(ventana)
    my_label.pack()
    player = tkvideo(path, my_label, loop = 0, size = (800,450))
    player.play()
        
    def destruir_ventana():
        ventana.destroy()
        
    ventana.after(wait*1000,destruir_ventana)
        
    ventana.mainloop()
    
   
        

#prueba foto
#bienvenida = visual("--.png")
#bienvenida.foto("--.png")

#prueba video
#Inicio = visual("--")
#Inicio.video_gif("--")