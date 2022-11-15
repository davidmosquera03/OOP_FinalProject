from tkinter import *
from tkvideo import *

class visual:
    """
    Generalizador para insertar fotos y
    videos con Tkinter y Tkvideo
    
    + path: ruta del directorio de la foto o video
    """
    def __init__(self, path:str,):
        self.path = path
        

    def foto(self, path):
        ventana = Tk()
        ventana.geometry("800x450")
        ventana.title("Lynx Game")
        ventana.iconbitmap("img\\1_lynx-lynx.ico")
        ventana.resizable(False, False)
        
        imagen = PhotoImage(file = path)
        Lblimagen = Label(ventana, image = imagen).place(x=0, y=0)
        
        def destruir_ventana():
            ventana.destroy()
        
        ventana.after(3000,destruir_ventana)
        
        ventana.mainloop()
        
    def video_gif(self, path:str):
        ventana = Tk()
        ventana.geometry("800x450")
        ventana.title("Lynx Game")
        ventana.iconbitmap("img\\1_lynx-lynx.ico")
        ventana.resizable(False, False)

        my_label = Label(ventana)
        my_label.pack()
        player = tkvideo(path, my_label, loop = 0, size = (800,450))
        player.play()
        
        def destruir_ventana():
            ventana.destroy()
        
        ventana.after(3000,destruir_ventana)
        
        ventana.mainloop()
    
   
        

#prueba foto
#bienvenida = visual("--.png")
#bienvenida.foto("--.png")

#prueba video
#Inicio = visual("--")
#Inicio.video_gif("--")

