# 3DBinPack_Foco

reformulação das classes
	atributos de status
	caminhao tem lista das cargas atribuidas
	atributos que carregam o desperdicio de carga(kg) e volume

variavel resultado trocada por uma lista de caminhoes em uso (mais facil de ler)

troca de penalidade por ultrapassar limite por impossibilidade de alocar

leitura de cargas trocadas de sequencial para aleatoria
	antes era lido de forma sequencial e decidido se seria alocado de acordo com a possibilidade
	agora é lido uma instancia aleatoria e decidido se sera alocado de acordo com a possibilidade

leitura de posições possiveis a partir dos itens ja alocados
	antes estava lendo as coordenadas de 1 em 1 valor

penalidade por afastamento do centro de gravidade do caminhao

leitura recursiva de cargas que estão em cima de outra carga
	caso ultrapasse o valor total, será penalizado
