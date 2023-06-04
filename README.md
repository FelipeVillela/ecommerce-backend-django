# ecommerce-backend-django
Projeto criado para estudos. Servidor para um ecommerce utilizando django rest framework

## Utilização
Siga os passos abaixo para configurar e executar o projeto.
### Pré-requisitos
Python 3.8 ou superior
Pip (gerenciador de pacotes do Python)
Ambiente virtual (recomendado)

### Passo 1: Configuração do ambiente virtual
Abra o terminal e navegue até o diretório raiz do projeto.

Crie um ambiente virtual executando o seguinte comando:

```
python3 -m venv nome_do_ambiente
```
Substitua nome_do_ambiente pelo nome desejado para o ambiente virtual.
É extremamente recomendado utilizar o nome "venv".
Isso ocorre porque o nome "venv" está incluído no arquivo .gitignore, garantindo que o ambiente virtual seja ignorado ao realizar um commit.
Essa prática evita a inclusão de arquivos desnecessários no repositório.

Caso não possua o pacote venv, instale usando
```
pip3 install virtualenv
```

Ative o ambiente virtual:

No Windows:

```
nome_do_ambiente\Scripts\activate
```
No Linux ou macOS:

```
source nome_do_ambiente/bin/activate
```

### Passo 2: Instalação dos requisitos
Com o ambiente virtual ativado, execute o seguinte comando para instalar as dependências do projeto:

```
pip3 install -r requirements.txt
```
Isso instalará todas as bibliotecas e pacotes necessários para o projeto.

### Passo 3: Configuração do arquivo .env
No diretório raiz do projeto, duplique o arquivo .env-example e renomeie para apenas .env

Abra o arquivo .env em um editor de texto.

Adicione as configurações necessárias ao arquivo .env, como chaves de API, informações de banco de dados e outras configurações específicas do projeto.

### Passo 4: Executando o projeto
Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando para iniciar o servidor de desenvolvimento:

```
python manage.py runserver
```
O servidor de desenvolvimento será iniciado e você poderá acessar o projeto no navegador em http://localhost:8000/.

