````markdown
# Projeto: Comunicação Assíncrona entre NodeJS e Flask

## 📄 Sobre o Projeto

Este projeto demonstra a comunicação entre uma aplicação **NodeJS (cliente)** e uma aplicação **Flask/Python (servidor)** para executar uma tarefa de longa duração.  
O cliente solicita a execução de um script de web scraping, e o servidor o processa em segundo plano, gerando um arquivo `.csv` como resultado, sem bloquear a aplicação cliente.

---

## 🏗️ Arquitetura

A comunicação é feita através de uma API REST e segue um padrão de **tarefa assíncrona com Polling**:

1. **NodeJS** envia um `POST` para `/iniciar-tarefa`.
2. **Flask** inicia a tarefa em uma thread separada e responde imediatamente com um `task_id`.
3. **NodeJS** entra em um loop, enviando requisições `GET` para `/status/<task_id>` a cada 5 segundos para verificar o progresso.
4. Quando o status muda para `concluido`, **Flask** retorna uma URL para download do arquivo gerado.

```plaintext
+------------------+         (1. Iniciar)          +-----------------+
|  Cliente NodeJS  |  ------ POST /iniciar ---->  |  Servidor Flask |
|                  |                               | (Inicia Thread) |
|                  |  <---- (2. ID da Tarefa) --  |                 |
+------------------+                               +-----------------+
        |
        | (3. Loop de Polling: GET /status/<id>)
        |
        +------------------------------------------> (4. Retorna Status)
        |
        | <------------------------------------------ {status: 'processando'}
        |
        | (Quando finalizado)
        |
        | <------------------------------------------ {status: 'concluido', resultado: {url_download}}
````

---

## 🛠️ Tecnologias Utilizadas

### Backend (Servidor):

* Python 3
* Flask
* Requests
* BeautifulSoup4

### Frontend (Cliente):

* Node.js
* Axios

---

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter as seguintes ferramentas instaladas em sua máquina:

* [Python](https://www.python.org/) (versão **3.6** ou superior)
* [Node.js](https://nodejs.org/) (versão **14** ou superior)

---

## 🚀 Como Executar o Projeto

Você precisará de **dois terminais** abertos simultaneamente.

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/Vinicius203/trabalho2_gerencia_de_redes
cd trabalho2_gerencia_de_redes
```

---

### 2️⃣ Configurar e Rodar o Servidor Flask (Terminal 1)

```bash
# Navegue até a pasta do servidor
cd servidor_flask

# (Opcional, mas recomendado) Crie e ative um ambiente virtual
python -m venv venv

# Ativar ambiente:
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install Flask requests beautifulsoup4

# Rodar o servidor
python app.py
```

O terminal deverá exibir uma mensagem indicando que o servidor está rodando em:
`http://0.0.0.0:5000/` ou `http://localhost:5000/`.

Deixe este terminal aberto.

---

### 3️⃣ Configurar e Rodar o Cliente NodeJS (Terminal 2)

```bash
# Abrir um NOVO terminal e navegar até a pasta do cliente
cd cliente_nodejs

# Instalar dependências
npm install

# Executar o cliente
node index.js
```

---

## ✅ Funcionamento Esperado

No **Terminal 2 (NodeJS)**, você verá:

```
🚀 1. Solicitando o início da tarefa de scraping para gerar o CSV...
✅ Tarefa iniciada com ID: [um-id-aleatorio]

🔄 2. Verificando o status da tarefa a cada 5 segundos...
   - Status atual: processando
   - Status atual: processando
   ...
```

Ao mesmo tempo, no **Terminal 1 (Flask)**, verá os logs do scraping em andamento.

Após cerca de **40-50 segundos**, o Terminal 2 exibirá:

```
🏁 3. Tarefa finalizada!
✅ Sucesso!
   - Mensagem: 400 livros foram salvos com sucesso!
   - Arquivo: relatorio_livros_[um-id-aleatorio].csv
   - Baixe seu relatório aqui: http://localhost:5000/download/relatorio_livros_[um-id-aleatorio].csv
```
