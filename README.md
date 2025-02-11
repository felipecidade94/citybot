# CityBot - Chatbot Multifuncional

CityBot é um assistente virtual inteligente desenvolvido para interagir com os usuários em uma ampla variedade de tópicos e realizar diversas tarefas, como analisar conteúdo de sites, extrair informações de PDFs, vídeos do YouTube e até mesmo realizar OCR (Reconhecimento Óptico de Caracteres) em imagens. O chatbot também possui memória de conversas, permitindo que ele se lembre das interações anteriores mesmo após o programa ser fechado.

## Funcionalidades Principais

- **Conversação Amigável**: CityBot pode conversar sobre qualquer assunto e responder perguntas baseadas nas informações fornecidas pelo usuário.
  
- **Análise de Sites**: Insira a URL de um site, e o bot poderá extrair informações e responder perguntas relacionadas ao conteúdo da página.

- **Extração de Informações de PDFs**: Forneça o caminho de um arquivo PDF, e o bot será capaz de ler e interpretar seu conteúdo.

- **Análise de Vídeos do YouTube**: Insira o link de um vídeo do YouTube, e o bot extrairá informações úteis do vídeo para responder às suas perguntas.

- **OCR de Imagens**: Utilizando OCR, o bot pode extrair texto de imagens em vários idiomas (Português, Inglês, Francês, Alemão, Italiano, Espanhol, Japonês, Russo, Coreano, Chinês).

- **Memória Persistente**: As conversas são salvas em um banco de dados SQLite, permitindo que o bot recupere conversas anteriores mesmo após o encerramento do programa.

## Tecnologias Utilizadas

- **LangChain**: Framework utilizado para integrar modelos de linguagem e criar fluxos de trabalho complexos. Aqui, usamos o modelo Groq para gerar respostas do chatbot.

- **SQLite3**: Biblioteca Python utilizada para criar e gerenciar o banco de dados local onde as conversas e preferências dos usuários são armazenadas.

- **Pytesseract & OpenCV**: Ferramentas para processamento de imagens e extração de texto através de OCR.

- **PyPDFLoader**: Utilizado para carregar e extrair conteúdo de arquivos PDF.

- **WebBaseLoader**: Utilizado para extrair conteúdo de páginas da web.

- **YoutubeLoader**: Extrai informações de vídeos do YouTube.

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/felipecidade94/citybot.git
   cd citybot
   ```
2. **Instale as dependências necessárias:**
   Certifique-se de ter o Python 3.x instalado no seu sistema. Em seguida, instale as bibliotecas necessárias usando o pip
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuração da API Groq:**
Para utilizar o modelo de IA Groq, você precisará configurar sua chave de API. Adicione sua chave de API no arquivo principal ou defina-a como uma variável de ambiente:
   
## Como Usar
MENU
1. Bora conversar?
2. Informações sobre um site
3. Informações sobre um vídeo do YouTube
4. Informações sobre um PDF
5. OCR imagem
6. Sair

## Opções Disponíveis:
- **Bora conversar?**
    Inicie uma conversa direta com o bot. Você pode fazer perguntas ou simplesmente conversar sobre qualquer assunto.
- **Informações sobre um site**
    Insira a URL de um site, e o bot irá extrair informações relevantes. Depois disso, você pode fazer perguntas específicas sobre o conteúdo do site.
- **Informações sobre um vídeo do YouTube**
    Insira o link de um vídeo do YouTube, e o bot extrairá informações úteis do vídeo. Você pode fazer perguntas sobre o conteúdo do vídeo.
- **Informações sobre um PDF**
    Forneça o caminho para um arquivo PDF, e o bot irá extrair e interpretar seu conteúdo. Após isso, você pode fazer perguntas relacionadas ao documento.
- **OCR imagem**
    Insira o caminho de uma imagem, selecione o idioma da imagem, e o bot extrairá o texto contido na imagem. O texto extraído pode ser salvo em um arquivo      .txt ou .docx.
- **Sair**
    Encerra o programa.

## Estrutura do Banco de Dados

O CityBot utiliza um banco de dados SQLite para armazenar as conversas e preferências dos usuários. A estrutura do banco de dados inclui duas tabelas   
principais:
- **users:** Armazena informações básicas sobre os usuários, como nome e preferências.
- **conversations:** Armazena as mensagens trocadas entre o usuário e o assistente, permitindo que o bot "lembre" das interações anteriores.

## Licença
Este projeto está licenciado sob a MIT License.
   
