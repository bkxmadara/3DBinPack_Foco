# Importa tudo do módulo data_Loader (provavelmente define as classes de dados)
from data_Loader import *
# Importa tudo do módulo classesCBA (provavelmente define classes como Carga e Caminhão)
from classesCBA import *
# Módulos padrão
import random  # Para gerar números aleatórios
from copy import deepcopy  # Para copiar objetos profundamente

# -------------------------------
# Classe que representa um indivíduo da população do algoritmo genético
# -------------------------------
class Individuo:
    def __init__(self, cargas, caminhoes):
        # Cria uma cópia profunda das cargas e caminhões recebidos
        self.cargas = deepcopy(cargas)
        self.caminhoes = deepcopy(caminhoes)
        # Avalia o indivíduo (define fitness e penalidade)
        self.avaliar()

    def avaliar(self):
        # Inicializa o fitness e a penalidade
        self.fitness = 0
        # Dicionário para armazenar qual carga foi alocada em qual caminhão
        self.alocacao = {c.id: None for c in self.cargas}
        self.penalidade = 0

        # Para cada caminhão disponível
        for caminhao in self.caminhoes:
            espaco_ocupado = []  # Lista de espaços já ocupados por cargas
            peso_total = 0  # Peso total carregado neste caminhão

            # Para cada carga, decide aleatoriamente se ela vai para este caminhão
            for carga in self.cargas:
                if random.random() < 0.5:  # 50% de chance de tentar alocar a carga
                    pos = self.encontrar_posicao_valida(caminhao, espaco_ocupado, carga)
                    if pos:
                        # Se encontrou posição válida, atualiza coordenadas da carga
                        x, y, z = pos
                        carga._x, carga._y, carga._z = x, y, z
                        self.alocacao[carga.id] = caminhao.id  # Registra a alocação
                        espaco_ocupado.append((carga, (x, y, z)))
                        peso_total += carga.peso_bruto

            # Verifica se o peso excede a capacidade, aplicando penalidade
            if peso_total > caminhao.capacidade_total_carga():
                excesso = peso_total - caminhao.capacidade_total_carga()
                self.penalidade += excesso * 10  # Penalidade proporcional ao excesso

        # O fitness é negativo pois queremos minimizar penalidades
        self.fitness = -self.penalidade

    def encontrar_posicao_valida(self, caminhao, ocupados, carga):
        """
        Tenta encontrar uma posição dentro do caminhão onde a carga não colida com as demais.
        """
        for z in range(0, int(caminhao.altura - carga.altura) + 1):
            for y in range(0, int(caminhao.largura - carga.largura) + 1):
                for x in range(0, int(caminhao.profundidade - carga.profundidade) + 1):
                    colisao = False
                    # Verifica colisão com outras cargas já alocadas
                    for (outra, (ox, oy, oz)) in ocupados:
                        if (
                            x < ox + outra.largura and x + carga.largura > ox and
                            y < oy + outra.profundidade and y + carga.profundidade > oy and
                            z < oz + outra.altura and z + carga.altura > oz
                        ):
                            colisao = True
                            break
                    if not colisao:
                        # Se não houver colisão, retorna posição válida
                        return (x, y, z)
        # Não encontrou posição válida
        return None

# -------------------------------
# Operador de crossover: combina dois indivíduos (pais) gerando um filho
# -------------------------------
def crossover(pai1, pai2):
    # Ponto de corte no meio da lista de cargas
    corte = len(pai1.cargas) // 2
    # O filho herda metade das cargas do pai1 e metade do pai2
    filho_cargas = pai1.cargas[:corte] + pai2.cargas[corte:]
    # Retorna novo indivíduo com os caminhões do pai1 (assumindo que são iguais)
    return Individuo(filho_cargas, pai1.caminhoes)

# -------------------------------
# Operador de mutação: altera aleatoriamente posições de cargas
# -------------------------------
def mutacao(individuo, taxa=0.1):
    # Para cada carga, com probabilidade 'taxa', muda a posição aleatoriamente
    for carga in individuo.cargas:
        if random.random() < taxa:
            carga._x = random.randint(0, 5)
            carga._y = random.randint(0, 2)
            carga._z = random.randint(0, 2)
    # Reavalia o indivíduo após a mutação
    individuo.avaliar()

# -------------------------------
# Função principal do algoritmo genético
# -------------------------------
def algoritmo_genetico(cargas, caminhoes, geracoes, populacao_tam):
    # Cria população inicial de indivíduos aleatórios
    populacao = [Individuo(cargas, caminhoes) for _ in range(populacao_tam)]

    for geracao in range(geracoes):
        # Ordena população pelo fitness (maior fitness primeiro)
        populacao.sort(key=lambda ind: ind.fitness, reverse=True)
        nova_populacao = populacao[:5]  # Mantém os 5 melhores indivíduos (elitismo)

        # Preenche o restante da população com filhos gerados por crossover e mutação
        while len(nova_populacao) < populacao_tam:
            # Seleciona dois pais aleatórios entre os 15 melhores
            pai1, pai2 = random.sample(populacao[:15], 2)
            filho = crossover(pai1, pai2)
            mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao
        # Mostra progresso
        print(f"Geração {geracao}: Melhor fitness = {populacao[0].fitness}")

    # Retorna a melhor solução encontrada
    melhor = populacao[0]
    resultado = {}

    # Inicializa resultado por caminhão
    for caminhao in melhor.caminhoes:
        resultado[caminhao.id] = []

    # Preenche resultado com as coordenadas finais de cada carga alocada
    for carga in melhor.cargas:
        cid = melhor.alocacao[carga.id]
        if cid is not None:
            resultado[cid].append({
                'id': carga.id,
                'coordenada': (carga._x, carga._y, carga._z)
            })

    return resultado
