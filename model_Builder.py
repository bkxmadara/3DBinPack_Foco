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
            familias_por_caminhao = {c.id: set() for c in self.caminhoes}
            self.penalidade = 0

            # Zera peso_cima de todas as cargas
            for carga in self.cargas:
                carga.peso_cima = 0.0

            for caminhao in self.caminhoes:
                espaco_ocupado = []
                peso_total = 0
                volume_total = 0

                for carga in random.sample(self.cargas, len(self.cargas)):
                    if random.random() < 0.5:
                        pos = self.encontrar_posicao_valida(caminhao, espaco_ocupado, carga)
                        if pos:
                            x, y, z = pos
                            carga._x, carga._y, carga._z = x, y, z
                            self.alocacao[carga.id] = caminhao.id

                            if (carga.peso_bruto + peso_total) < caminhao.capacidade_total_carga():
                                espaco_ocupado.append((carga, (x, y, z)))
                                peso_total += carga.peso_bruto
                                volume_total += carga.volume()
                                familias_por_caminhao[caminhao.id].add(carga.lote)
                            else:
                                break

                # Penalidade por centro de gravidade deslocado
                ocupadas = [c for (c, _) in espaco_ocupado]
                if peso_total > 0:
                    cg_x = sum(
                        (c.get_x() + c.largura / 2) * c.peso_bruto for c in ocupadas
                    ) / peso_total
                    cg_y = sum(
                        (c.get_y() + c.profundidade / 2) * c.peso_bruto for c in ocupadas
                    ) / peso_total
                    cg_z = sum(
                        (c.get_z() + c.altura / 2) * c.peso_bruto for c in ocupadas
                    ) / peso_total

                    alvo_x = caminhao.profundidade / 2
                    alvo_y = caminhao.largura / 2
                    alvo_z = caminhao.altura / 2

                    deslocamento = ((cg_x - alvo_x) ** 2 + (cg_y - alvo_y) ** 2 + (cg_z - alvo_z) ** 2) ** 0.5
                    self.penalidade += deslocamento * 100

                # Penalidade por múltiplas famílias
                if len(familias_por_caminhao[caminhao.id]) > 1:
                    self.penalidade += 1000 * len(familias_por_caminhao[caminhao.id])

                # Penalidade por sobra de volume
                if volume_total < caminhao.volume():
                    sobra = caminhao.volume() - volume_total
                    caminhao.set_sobra_volume(sobra)
                    self.penalidade += sobra * 10

                # Atualiza sobra de carga
                sobra = caminhao.capacidade_total_carga() - peso_total
                caminhao.set_sobra_carga(sobra)

                # Verifica empilhamento e atualiza peso_cima
                for base, (bx, by, bz) in espaco_ocupado:
                    peso_em_cima = 0.0
                    for topo, (tx, ty, tz) in espaco_ocupado:
                        if topo == base:
                            continue
                        sobrepoe_x = not (tx + topo.largura <= bx or tx >= bx + base.largura)
                        sobrepoe_y = not (ty + topo.profundidade <= by or ty >= by + base.profundidade)
                        em_cima = abs(tz - (bz + base.altura)) < 0.01

                        if sobrepoe_x and sobrepoe_y and em_cima:
                            peso_em_cima += topo.peso_bruto
                            peso_em_cima += self._peso_acima_recursivo(topo, espaco_ocupado)

                    base.peso_cima = peso_em_cima

                    if peso_em_cima > base.peso_suportado:
                        excesso = peso_em_cima - base.peso_suportado
                        self.penalidade += excesso * 1000

            self.fitness = self.penalidade

        def _peso_acima_recursivo(self, carga, ocupados):
            peso = 0.0
            cx, cy, cz = carga.get_x(), carga.get_y(), carga.get_z()

            for topo, (tx, ty, tz) in ocupados:
                if topo == carga:
                    continue
                sobrepoe_x = not (tx + topo.largura <= cx or tx >= cx + carga.largura)
                sobrepoe_y = not (ty + topo.profundidade <= cy or ty >= cy + carga.profundidade)
                em_cima = abs(tz - (cz + carga.altura)) < 0.01

                if sobrepoe_x and sobrepoe_y and em_cima:
                    peso += topo.peso_bruto
                    peso += self._peso_acima_recursivo(topo, ocupados)

            return peso

        def encontrar_posicao_valida(self, caminhao, ocupados, carga):
            candidatos = set()
            candidatos.add((0, 0, 0))

            for outra, (ox, oy, oz) in ocupados:
                candidatos.add((round(ox + outra.largura, 2), round(oy, 2), round(oz, 2)))
                candidatos.add((round(ox, 2), round(oy + outra.profundidade, 2), round(oz, 2)))
                candidatos.add((round(ox, 2), round(oy, 2), round(oz + outra.altura, 2)))

            for (x, y, z) in candidatos:
                if (
                    x + carga.largura > caminhao.profundidade or
                    y + carga.profundidade > caminhao.largura or
                    z + carga.altura > caminhao.altura
                ):
                    continue

                colisao = False
                for outra, (ox, oy, oz) in ocupados:
                    if (
                        x < ox + outra.largura and x + carga.largura > ox and
                        y < oy + outra.profundidade and y + carga.profundidade > oy and
                        z < oz + outra.altura and z + carga.altura > oz
                    ):
                        colisao = True
                        break

                if not colisao:
                    return (round(x, 2), round(y, 2), round(z, 2))

            return None

    @staticmethod
    def crossover(pai1, pai2):
        corte = len(pai1.cargas) // 2
        filho_cargas = pai1.cargas[:corte] + pai2.cargas[corte:]
        return AlgoritmoGenetico.Individuo(filho_cargas, pai1.caminhoes)

    @staticmethod
    def mutacao(individuo, taxa=0.5):
        for carga in individuo.cargas:
            if random.random() < taxa:
                carga._x = random.randint(0, 4)
                carga._y = random.randint(0, 4)
                carga._z = random.randint(0, 4)
        individuo.avaliar()

    @classmethod
    def execute(cls, cargas, caminhoes, geracoes, populacao_tam):
        populacao = [cls.Individuo(cargas, caminhoes) for _ in range(populacao_tam)]

        for geracao in range(geracoes):
            populacao.sort(key=lambda ind: ind.fitness)
            nova_populacao = populacao[:5]

            while len(nova_populacao) < populacao_tam:
                pai1, pai2 = random.sample(populacao[:15], 2)
                filho = cls.crossover(pai1, pai2)
                cls.mutacao(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao
            print(f"Geração {geracao}: Melhor fitness = {populacao[0].fitness}")

        melhor = populacao[0]
        caminhoes_em_uso = []

        for caminhao in melhor.caminhoes:
            caminhao.lista_cargas = []
            caminhao.status = "disponível"

        for carga in melhor.cargas:
            cid = melhor.alocacao[carga.id]
            if cid is not None:
                caminhao = next(c for c in melhor.caminhoes if c.id == cid)
                carga.status = "atribuída"
                if carga not in caminhao.lista_cargas:
                    caminhao.lista_cargas.append(carga)
                caminhao.status = "em uso"
                if caminhao not in caminhoes_em_uso:
                    caminhoes_em_uso.append(caminhao)

        return caminhoes_em_uso
