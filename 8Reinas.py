# Problema de las 8 Reinas


import random
import matplotlib.pyplot as plot
import numpy

#Definimos una clase Cromosoma que nos serivira para representar un AG
class Cromosoma:
    def __init__(self, genes, aptitud):
        self.genes = genes
        self.aptitud = aptitud

    def len(self):
        return len(self.genes)

    def __str__(self):
        s="%s %d" % (" ".join(map(str, self.genes)), self.aptitud)
        s2=[]
        n=len(self.genes)
        for i in range(n):
            s2.append(list("."*n))
            for k in range(n):
                if self.genes[k] == i:
                    s2[i][k]="R"
            s2[i]=" ".join(s2[i])
        return "\n".join(s2)+"\nAptitud: " + str(self.aptitud)



class AGenetico:

    def __init__(self, tamanio):
        self.tamanio=tamanio
        self.genes=range(tamanio)

    def obtenerAptitud(self, genes):
        size = len(genes)
        print(genes)
        print(size)
        #Variables donde almacenaramos los ataques
        diagonal_izquierda_derecha = [0] * (2 * size - 1)
        diagonal_derecha_izquierda = [0] * (2 * size - 1)
        reinaCol = [0] * (2 * size - 1)
        reinaFila = [0] * (2 * size - 1)

        # Número de reinas en cada diagonal
        for i in range(size):
            reinaCol[i] += 1 # recorremos las columnas
            reinaFila[genes[i]] += 1 # recorremos las filas
            #Recorremos las diagonales
            diagonal_izquierda_derecha[i + genes[i]] += 1 # [columna + fila]
            diagonal_derecha_izquierda[size - 1 - i + genes[i]] += 1 # [size-1-columna+ fila]

        # Número de ataques en cada diagonal
        aptitud = 0
        for i in range(2 * size - 1):
            #Recorremos las columnas
            if reinaCol[i] > 1: # hay ataques
                aptitud += reinaCol[i] - 1 # n-1 ataques
            # Recorremos las filas
            if reinaFila[i] > 1:
                aptitud += reinaFila[i] - 1
            # recorremos todas las diagonales
            if diagonal_izquierda_derecha[i] > 1: # hay ataques
                aptitud += diagonal_izquierda_derecha[i] - 1 # n-1 ataques
            if diagonal_derecha_izquierda[i] > 1:
                aptitud += diagonal_derecha_izquierda[i] - 1

        print("aptitud",aptitud)
        return aptitud

    def nuevoPadre(self):
        genes = random.sample(self.genes, self.tamanio)
        aptitud = self.obtenerAptitud(genes)
        return Cromosoma(genes, aptitud)

    def cruza(self, x, y):
        c = random.randint(0, x.len())
        genes = x.genes[:c]+y.genes[c:]
        aptitud = self.obtenerAptitud(genes)
        return Cromosoma(genes, aptitud)

    def mutar(self, hijo):
        genes = hijo.genes[:]
        indice = random.randrange(0, len(hijo.genes))
        nuevoGen, alterno = random.sample(self.genes, 2)
        genes[indice] = alterno if nuevoGen == genes[indice] else nuevoGen
        hijo.aptitud = self.obtenerAptitud(genes)
        hijo.genes = genes
        #n=random.randint(0, hijo.len()-1)
        #genes=hijo.genes
        #genes[n]=-1
        #genX=genY=max(genes)
        #while genX in genes and genY in genes:
        # genX, genY = random.sample(self.genes, 2)
        #genes[n]= genX if genX in genes else genY
        #hijo.aptitud=self.obtenerAptitud(genes)
        #hijo.genes=genes
        return hijo

    def seleccion(self, poblacion):
        if len(poblacion)>0:
            return random.choice(poblacion)
        else:
            return self.nuevoPadre()

    def algoritmo(self, poblacion):
        while True:
            npobla = []
            for i in range(len(poblacion)):
                x = self.seleccion(poblacion)
                y = self.seleccion(poblacion)
                hijo = self.cruza(x, y)
                if random.randint(1, 20) < 3:
                    hijo = self.mutar(hijo)
                npobla.append(hijo)
                if npobla[i].aptitud == 0:
                    self.obtenerMejor(npobla[i])
                    print("Solucion encontrada")
                    return npobla[i].genes
            poblacion = npobla

    def run(self):
        poblacion = []
        for i in range(400):
            poblacion.append(self.nuevoPadre())
        return self.algoritmo(poblacion)
        # print(self.algoritmo(poblacion))

    def obtenerMejor(self, mejor):
        self.mejor = mejor
        print("Mejor")
        print(mejor)


if __name__ == "__main__":
    reinas = 8
    alg = AGenetico(reinas)
    best = alg.run()
    y = best
    x = alg.genes
    x = numpy.array(x)
    print(x)
    y = numpy.array(y)
    z = y
    print(y)
    x = x + 0.5
    y = y + 0.5
    plot.figure()
    plot.scatter(x, y, marker=r'$\mathrm{\mathbb{\Re}}$', color="black", s=1000)
    plot.xlim(0, reinas)
    plot.ylim(0, reinas)
    plot.xticks(x - 0.5)
    plot.yticks(x - 0.5)
    plot.grid(True)
    plot.title(u"Mejor Individuo")
    ax = plot.gca()
    ax.set_facecolor('gray')
    plot.show()
