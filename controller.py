from tkinter import Tk
import main


class Controller:
    def __init__(self, ventana):

        """ La función importa la clase Panel del archivo main """

        self.mi_ventana = ventana
        self.objeto_main = main.Panel(self.mi_ventana)


if __name__ == "__main__":
    
    
    mi_ventana = Tk()
    mi_app = Controller(mi_ventana)
    mi_ventana.mainloop()
