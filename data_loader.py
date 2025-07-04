import pandas as pd
import unicodedata
from classes_cba import Caminhao, Carga

caminhoes = [
    Caminhao(id=1, nome="Truck A", tipo_carga="Geral", altura=2.5, largura=2.5, profundidade=10, carga_por_eixo=7000, quantidade_eixos=3),
    Caminhao(id=2, nome="Truck B", tipo_carga="Geral", altura=3, largura=2.5, profundidade=12, carga_por_eixo=8000, quantidade_eixos=4),
    Caminhao(id=3, nome="Truck C", tipo_carga="Geral", altura=2.8, largura=2.5, profundidade=11, carga_por_eixo=7500, quantidade_eixos=3)
]

# Função auxiliar
def str_para_float(valor):
    try:
        return float(str(valor).replace(',', '.'))
    except Exception:
        return 0.0

def normalizar_nome(coluna):
    # Remove acentos, coloca em caixa baixa, remove espaços extras e substitui por _
    coluna = unicodedata.normalize('NFKD', coluna).encode('ASCII', 'ignore').decode('utf-8')
    return coluna.strip().lower().replace(" ", "_")

class FileReader:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def ler_cargas(self):
        df = pd.read_excel(self.caminho_arquivo, dtype=str)

        # Padroniza os nomes das colunas
        df.columns = [normalizar_nome(col) for col in df.columns]

        # Define os nomes esperados
        colunas_esperadas = [
            "familia", "lote", "dep.", "ud", "peso_bruto_ud", "altura",
            "largura", "compr", "peso_sup.", "texto_breve_de_material"
        ]

        # Padroniza os nomes esperados também
        colunas_esperadas = [normalizar_nome(c) for c in colunas_esperadas]

        # Valida se todas estão presentes
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                raise ValueError(f"Coluna obrigatória '{coluna}' não encontrada no arquivo.")

        cargas = []

        for _, row in df.iterrows():
            carga = Carga(
                id=row["ud"],
                lote=row["lote"],
                deposito=row["dep."],  # já está padronizado como "dep."
                peso_bruto=str_para_float(row["peso_bruto_ud"]),
                altura=str_para_float(row["altura"]),
                largura=str_para_float(row["largura"]),
                profundidade=str_para_float(row["compr"]),  # "compr." = profundidade
                peso_suportado=str_para_float(row["peso_sup."]),
                tipo_carga=row["familia"],  # usa "familia" como tipo_carga
                descricao=row["texto_breve_de_material"]
            )
            cargas.append(carga)

        return cargas

