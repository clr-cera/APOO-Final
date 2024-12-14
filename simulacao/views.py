from django.shortcuts import render
from .models import Simulacao
from itertools import product

import matplotlib.pyplot as plt
import graphviz
import io
import base64

from random import randint, shuffle, sample

def realizar_simulacao(request):
    """Função principal que realiza a simulação genética."""
    if request.method == 'POST':
        # Entrada de dados do formulário
        numero_geracoes = int(request.POST.get('numero_geracoes'))
        sequencias_genomas = request.POST.getlist('genomas')

        # Validação das entradas
        if numero_geracoes < 1 or len(sequencias_genomas) < 2:
            return render(request, 'realizar_simulacao.html', {
                'erro': 'Informe o número de gerações e ao menos 2 genomas.'
            })

        # Inicia a simulação
        geracoes = [sequencias_genomas]
        for _ in range(1, numero_geracoes):
            nova_geracao = []
            pais = geracoes[-1]
            for i in range(0, len(pais), 2):
                if i + 1 < len(pais):
                    pai, mae = pais[i], pais[i + 1]
                    filhos = gerar_combinacoes(pai, mae)
                    nova_geracao.extend(filhos)
            if not nova_geracao:  # Se não houver filhos válidos, interrompe o loop
                break
            geracoes.append(nova_geracao)

        # Calcula estatísticas
        estatisticas = calcular_estatisticas(geracoes)

        # Salva a simulação no banco de dados
        simulacao = Simulacao.objects.create(
            numero_geracoes=numero_geracoes,
            resultado="\n".join([f"Geração {i+1}: {', '.join(geracao)}" for i, geracao in enumerate(geracoes)]),
            estatisticas=str(estatisticas)
        )

        # Gera o gráfico das frequências
        img = gerar_grafico(estatisticas)
        dot = criar_heredograma_genetico(geracoes)
        dot.format = 'png'
        img_data = dot.pipe()
        heredograma_base64 = base64.b64encode(img_data).decode('utf-8')

        return render(request, 'resultado_simulacao.html', {
            'simulacao': simulacao,
            'estatisticas': estatisticas,
            'grafico': img,
            'heredograma': f"data:image/png;base64,{heredograma_base64}"
        })

    return render(request, 'realizar_simulacao.html')




def gerar_combinacoes(pai, mae):
    """Gera combinações válidas de genes entre dois genomas."""
    filhos = []
    genes_pai = [pai[i:i + 2] for i in range(0, len(pai), 2)]  # Divide em pares de alelos
    genes_mae = [mae[i:i + 2] for i in range(0, len(mae), 2)]

    for i in range(4):
        for j in range(len(genes_pai)):
            l = list(genes_pai[j])
            shuffle(l)
            genes_pai[j] = ''.join(l)

        for j in range(len(genes_mae)):
            l = list(genes_mae[j])
            shuffle(l)
            genes_mae[j] = ''.join(l)

        filho = []
        for j in range(len(genes_pai)):
            filho.append(''.join(genes_pai[j][0] + genes_mae[j][0]))

        filho = ''.join(filho)

        filhos.append(filho)

    return filhos  # Remove duplicatas


def calcular_estatisticas(geracoes):
    """Calcula a frequência em porcentagens dos alelos em todas as gerações."""
    estatisticas = []
    for i, geracao in enumerate(geracoes):
        frequencia = {}
        total_alelos = 0

        # Conta a frequência dos alelos
        for genoma in geracao:
            for alelo in genoma:
                frequencia[alelo] = frequencia.get(alelo, 0) + 1
                total_alelos += 1  # Soma todos os alelos na geração

        # Converte para porcentagem
        porcentagem = {alelo: (freq / total_alelos) * 100 for alelo, freq in frequencia.items()}
        estatisticas.append({'Geração': i + 1, 'Porcentagem': porcentagem})
    return estatisticas



def gerar_grafico(estatisticas):
    """Gera um gráfico das porcentagens dos alelos ao longo das gerações."""
    plt.figure(figsize=(10, 6))

    # Configurar os dados do gráfico
    geracoes = [f"Geração {dados['Geração']}" for dados in estatisticas]
    frequencias = {}

    # Inicializa com frequências
    for dados in estatisticas:
        for alelo in dados['Porcentagem']:
            if alelo not in frequencias:
                frequencias[alelo] = [0] * len(estatisticas)

    # Preenche as porcentagens reais
    for i, dados in enumerate(estatisticas):
        for alelo, porcentagem in dados['Porcentagem'].items():
            frequencias[alelo][i] = porcentagem

    # Plota as frequências em porcentagem
    for idx, (alelo, freq) in enumerate(frequencias.items()):
        if any(freq):  # Plota apenas se houver valores válidos
            linestyle = '--' if idx % 2 == 0 else '-'
            marker = 'o' if idx % 2 == 0 else 's'
            plt.plot(geracoes, freq, label=f"{alelo}", linestyle=linestyle, marker=marker)

    # Configurações do gráfico
    plt.title("Porcentagem de Frequência Genética por Geração")
    plt.xlabel("Gerações")
    plt.ylabel("Porcentagem (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Salvar imagem em base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()  # Fecha a figura para liberar memória
    return f"data:image/png;base64,{img}"


def criar_heredograma_genetico(geracoes, titulo="Heredograma Genético"):
    """
    Cria um heredograma a partir das gerações da simulação genética.

    Parâmetros:
    - geracoes: Lista de gerações de genomas
    - titulo: Título do heredograma (opcional)

    Retorna:
    - Objeto graphviz.Digraph representando o heredograma
    """
    # Cria um novo grafo direcionado
    dot = graphviz.Digraph(comment=titulo, engine='dot')
    dot.attr(rankdir='TB')  # Layout de cima para baixo
    dot.attr('node', shape='box')

    # Define o título do grafo
    dot.attr(label=titulo)
    dot.attr(labelloc='t')

    # Dicionário para mapear nós de cada geração
    node_map = {}

    # Itera sobre as gerações
    for gen_index, geracao in enumerate(geracoes):
        # Cria um subgrafo para manter a geração no mesmo nível
        with dot.subgraph() as gen_subgraph:
            gen_subgraph.attr(rank='same')

            # Processa cada genoma na geração
            for genome_index, genoma in enumerate(geracao):
                # Cria um identificador único para o nó
                node_id = f'gen{gen_index}_genome{genome_index}'

                # Cria o nó com o genoma como label
                gen_subgraph.node(node_id, label=genoma,
                                  style='filled',
                                  fillcolor='lightblue')

                # Armazena o ID do nó para possíveis conexões
                if gen_index not in node_map:
                    node_map[gen_index] = []
                node_map[gen_index].append(node_id)

                # Conecta com a geração anterior, se existir
                if gen_index > 0:
                    # Tenta conectar com os pais prováveis
                    # Assume uma relação de parentesco simples
                    parent_index = (genome_index // 4) *2
                    if parent_index < len(node_map[gen_index - 1]):
                        parent_id = node_map[gen_index - 1][parent_index]
                        parent_id_2 = node_map[gen_index - 1][parent_index+1]
                        dot.edge(parent_id, node_id)
                        dot.edge(parent_id_2, node_id)
    return dot