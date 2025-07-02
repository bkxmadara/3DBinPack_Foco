from classesCBA import *
from data_Loader import *
from model_Builder import algoritmo_genetico

def main():
    # Carrega os dados
    read_data()

    # Executa o algoritmo genético
    resultado = algoritmo_genetico(cargas, caminhoes, geracoes=30, populacao_tam=20)

    # Mostra o resultado final da melhor solução
    for caminhao_id, lista in resultado.items():
        print(f"\nCaminhão ID: {caminhao_id}")
        for item in lista:
            print(f"    Carga ID: {item['id']} | Coordenada: {item['coordenada']}")

if __name__ == "__main__":
    main()
