import tkinter as tk
from tkinter import filedialog
from classes_cba import Caminhao, Carga
from data_loader import FileReader
from model_builder import AlgoritmoGenetico

if __name__ == "__main__":
    caminhoes = [
        Caminhao(id=1, nome="Truck A", tipo_carga="Geral", altura=2.5, largura=2.5, profundidade=10, carga_por_eixo=7000, quantidade_eixos=3),
        Caminhao(id=2, nome="Truck B", tipo_carga="Geral", altura=3, largura=2.5, profundidade=12, carga_por_eixo=8000, quantidade_eixos=4),
        Caminhao(id=3, nome="Truck C", tipo_carga="Geral", altura=2.8, largura=2.5, profundidade=11, carga_por_eixo=7500, quantidade_eixos=3)
    ]

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo Excel de cargas",
        filetypes=[("Planilhas do Excel", "*.xlsx")]
    )

    if not file_path:
        print("Nenhum arquivo selecionado. Encerrando.")
        exit()

    reader = FileReader(file_path)
    cargas = reader.ler_cargas()

    caminhoes_em_uso = AlgoritmoGenetico.execute(cargas, caminhoes, geracoes=20, populacao_tam=100)

    for caminhao in caminhoes_em_uso:
        print(f"\nCaminhão ID: {caminhao.id} | Status: {caminhao.status} | Volume total: {caminhao.volume():.2f} m³ | Volume que sobrou: {caminhao.sobra_volume:.2f} m³ | Carga total: {caminhao.capacidade_total_carga():.2f} | Carga que sobrou: {caminhao.sobra_carga:.2f}")
        for carga in caminhao.lista_cargas:
            print(f"    Carga ID: {carga.id} | Família: {carga.lote} | Volume: {carga.volume():.2f} m³ | Coordenadas: ({carga._x}, {carga._y}, {carga._z}) | peso que suporta: ({carga.peso_suportado} | peso em cima: ({carga.peso_cima} ")
