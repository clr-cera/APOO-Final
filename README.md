Aqui está a versão atualizada do texto com as informações sobre **migrações do banco de dados** para garantir que o projeto funcione corretamente ao ser inicializado.

---

# Sistema de Simulação Genética
Projeto em Django para a simulação de heranças genéticas.

---

## Requisitos do Sistema
Para rodar o projeto corretamente, instale os seguintes itens:

1. **Python 3.12**  
   - O projeto foi desenvolvido na versão 3.12 do Python.  
   - Baixe e instale o Python aqui: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Graphviz**  
   - Necessário para gerar o **heredograma** no sistema.

   ### Instalação do Graphviz
   - **Windows**:  
     1. Baixe o instalador aqui: [Graphviz Downloads](https://graphviz.org/download/).  
     2. Durante a instalação, **marque a opção de adicionar o Graphviz ao PATH**.  
     3. Verifique a instalação com o comando no terminal:  
        ```bash
        dot -V
        ```
   - **Linux (Ubuntu/Debian)**:  
     Instale via terminal:
     ```bash
     sudo apt-get install graphviz
     ```
     Verifique a instalação:
     ```bash
     dot -V
     ```

3. **Matplotlib**  
   - Biblioteca necessária para gerar os gráficos de frequência genética.

   ### Instalação do Matplotlib
   No terminal, execute o seguinte comando:
   ```bash
   python3 -m pip install matplotlib
   ```

---

## Instalando as Dependências do Projeto
As dependências estão listadas no arquivo `requirements.txt`. Para instalá-las, siga um dos métodos abaixo:

### Método 1: Instalação Manual (pip)
1. Abra o terminal e navegue até a pasta raiz do projeto (onde está o arquivo `requirements.txt`).
2. Execute o seguinte comando:
   ```bash
   pip install -r requirements.txt
   ```

### Método 2: Usando `uv` (para desenvolvimento)
1. Instale o pacote **uv**:
   ```bash
   pip install uv
   ```
2. Execute o projeto e instale as dependências automaticamente com:
   ```bash
   uv run manage.py runserver
   ```

---

## Migrando o Banco de Dados
O projeto Django utiliza um banco de dados **SQLite** por padrão, mas é possível configurar outro banco de dados como PostgreSQL ou MySQL.

### Criação e Aplicação das Migrações
Antes de rodar o projeto pela primeira vez, aplique as migrações do banco de dados para criar as tabelas necessárias:

1. No terminal, navegue até o diretório principal do projeto (onde está o arquivo `manage.py`).
2. Execute os seguintes comandos:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

### Criar um Superusuário (opcional)
Para acessar o painel de administração do Django, crie um superusuário com o comando abaixo:
```bash
python3 manage.py createsuperuser
```
Siga as instruções para configurar o usuário e senha.

---

## Rodando o Projeto Django

### Passos para rodar o projeto
1. No terminal, navegue até o diretório principal do projeto (onde está o arquivo `manage.py`).
2. Execute o servidor local do Django com o comando:
   ```bash
   python3 manage.py runserver
   ```
3. Acesse o projeto no navegador usando o endereço:
   ```
   http://127.0.0.1:8000/
   ```

### Possíveis Problemas
- Caso algum erro relacionado ao **Graphviz** ou **Matplotlib** ocorra, verifique se foram instalados corretamente e adicionados ao PATH.
- Para o **Graphviz**, garanta que o comando `dot -V` retorna a versão corretamente.

---

## Resumo dos Comandos Principais

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

### Criação do Banco de Dados
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
### Rodar o Projeto
```bash
python3 manage.py runserver
```

### Verificar o Graphviz
```bash
dot -V
```

---

Agora o projeto está pronto para ser rodado! Caso surjam dúvidas ou problemas, siga novamente as etapas acima ou verifique as configurações de ambiente. 🚀
