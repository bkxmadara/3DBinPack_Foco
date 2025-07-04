import random
from copy import deepcopy
from classes_cba import Caminhao, Carga

class AlgoritmoGenetico:
    class Individuo:
        def __init__(self, cargas, caminhoes):
            self.cargas = deepcopy(cargas)
            self.caminhoes = deepcopy(caminhoes)
            self.avaliar()

        def avaliar(self):
            self.fitness = 0
            self.alocacao = {c.id: None for c in self.cargas}
            self.penalidade = 0

            for caminhao in self.caminhoes:
                espaco_ocupado = []
                peso_total = 0

                for carga in self.cargas:
                    if random.random() < 0.5:
                        pos = self.encontrar_posicao_valida(caminhao, espaco_ocupado, carga)
                        if pos:
                            x, y, z = pos
                            carga._x, carga._y, carga._z = x, y, z
                            self.alocacao[carga.id] = caminhao.id
                            espaco_ocupado.append((carga, (x, y, z)))
                            peso_total += carga.peso_bruto

                if peso_total > caminhao.capacidade_total_carga():
                    excesso = peso_total - caminhao.capacidade_total_carga()
                    self.penalidade += excesso * 10

            self.fitness = -self.penalidade

        def encontrar_posicao_valida(self, caminhao, ocupados, carga):
            for z in range(0, int(caminhao.altura - carga.altura) + 1):
                for y in range(0, int(caminhao.largura - carga.largura) + 1):
                    for x in range(0, int(caminhao.profundidade - carga.profundidade) + 1):
                        colisao = False
                        for (outra, (ox, oy, oz)) in ocupados:
                            if (
                                x < ox + outra.largura and x + carga.largura > ox and
                                y < oy + outra.profundidade and y + carga.profundidade > oy and
                                z < oz + outra.altura and z + carga.altura > oz
                            ):
                                colisao = True
                                break
                        if not colisao:
                            return (x, y, z)
            return None

    @staticmethod
    def crossover(pai1, pai2):
        corte = len(pai1.cargas) // 2
        filho_cargas = pai1.cargas[:corte] + pai2.cargas[corte:]
        return AlgoritmoGenetico.Individuo(filho_cargas, pai1.caminhoes)

    @staticmethod
    def mutacao(individuo, taxa=0.1):
        for carga in individuo.cargas:
            if random.random() < taxa:
                carga._x = random.randint(0, 5)
                carga._y = random.randint(0, 2)
                carga._z = random.randint(0, 2)
        individuo.avaliar()

    @classmethod
    def execute(cls, cargas, caminhoes, geracoes=30, populacao_tam=20):
        populacao = [cls.Individuo(cargas, caminhoes) for _ in range(populacao_tam)]

        for geracao in range(geracoes):
            populacao.sort(key=lambda ind: ind.fitness, reverse=True)
            nova_populacao = populacao[:5]

            while len(nova_populacao) < populacao_tam:
                pai1, pai2 = random.sample(populacao[:15], 2)
                filho = cls.crossover(pai1, pai2)
                cls.mutacao(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao
            print(f"Geração {geracao}: Melhor fitness = {populacao[0].fitness}")

        melhor = populacao[0]
        resultado = {}

        for caminhao in melhor.caminhoes:
            resultado[caminhao.id] = []

        for carga in melhor.cargas:
            cid = melhor.alocacao[carga.id]
            if cid is not None:
                resultado[cid].append({
                    'id': carga.id,
                    'coordenada': (carga._x, carga._y, carga._z)
                })

        return resultado
