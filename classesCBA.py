import random

class Caminhao:
    def __init__(self, id, nome, tipo_carga, altura, largura, profundidade, carga_por_eixo, quantidade_eixos):
        self.id = id
        self.nome = nome
        self.tipo_carga = tipo_carga
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade
        self.carga_por_eixo = carga_por_eixo
        self.quantidade_eixos = quantidade_eixos

    def volume_carga(self):
        return self.altura * self.largura * self.profundidade

    def capacidade_total_carga(self):
        return self.carga_por_eixo * self.quantidade_eixos

    def __str__(self):
        return (f"Caminhão {self.nome} (ID: {self.id})\n"
                f"Tipo de carga: {self.tipo_carga}\n"
                f"Dimensões (A x L x P): {self.altura} x {self.largura} x {self.profundidade} m\n"
                f"Volume da carga: {self.volume_carga()} m³\n"
                f"Eixos: {self.quantidade_eixos} com {self.carga_por_eixo} kg por eixo\n"
                f"Capacidade total: {self.capacidade_total_carga()} kg")

class Carga:
    def __init__(self, id, lote, deposito, peso_bruto, largura, altura, profundidade, peso_suportado, tipo_carga, descricao):
        self.id = id
        self.lote = lote
        self.deposito = deposito
        self.peso_bruto = peso_bruto
        self.tipo_carga = tipo_carga
        self.descricao = descricao
        self.peso_suportado = peso_suportado
        
        self._x = None
        self._y = None
        self._z = None

        if (largura >= 4 or profundidade >= 4):
            self.largura = largura + 0.025
            self.altura = altura + 0.025
            self.profundidade = profundidade + 0.025
        else:
            self.largura = largura
            self.altura = altura
            self.profundidade = profundidade

        def get_x(self):
            return self._x

        def get_y(self):
            return self._y

        def get_z(self):
            return self._z

        def set_x(self, x):
            self._x = x

        def set_y(self, y):
            self._y = y

        def set_z(self, z):
            self._z = z

        def volume(self):
            return self.largura * self.altura * self.profundidade

        def __str__(self):
            return (f"Carga ID: {self.id}, Lote: {self.lote}\n"
                    f"Depósito: {self.deposito}\n"
                    f"Tipo de carga: {self.tipo_carga}\n"
                    f"Peso bruto: {self.peso_bruto} kg | Peso suportado: {self.peso_suportado} kg\n"
                    f"Dimensões (A x L x P): {self.altura:.3f} x {self.largura:.3f} x {self.profundidade:.3f} m\n"
                    f"Volume: {self.volume():.3f} m³\n"
                    f"Posição (x, y, z): {self._x}, {self._y}, {self._z}\n"
                    f"Descrição: {self.descricao}")
