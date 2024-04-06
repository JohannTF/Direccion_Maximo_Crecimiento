from math import sqrt
import numpy as np
from sympy import diff, lambdify, symbols

class Logica():
    def __init__(self, a, b, c, pX, pY, n, ax):
        self.x, self.y = symbols('x y')
        self.ax = ax
        self.puntoInicioX = pX
        self.puntoInicioY = pY
        self.valorA = a
        self.valorB = b
        self.valorC = c
        self.numVectores = n
        self.funcionOriginal = (self.x**a)+(self.y**b)+(self.x*self.y*c)
        # La derivada de la función con respecto a X
        self.parcialX = diff(self.funcionOriginal, self.x)

        # La derivadad de la función con respecto a Y
        self.parcialY = diff(self.funcionOriginal, self.y)

        # Evalua la 'funciónOriginal' con respecto de (x, y) y el resultado es lo que retorna 'fz()'
        self.fz = lambdify((self.x, self.y), self.funcionOriginal) # fz(valorX, valorY)
        self.puntoInicioZ = self.fz(self.puntoInicioX, self.puntoInicioY)

        # Evalua la 'parcialX' con respecto de (x, y) y el resultado es lo que retorna 'evaluacionEnParcialX'
        self.evaluacionEnParcialX = lambdify((self.x, self.y), self.parcialX) # evaluacionEnParcialX(valorX, valorY)

        # Evalua la 'parcialY' con respecto de (x, y) y el resultado es lo que retorna 'evaluacionEnParcialY'
        self.evaluacionEnParcialY = lambdify((self.x, self.y), self.parcialY) # evaluacionEnParcialY(valorX, valorY)


    def vectorUnitario(self, puntoEnX, puntoEnY):
        componenteX = self.evaluacionEnParcialX(puntoEnX, puntoEnY)
        componenteY = self.evaluacionEnParcialY(puntoEnX, puntoEnY)

        componenteX_cuadrado = pow(componenteX, 2)
        componenteY_cuadrado = pow(componenteY, 2)

        magnitud = sqrt(componenteX_cuadrado + componenteY_cuadrado)

        if(magnitud == 0):
            return 0, 0
        else:
            componenteX /= magnitud
            componenteY /= magnitud
        return componenteX, componenteY
    

    def vectores(self):
        # Arreglo con los colores para cada vector
        colores = ['k','r', 'g','brown','c','m','grey','pink', 'y', 'violet']

        # Marcar el punto de inicio
        self.ax.scatter(self.puntoInicioX, self.puntoInicioY, self.puntoInicioZ, color = colores[0])

        # Anotar las cordenadas del punto de inicio
        self.ax.text(
            self.puntoInicioX, self.puntoInicioY, self.puntoInicioZ # Posición donde está el cuadro de texto
            , "({},{},{:.2f})".format(self.puntoInicioX, self.puntoInicioY, self.puntoInicioZ) # Mensaje que contendrá el cuadro de texto
            , horizontalalignment='left' # La alineación del texto en el cuadro
            , color= colores[0] # El color del texto
            , weight='semibold'
        )
        # Arreglo de dos dimensiones inicializado con los puntos iniciales
        xyz = np.array([[0, 0, 0], [self.puntoInicioX, self.puntoInicioY, self.puntoInicioZ]], dtype=float)

        for i in range(self.numVectores):
            # Calcular la componente en 'x' y en 'y' del vector, tomando como punto de inicio el punto final anterior
            vectorCompX, vectorCompY = self.vectorUnitario(xyz[1][0], xyz[1][1])

            # Asignar el punto final del anterior vector como el nuevo punto de inicio del siguiente vector
            xyz[0] = xyz[1]

            # Agregado a la componente en 'x' y a la componente en 'y' los puntos de partida
            vectorCompX += xyz[0][0]
            vectorCompY += xyz[0][1]

            # Calcular la componente en 'z'
            vectorCompZ = self.fz(vectorCompX, vectorCompY)

            # El nuevo punto final del vector
            xyz[1] = [vectorCompX, vectorCompY, vectorCompZ]

            # Marcar el punto final de cada vector
            self.ax.scatter(xyz[1][0], xyz[1][1], xyz[1][2], color = colores[i%10])

            # Trazar los 'n' vectores desde un punto de partida hasta el final
            self.ax.plot(
                (xyz[0][0], xyz[1][0]) # Inicio y final para la componente en X
                , (xyz[0][1], xyz[1][1]) # Inicio y final para la componente en y
                , (xyz[0][2], xyz[1][2]) # Inicio y final para la componente en z
                , color=colores[i%10] # Color de cada linea
            )

        # Anotar las cordenadas del último punto (x,y,z) siempre y cuando el punto inicial sea distinto de 0
        self.ax.text(
            xyz[1][0], xyz[1][1], xyz[1][2] # Posición donde está el cuadro de texto
            , "({:.2f},{:.2f},{:.2f})".format(xyz[1][0], xyz[1][1], xyz[1][2]) # Mensaje que contendrá el cuadro de texto
            , horizontalalignment='left' # La alineación del texto en el cuadro
            , color= colores[0] # El color del texto
            , weight='semibold' #
        )


class Graficar(Logica):
    def __init__(self, a, b, c, pX, pY, n, ax, fig):
        super().__init__(a, b, c, pX, pY, n, ax)
        self.ax = ax
        self.fig = fig
        self.RESOLUCION = 10 # 10-100
        self.configuracionFigura()
        self.vectores()
        self.vistaFigura()

    def configuracionFigura(self):
        # Configuraciones iniciales de la figura
        self.ax.set_xlabel("X", color=(1, 1, 1), fontweight="bold")
        self.ax.set_ylabel("Y", color=(1, 1, 1), fontweight="bold")
        self.ax.set_zlabel("Z", color=(1, 1, 1), fontweight="bold")
        self.ax.set_title((r'$f\:\left(x,\:y\right)\:=\:x^a+y^b+c\cdot x\cdot y$'), color=(1, 1, 1), fontsize=18, fontweight="bold")
        self.ax.tick_params(labelcolor='tab:green')
        self.ax.set_facecolor('#242424')
        self.fig.set_facecolor('#242424')
        self.ax.view_init(20, 30)
    
    def vistaFigura(self):
        # Dimensiones de los ejes 'x' y 'y'
        limite_X = self.ax.get_xlim()
        limite_Y = self.ax.get_ylim()

        # Para la dimensión de 'x' para f(x, y)
        inicioX = round(abs((limite_X[1]+1))*(-1))
        finalX = round(abs(limite_X[1]+1))

        # Para la dimensión de 'y' para f(x, y)
        inicioY =  round((limite_Y[1]+1)*(-1))
        finalY =  round(limite_Y[1]+1)

        # Creando los puntos evaluar 'x' y 'y' en la funcionOriginal
        x_puntos = np.arange(inicioX, finalX, (finalX-inicioX)/10)
        y_puntos = np.arange(inicioY, finalY, (finalY-inicioY)/10)
        xx, yy = np.meshgrid(x_puntos, y_puntos)

        # Resultados tras evaluar f(x, y) en los puntos datos por los arreglo 'xx' y 'yy'
        zz = np.empty(shape=(self.RESOLUCION, self.RESOLUCION))
        for i in range(self.RESOLUCION):
            for j in range(self.RESOLUCION):
                zz[i][j] = self.fz(xx[i][j], yy[i][j])

        # Puntos en 'x' y 'y' para generar la cuadricula (plano en z=0)
        baseX = [inicioX, finalX]
        baseY = [inicioY, finalY]
        baseX, baseY = np.meshgrid(baseX, baseY)
        baseZ = np.zeros(shape=(2,2))

        # Lineas de guía en los ejes y punto en el origen
        self.ax.plot([inicioX, finalX], [0 , 0], [0 , 0], color = 'r')
        self.ax.plot([0 , 0], [inicioY, finalY], [0 , 0], color = 'g')
        self.ax.plot([0 , 0], [0 , 0], [-zz[-1][-1], zz[-1][-1]], color = 'b')
        self.ax.scatter(0, 0, 0, color = 'black')

        # Superficie de la funcion
        self.ax.plot_surface(xx, yy, zz, color = "blue", alpha = 0.2)
        self.ax.plot_wireframe(xx, yy, zz, color = "blue", alpha = 0.1)

        # Superficie sobre el plano
        self.ax.plot_surface(baseX, baseY, baseZ, color = "black", alpha = 0.4)