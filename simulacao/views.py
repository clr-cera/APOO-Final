from django.shortcuts import render
from .models import Simulacao
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

        heredograma_base64, estatisticas, img, simulacao = Simulacao.propagar(sequencias_genomas, numero_geracoes)

        return render(request, 'resultado_simulacao.html', {
            'simulacao': simulacao,
            'estatisticas': estatisticas,
            'grafico': img,
            'heredograma': f"data:image/png;base64,{heredograma_base64}"
        })

    return render(request, 'realizar_simulacao.html')



