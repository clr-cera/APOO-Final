import base64
import json


from random import randint, shuffle, sample
from django.shortcuts import render
from .models import Simulacao


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

        heredograma_base64, estatisticas, img, simulacao = Simulacao.propagar(sequencias_genomas, numero_geracoes)

        # Passa estatísticas explicitamente para o template
        return render(request, 'resultado_simulacao.html', {
            'simulacao': simulacao,
            'estatisticas': estatisticas,  # Passa para o template
            'grafico': img,
            'heredograma': f"data:image/png;base64,{heredograma_base64}"
        })

    return render(request, 'realizar_simulacao.html')

def listar_simulacoes(request):
    """Lista todas as simulações salvas no banco de dados."""
    simulacoes = Simulacao.objects.all()  # Busca todas as simulações
    return render(request, 'listar_simulacoes.html', {'simulacoes': simulacoes})

def visualizar_simulacao(request, simulacao_id):
    """Visualiza os detalhes de uma simulação específica."""
    simulacao = Simulacao.objects.get(id=simulacao_id)

    # Recria o gráfico
    grafico = Simulacao.recriar_grafico(simulacao.grafico_dados)

    # Recria o heredograma
    heredograma_dot = Simulacao.recriar_heredograma(simulacao.heredograma_dados)
    heredograma_dot.format = 'png'
    heredograma_img_data = heredograma_dot.pipe()
    heredograma_base64 = base64.b64encode(heredograma_img_data).decode('utf-8')

    # Garante que as estatísticas estão desserializadas
    if isinstance(simulacao.estatisticas, str):
        estatisticas = json.loads(simulacao.estatisticas)
    else:
        estatisticas = simulacao.estatisticas

    return render(request, 'visualizar_simulacao.html', {
        'simulacao': simulacao,
        'estatisticas': estatisticas,
        'grafico': grafico,
        'heredograma': f"data:image/png;base64,{heredograma_base64}"
    })