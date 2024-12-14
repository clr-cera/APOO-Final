from django.shortcuts import render
from .models import Simulacao
from itertools import product

import matplotlib.pyplot as plt
import io
import base64

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
            nova_geracao = list(set(nova_geracao))  # Remove duplicatas
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

        return render(request, 'resultado_simulacao.html', {
            'simulacao': simulacao,
            'estatisticas': estatisticas,
            'grafico': img
        })

    return render(request, 'realizar_simulacao.html')




def gerar_combinacoes(pai, mae):
    """Gera combinações válidas de genes entre dois genomas."""
    genes_pai = [pai[i:i + 2] for i in range(0, len(pai), 2)]  # Divide em pares de alelos
    genes_mae = [mae[i:i + 2] for i in range(0, len(mae), 2)]

    # Gera todas as combinações válidas para cada par
    combinacoes = product(*[
        [a1 + a2 for a1 in sorted(set(pai_)) for a2 in sorted(set(mae_))]
        for pai_, mae_ in zip(genes_pai, genes_mae)
    ])

    filhos = [''.join(filho) for filho in combinacoes]
    return sorted(set(filhos))  # Remove duplicatas


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