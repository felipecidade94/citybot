# CityBot 🤖 - Assistente Multifuncional com IA

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![GitHub](https://img.shields.io/badge/License-MIT-green)

## 📌 Visão Geral
O **CityBot** é um assistente virtual inteligente que combina:
- Chatbot baseado em **LLM (Llama 3 via Groq API)**
- Processamento de **documentos (PDFs, sites, vídeos)**
- **OCR** para extração de texto de imagens
- Armazenamento em banco de dados **SQLite**

## 🚀 Recursos Principais

### 💬 Chat Inteligente
- Memória de conversa persistente
- Respostas contextualizadas
- Suporte a multi-turn conversations

### 📂 Processamento de Documentos
| Tipo        | Biblioteca       | Funcionalidade               |
|-------------|-----------------|------------------------------|
| PDF         | PyPDFLoader     | Extração e análise de texto  |
| Sites Web   | WebBaseLoader   | Raspagem de conteúdo         |
| Vídeos      | YoutubeLoader   | Transcrição automática       |

### 👁️ OCR Avançado
- Suporte a 10 idiomas
- Saída em TXT ou DOCX
- Integração com OpenCV e Tesseract

## 🛠️ Configuração

### Pré-requisitos
```bash
pip install -r requirements.txt
```

## 🏁 Como Usar

### Configure sua API Key
```python
api_key = 'sua_chave_groq_aqui'
os.environ['GROQ_API_KEY'] = api_key
```

### Execute o bot
python citybot.py

### Menu Interativo
1. Conversar
2. Processar site
3. Analisar vídeo
4. Ler PDF
5. OCR de imagem
6. Sair

## 📊 Estrutura do Banco de Dados

O CityBot utiliza um banco de dados SQLite (`citybot.db`) com a seguinte estrutura:

### Tabela `users`
Armazena informações dos usuários:
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preferences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🌟 Exemplo de Uso
```python
# Processando um PDF
bot = CityBot(api_key, 'llama-3.1-8b-instant')
pdf_text = bot.carrega_pdf()
resposta = bot.resposta_bot([('user', 'Resuma este PDF')], pdf_text)
```
