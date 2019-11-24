import math
import random
from matplotlib import pyplot as plt

#multiplica um vetor por um escalar
def scalar_multiply (escalar, vetor):
    return [escalar * i for i in vetor]

#soma n vetores
def vector_sum (vetores):
    resultado = vetores[0]
    for vetor in vetores[1:]:
        resultado = [resultado[i] + vetor[i] for i in range(len(vetor))]
    return resultado

# calcula a média de n vetores
def vector_mean(vetores):
    return scalar_multiply(1/len(vetores), vector_sum(vetores))

def test_vector_mean ():
    a = [1, 2, 3]
    b = [1, 3, 2]
    c = [1, 1, 1]
    r = vector_mean([a, b, c])
    for elemento in r:
        print (elemento)

#produto escalar
def dot (v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

# subtração de vetores
def vector_subtract (v, w):
    return [v_i - w_i for v_i, w_i in zip (v, w)]

#soma dos quadrados
def sum_of_squares (v):
    return dot (v, v)

#distância ao quadrado
def squared_distance (v, w):
    return sum_of_squares (vector_subtract(v, w))

# distância
def distance(v, w):
    return math.sqrt(squared_distance(v,w))


class KMeans:
    def __init__ (self, k, means = None):
        self.k = k
        self.means = means
    def classify (self, ponto):
        return min (range (self.k), key = lambda i: distance(ponto, self.means[i]))
    def train (self, pontos):
        #escolha de k elementos
        self.means = random.sample (pontos, self.k) if self.means == None else self.means
        #nenhuma atribuição, para começar
        assignments = None
        while True:
            #associa cada instância a um inteiro 0 <= i < k
            new_assignments = list(map (self.classify, pontos))
            #se não houver mudança, termina
            if new_assignments == assignments:
                return
            #atribuição atual se torna a nova
            assignments = new_assignments
            #cálculo das novas médias
            for i in range (self.k):
            #pontos associados ao agrupamento i
            #note que pontos e assignments estão na ordem
            #por exemplo pontos = [1, 2, 3] e assignments = [1, 2, 2]
            #indicam que a primeira instância está no grupo 1 e as demais
            # no grupo 2
                i_points = [p for p, a in zip (pontos, assignments) if a == i]
            # tem alguém nesse grupo?
                if i_points:
                    self.means[i] = vector_mean (i_points)
            return assignments

def test_k_means ():
    kmeans = KMeans(3, [[1], [3], [11]])
    kmeans.train([[1], [2], [3], [6], [7], [10], [11]])
    print (kmeans.means)
    kmeans = KMeans(3)
    kmeans.train([[1], [2], [3], [6], [7], [10], [11]])
    print (kmeans.means)

# Adapte o algoritmo para que seja possível verificar cada um dos grupos.
def test_k_means_grupos ():
    grupo = 0
    teste = [[1], [2], [3], [6], [7], [10], [11], [14], [19]]
    kmeans = KMeans(3)
    indices = sorted(kmeans.train(teste))
    print (f'Objetos: {teste}')
    print (f'Train: {indices}')
    lista = []
    i = 0
    for elem in indices:
        if elem == grupo:
            lista.append(teste[i])
            i += 1
        else:
            print (f'Grupo{grupo} = {lista}')
            lista = []
            lista.append(teste[i])
            i += 1
            grupo += 1
    print (f'Grupo{grupo} = {lista}')



# Aula7 - Data: 18/Nov/2019
def gera_base(n):
    base = []
    for _ in range (n //3):
        x = random.randint(-50, -40)
        y = random.randint(0, 10)
        while (x, y) in base:
            x = random.randint(-50, -40)
            y = random.randint(0, 10)
        base.append((x, y))
    for _ in range (n //3):
        x = random.randint(-40, -10)
        y = random.randint(-10, 0)
        while (x, y) in base:
            x = random.randint(-40, -10)
            y = random.randint(-10, 0)
        base.append((x, y))
    for _ in range (n //3):
        x = random.randint(10, 20)
        y = random.randint(10, 20)
        while (x, y) in base:
            x = random.randint(10, 20)
            y = random.randint(10, 20)
        base.append((x, y))
    return base 

def test_gera_base ():
    base = gera_base(12)
    for elemento in base:
        print (elemento)

def calcula_somatorio_de_distancias (base, kmeans):
    soma = 0    
    for instancia in base:        
        dist = distance (instancia, kmeans.means[0])        
        for centroide in kmeans.means[1:]:
            if distance (instancia, centroide) < dist:
                dist = distance (instancia, centroide)        
        soma += dist    
    return soma

def test_calcula_somatorio_de_distancias():
    base = gera_base(6)
    kmeans = KMeans (3)
    kmeans.train(base)
    print (f'Total: {calcula_somatorio_de_distancias(base, kmeans):.2f}')

def exibe_grafico (base, representantes=[], distancia=-1):
    g1_x = [v[0] for v in base[:len(base)//3]]    
    g1_y = [v[1] for v in base[:len(base)//3]]
        
    g2_x = [v[0] for v in base[len(base)//3: len(base)//3 * 2 ]]    
    g2_y = [v[1] for v in base[len(base)//3: len(base)//3 * 2 ]]

    g3_x = [v[0] for v in base[len(base)//3 * 2: len(base)]]    
    g3_y = [v[1] for v in base[len(base)//3 * 2: len(base)]]    
    
    plt.scatter (g1_x, g1_y, marker='.')    
    plt.scatter (g2_x, g2_y, marker='*')    
    plt.scatter (g3_x, g3_y, marker='^')    
    for representante in representantes:        
        plt.scatter (representante[0], representante[1], marker="+")    
    plt.title(f'Somatório de distâncias: {distancia:.2f}')    
    plt.show()

def test_exibe_grafico ():
    base = gera_base(12)
    exibe_grafico(base)

def test_final ():    
    base = gera_base (120)    
    kmeans = KMeans (3)    
    kmeans.train(base)    
    distancia = calcula_somatorio_de_distancias(base, kmeans)    
    exibe_grafico (base, kmeans.means, distancia)


# Aula8 - Data: 19/Nov/2019
# Implemente a seguinte função. Para cada valor de k (a partir de 2), ela executa o algoritmo 
# KMeans i vezes e utiliza a função da aula de cálculo de distâncias, a fim de obter a distância
# média, m. Ela deve devolver o menor valor de k tal que m < limiar.
def obtem_melhor_k (base, i, limiar):
    distancia = limiar
    n = 2
    while distancia >= limiar:
        k = n
        distancia = 0
        for _ in range(i):
            kmeans = KMeans(k)
            kmeans.train(base)
            distancia += calcula_somatorio_de_distancias(base, kmeans)
        distancia /= i
        n += 1
        #print(f' Valor de k: {k}')
        #print(f' Distância média: {distancia:.2f}')
    #print(f' Valor de k: {k}')
    print(f'O Valor de k = {k}, que mais se aproxima do limite {limiar} aponta uma distância média: {distancia:.2f}')
    return k

def test_obtem_melhor_k ():
    base = gera_base (120)
    obtem_melhor_k (base, 5, 1000)



def main():
    pass
    #test_vector_mean ()
    #test_k_means ()
    #test_k_means_grupos ()
    #test_gera_base ()
    #test_calcula_somatorio_de_distancias()
    #test_exibe_grafico ()
    #test_final ()
    test_obtem_melhor_k ()
main()