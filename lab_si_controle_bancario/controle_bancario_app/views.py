from datetime import datetime
import random, time
from http import client
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone

#importações dos modelos (classes) necessários para o UC Abrir Conta
from controle_bancario_app.models import contaComum, PessoaFisica, movimento

#a seguir são definidas as funções que possuem lógica dos controladores no padrão MVC

# função default da interface inicial do sistema 'home'
def home(request):
    #método executado quando o usuário está na interface inicial do sistema. 
    #Envia-se uma solicitação de renderização da interface home.html
    return render(request, "controle_bancario/home.html")

#função consultarCliente
def consultarCliente(request):
     # verifica se a solicitação (request) usa o metodo POST de envio de dados
    if request.method == "POST":
         #captura o valor da variável cpfPessoa enviada pela interface e o aloca para a variável local cpf    
        cpf = request.POST['cpfPessoa']
        
        #chama a função consultarCpfCliente() com parâmetro de entrada o número de cpf
        cliente = consultarCpfCliente(cpf)
        # o método retorna um objeto do tipo pessoaFisica 
        # o objeto retornado contem os dados do cliente com o cpf enviado como parâmetro
        # o objeto é alocado à variável local cliente

        #caso tenha achado um cliente com esse cpf no banco de dados ...
        if(cliente):
            #retorna o cpf do cliente cujos dados vão ser atualizados para a interface de usuário  'atualizarDadosCliente.html'
            return redirect('atualizarDadosCliente', cpfPessoa = cliente.cpfPessoa)
        #caso o cliente não esteja registrado no banco de dados
        else:
            #redireciona para a interface de usuário "abrirConta.html" 
            return redirect("abrirConta")
        
    #quando a solicitação (request) usa o método GET é solicitada a renderização da interface consultarCliente.html
    else:
        return render(request, "controle_bancario/consultarCliente.html")

#função para consultar se o cpf informado pertence a um cliente já registrado no banco de dados 
def consultarCpfCliente(cpf):
    #chamada do método consultarCpf() da classe PessoaFisica, com parâmetro de entrada o número do cpf
    #o método retorna um objeto do tipo pessoaFisica que é alocado à variável local cliente
    cliente = PessoaFisica.consultarCpf(cpf)
    #confirma se o objeto não está vazio (ou seja o cliente existe)
    if(cliente):
       #retornar o objeto cliente do tipo pessoaFisica
       return cliente
    #se o cliente não existe no banco de dados...
    else:
        return False

#função para atualização dos dados de um cliente
#a função recebe como entrada a requisição (request) da interface de usuário
#também, recebe como entrada (opcional) o cpf do cliente cuja informação vai ser atualizada
def atualizarDadosCliente(request, cpfPessoa = None):
    # verifica se a solicitação (request) usa o metodo POST de envio de dados
    if request.method == "POST":        
        #consulta no banco a existencia do cliente e recebe como retorno o objeto do tipo pessoaFisica com os dados do cliente
        cliente = consultarCpfCliente(cpfPessoa)
        #pega os dados enviados pela interface de usuário na solicitação e os aloca no objeto cliente do tipo pessoaFisica
        cliente.nomePessoa = request.POST['nomePessoa']
        cliente.enderecoPessoa = request.POST['enderecoPessoa']
        cliente.cepPessoa = request.POST['cepPessoa']
        cliente.telefonePessoa = request.POST['telefonePessoa']
        cliente.rendaPessoa = request.POST['rendaPessoa']
        
        #chama o método atualizarPessoa() da classe pessoaFisica.
        #o método retorna o objeto com as informações atualizadas
        res = cliente.atualizarPessoa()

        #preparação da mensagem de retorno à interface de usuário
        if res:
            mensagem = "Os dados do cliente foram atualizados!"
            
        else:
            mensagem = "Erro. Os dados do cliente não foram atualizados!"
        
        context = {
            "resposta": mensagem,
            "cliente": res
        }
        #envia à interface de usuário atualizarDadosCliente uma solicitação de renderização da mensagem
        return render(request,"controle_bancario/atualizarDadosCliente.html",context)
    
    #verifica se a solicitação (request) usa o metodo GET de envio de dados
    if request.method == 'GET':
        cliente = consultarCpfCliente(cpfPessoa)
        context={ "cliente": cliente}
        return render(request, "controle_bancario/atualizarDadosCliente.html",context)

    #caso a solicitação não seja com POST nem GET
    # a solicitação (request) não contém dados 
    # dessa forma será mostrado para o usuario final o form de abertura de conta que está em abrirConta.html
    return render(request, "controle_bancario/atualizarDadosCliente.html")


def abrirConta(request):
    # verifica se a solicitação (request) usa o metodo POST de envio de dados
    if request.method == "POST":        
        
            #chamada da função registrarCliente e passa como parâmetro os dados enviados no formulário
            cliente = registrarCliente(request)
        
            # - chama a função criarConta para realizar a abertura de conta para o cliente
            conta = criarConta(request,cliente)

            # - chama a função para emitir o cartão da conta
            emissao = emitirCartao(cliente,conta)

            # - redireciona para a interface de realizar depósito
            return redirect("realizarDeposito")
    else:  
        # a solicitação (request) não contém dados 
        # dessa forma será mostrado para o usuario final o form para abertura de conta que está em abrirConta.html
        return render(request, "controle_bancario/abrirConta.html")

def registrarCliente(request):
     #criação do cliente como instância da classe PessoaFisica definida no modelo de classes
     cliente = PessoaFisica(nomePessoa = request.POST['nomePessoa'], enderecoPessoa = request.POST['enderecoPessoa'], cepPessoa = request.POST['cepPessoa'], telefonePessoa = request.POST['telefonePessoa'], rendaPessoa = request.POST['rendaPessoa'], situacaoPessoa = 1, cpfPessoa = request.POST['cpfPessoa'], rgPessoa = request.POST['rgPessoa'], dataNascimento = request.POST['dataNascimento'])
     #registro do cliente no banco fazendo uso do método registrarPessoa() definido na classe PessoaFisica no modelo de classes
     cliente.registrarPessoa()
     return cliente

#criar conta
def criarConta(request,cliente):
    #dados da nova contaComum
        numeroConta = str(random.randint(1,500))
        aberturaConta = datetime.today().strftime('%Y-%m-%d')
        situacaoConta = '1'
        senhaConta = request.POST['senhaConta']  #to-do: implementar a encriptação da senha
        saldoConta = '0'
        #criação do objeto do tipo contaComum
        conta = contaComum(idCliente = cliente, numeroConta = numeroConta, aberturaConta = aberturaConta, situacaoConta = situacaoConta, senhaConta = senhaConta, saldoConta = saldoConta)
        #registro da nova conta no banco fazendo uso do método abrirConta() definido na classe contaComum no modelo de classes
        conta.abrirConta()
        return conta.numeroConta

#função para buscar se uma conta existe ou não
def consultarConta(numeroConta):
    #chama o metodo consultarConta() da classe contaComum com parâmetro de entrada numeroConta. O método retorna um objeto do tipo contaComum
    conta = contaComum.consultarConta(numeroConta)
    #caso seja encontrado um registro no banco com esse numero de conta
    if(conta):
       #retorna o objeto conta, instância da classe contaComum
       return conta
    #caso contrário ...
    else:
        return False

#função para realizar deposito numa conta
def realizarDeposito(request):
    # verifica se a solicitação (request) usa o metodo POST de envio de dados
    if request.method == "POST":    
        #captura o valor da variável numeroConta enviada pela interface e o aloca para a variável local numeroConta    
        numeroConta = request.POST['numeroConta']
        #chama o metodo consultarConta() da classe contaComum com parâmetro de entrada numeroConta. O método retorna um objeto do tipo contaComum
        conta = consultarConta(numeroConta)
        #caso seja encontrado um registro no banco com esse numero de conta
        if conta:
            #captura o valor da variável valorMovimento enviada pela interface e o aloca para a variável local valor    
            valor = int(request.POST['valorMovimento'])
            #captura o valor da variável cpfPessoa enviada pela interface e o aloca para a variável local cpf
            cpf = request.POST['cpfPessoa']
            #chama a função consultarCpfCliente() com parâmetro de entrada cpf. A função retorna um objeto do tipo pessoaFisica que é alocado à variável local cliente
            cliente = consultarCpfCliente(cpf)
            
            #criação do objeto do tipo movimento
            mov = movimento(idConta=conta, tipoMovimento = 1, valorMovimento = valor)
            #registrar os atributos da classe movimento no banco
            res1 = mov.registrarMovimento()
            #atualizar saldo conta. Chama o método atualizarSaldo() da classe contaComum com parâmetro de entrada valor
            res2 = conta.atualizarSaldo(valor)

            if res1 and res2:
                #formatação da mensagem de retorno. Concatenação de strings ...
                mensagem = f"Operação Sucedida! Depósito realizado para: {cliente.nomePessoa} na conta: {conta.numeroConta} por um valor de: {mov.valorMovimento} na data: {mov.dataMovimento}"
            else:
                mensagem = "Não foi possível fazer o depósito."    

            #preparação para o envio de variáveis de volta para a interface de usuário
            context = {
            "resposta": mensagem
            }
            #o retorno é uma mensagem de renderização enviada à interface realizarDeposito.html
            return render(request,"controle_bancario/realizarDeposito.html",context)
        else:
            context = {
                "resposta": 'Número de conta não existe'
            }
            #retorna a resposta para ser renderizada pela interface realizarDeposito.html
            return render(request,"controle_bancario/realizarDeposito.html",context)
    else:  
        # a solicitação (request) não contém dados 
        # dessa forma será mostrado para o usuario final o form de abertura de conta que está em realizarDeposito.html
        return render(request, "controle_bancario/realizarDeposito.html")
    

########################################################
## APARTIR DAQUI AS FUNÇÕES NÃO ESTÃO IMPLEMENTADAS 

#emitir cartao
def emitirCartao(cliente,conta):
    #realizar a emissão do cartao #To-do
    return 0

def emitirExtrato(request):
    return render(request, "controle_bancario/emitirExtrato.html")

def emitirSaldo(request):
    return render(request, "controle_bancario/emitirSaldo.html")

def encerrarConta(request):
    return render(request, "controle_bancario/encerrarConta.html")


def realizarSaque(request):
    return render(request, "controle_bancario/realizarSaque.html")

def gerenciarClientes(request):
    return render(request, "controle_bancario/gerenciarClientes.html")


    



