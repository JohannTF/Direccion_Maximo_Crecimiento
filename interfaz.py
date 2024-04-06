import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import operaciones

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana principal
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title("Analsis Vectorial")
        self.resizable(1, 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Configuración de la figura
        self.fig = plt.figure(figsize=(7,6))
        self.ax = plt.axes(projection='3d')
        self.configuracionFigura()
        self.principal()

    def configuracionFigura(self):
        self.ax.set_xlabel("X", color=(1, 1, 1), fontweight="bold")
        self.ax.set_ylabel("Y", color=(1, 1, 1), fontweight="bold")
        self.ax.set_zlabel("Z", color=(1, 1, 1), fontweight="bold")
        self.ax.set_title((r'$f\:\left(x,\:y\right)\:=\:x^a+y^b+c\cdot x\cdot y$'), color=(1, 1, 1), fontsize=18, fontweight="bold")
        self.ax.tick_params(labelcolor='tab:green')
        self.ax.set_facecolor('#242424')
        self.fig.set_facecolor('#242424')
        self.ax.view_init(20, 30)

    def obtenerDatos(self, opciones, canvas):
        self.ax.clear()
        # Obtener los datos ingresado convertirlos a entero
        dato = [int(opciones[key].get()) for key in opciones.keys()]
        # Llamado a la clase para graficar los resultados y pasando los datos enteros como argumento
        operaciones.Graficar(
            a=dato[0],
            b=dato[1],
            c=dato[2],
            pX=dato[3],
            pY=dato[4],
            n=dato[5],
            ax=self.ax,
            fig= self.fig
        )
        # Dibujar el gráfico resultante
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column=0, sticky="nwes")

    
    def principal(self):
        # Frame principal y sus configuraciones iniciales
        frame_main = customtkinter.CTkFrame(self)
        frame_main.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", )
        frame_main.grid_rowconfigure((0,1), weight=1)
        frame_main.grid_columnconfigure((0,1), weight=1, uniform='column')

        # Frame para los datos
        frame_sub1 = customtkinter.CTkFrame(frame_main)
        frame_sub1.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        frame_sub1.grid_columnconfigure((0,1), weight=1)

        # Frame para el gráfico
        frame_sub2 = customtkinter.CTkFrame(frame_main)
        frame_sub2.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        # Solo una celda (col=0, row=0) para el grafico
        frame_sub2.grid_rowconfigure(0, weight=1)
        frame_sub2.grid_columnconfigure(0, weight=1)
        
        # Titulo
        # Agregar una nueva fila al frame_sub1 para el titulo
        frame_sub1.grid_rowconfigure(0, weight=1)
        label = customtkinter.CTkLabel(master=frame_sub1, text="Dirección de Maximo Crecimiento", font=("timmana", 28))
        label.grid(row=0, column=0, columnspan=frame_sub1.grid_size()[0], sticky="nsew", pady=1, padx=1)

        # Label con su valor de cada opción
        opciones = {
            "a": "0",
            "b": "0", 
            "c": "0", 
            "Punto en X": "0", 
            "Punto en Y": "0", 
            "Num Vectores": "0"
        }

        # Insertar las opciones al frame_sub1
        for indice, clave in enumerate(opciones):
            # Agregar una nueva fila al frame_sub1
            frame_sub1.grid_rowconfigure(indice+1, weight=1)

            # Label
            label = customtkinter.CTkLabel(master=frame_sub1, text=clave, font=("Arial", 18))
            label.grid(row=indice+1, column=0, sticky="e", pady=5, padx=10)

            # Entradas
            opciones[clave] = customtkinter.CTkEntry(master=frame_sub1, justify="center", corner_radius=5)
            opciones[clave].grid(row=indice+1, column=1, sticky="w", pady=5, padx=10)

        # Dibujar el gráfico
        canvas = FigureCanvasTkAgg(self.fig, master=frame_sub2)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column=0, sticky="nwes")

        # Boton para calcular
        boton = customtkinter.CTkButton(master=frame_sub1, text="Calcular", command=lambda: self.obtenerDatos(opciones, canvas), cursor='hand2')
        boton.grid(row=frame_sub1.grid_size()[1], column=0, columnspan=frame_sub1.grid_size()[0], sticky="nsew", pady=10, padx=10)

interfaz = GUI()
interfaz.mainloop()