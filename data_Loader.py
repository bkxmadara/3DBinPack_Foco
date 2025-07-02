import pandas as pd
from classesCBA import *

cargas = []

caminhoes = [
    Caminhao(id=1, nome="Truck A", tipo_carga="Geral", altura=2.5, largura=2.5, profundidade=10, carga_por_eixo=7000, quantidade_eixos=3),
    Caminhao(id=2, nome="Truck B", tipo_carga="Geral", altura=3, largura=2.5, profundidade=12, carga_por_eixo=8000, quantidade_eixos=4),
    Caminhao(id=3, nome="Truck C", tipo_carga="Geral", altura=2.8, largura=2.5, profundidade=11, carga_por_eixo=7500, quantidade_eixos=3)
    ]

def read_data():
    df = pd.read_excel('UD x Dimenções (002).xlsx', dtype=str)

    def str_para_float(valor):
        try:
            return float(valor.replace(',', '.'))
        except:
            return 0.0

    for _, row in df.iterrows():
        carga = Carga(
            id=row.iloc[6],
            lote=row.iloc[3],
            deposito=row.iloc[5],
            peso_bruto=str_para_float(row.iloc[7]),
            altura=str_para_float(row.iloc[8]),
            largura=str_para_float(row.iloc[9]),
            profundidade=str_para_float(row.iloc[10]),
            peso_suportado=str_para_float(row.iloc[15]),
            tipo_carga=row.iloc[0],
            descricao=row.iloc[2]
        )
        cargas.append(carga)

    