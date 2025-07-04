import tkinter as tk
from tkinter import filedialog
from classes_cba import Caminhao, Carga
from data_loader import FileReader
from model_Builder import AlgoritmoGenetico

if __name__ == "__main__":
    # Caminhões disponíveis
    caminhoes = [
        Caminhao(id=1, nome="Truck A", tipo_carga="Geral", altura=2.5, largura=2.5, profundidade=10, carga_por_eixo=7000, quantidade_eixos=3),
        Caminhao(id=2, nome="Truck B", tipo_carga="Geral", altura=3, largura=2.5, profundidade=12, carga_por_eixo=8000, quantidade_eixos=4),
        Caminhao(id=3, nome="Truck C", tipo_carga="Geral", altura=2.8, largura=2.5, profundidade=11, carga_por_eixo=7500, quantidade_eixos=3)
    ]

    # Interface file reader
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo Excel de cargas",
        filetypes=[("Planilhas do Excel", "*.xlsx")]
    )

    if not file_path:
        print("Nenhum arquivo selecionado. Encerrando.")
        exit()

    # Carrega as cargas a partir do arquivo selecionado
    reader = FileReader(file_path)
    cargas = reader.ler_cargas()

    # Execução do algorítmo
    resultado = AlgoritmoGenetico.execute(cargas, caminhoes, geracoes=30, populacao_tam=20)

    # Output
    for caminhao_id, lista in resultado.items():
        print(f"\nCaminhão ID: {caminhao_id}")
        for item in lista:
            print(f"    Carga ID: {item['id']} | Coordenada: {item['coordenada']}")
