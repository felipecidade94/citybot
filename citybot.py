import os
import sqlite3
import cv2
import pytesseract
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import pyperclip
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, YoutubeLoader


class CityBot:
    def __init__(self, api_key, api_model):
        self.api_key = api_key
        self.api_model = api_model
        self.conexao = sqlite3.connect('citybot.db')
        self.create_table()
        self.memory = ConversationBufferWindowMemory(k=99999)

    def create_table(self):
        with self.conexao:
            self.conexao.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                preferences TEXT
            )
            """)

            self.conexao.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                user_message TEXT,
                assistant_response TEXT
            )
            """)

    def save_user(self, name, preferences):
        with self.conexao:
            self.conexao.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", (name, preferences))

    def load_user(self, name):
        with self.conexao:
            return self.conexao.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()

    def save_conversation(self, user_message, assistant_response):
        with self.conexao:
            self.conexao.execute("INSERT INTO conversations (user_message, assistant_response) VALUES (?, ?)", (user_message, assistant_response))

    def load_conversations(self):
        with self.conexao:
            return self.conexao.execute("SELECT user_message, assistant_response FROM conversations").fetchall()

    def chat(self):
        chat = ChatGroq(model=self.api_model)
        return chat

    def resposta_bot(self, mensagens, documento=''):
        mensagem_sistema = 'Você é um assistente amigável chamado CityBot, capaz de conversar sobre qualquer assunto, inclusive qualquer informação sobre {informacoes}.'
        informacoes = documento if documento else ''
        mensagem_modelo = [('system', mensagem_sistema.format(informacoes=informacoes))]
        for tipo, conteudo in mensagens:
            if tipo not in ['user', 'assistant']:
                tipo = 'user' if tipo == 'human' else 'assistant'
            mensagem_modelo.append((tipo, conteudo))
        template = ChatPromptTemplate.from_messages(mensagem_modelo)
        chain = template | self.chat()
        return chain.invoke({'informacoes': informacoes}).content

    def carrega_site(self):
        url_site = input('Informe o URL do site: ').strip()
        loader = WebBaseLoader(url_site)
        documento = ''.join(doc.page_content for doc in loader.load())
        return documento

    def carrega_video(self):
        url_video = input('Informe o URL do vídeo: ').strip()
        loader = YoutubeLoader.from_youtube_url(url_video, language=['pt'])
        documento = ''.join(doc.page_content for doc in loader.load())
        return documento

    def carrega_pdf(self):
        caminho = input('Informe o caminho do PDF: ').replace('\\', '/').replace('"', '').strip()
        loader = PyPDFLoader(caminho)
        documento = ''.join(doc.page_content for doc in loader.load())
        return documento

    def carrega_imagem_ocr(self):
        caminho = input('Informe o caminho da imagem: ').replace('\\', '/').replace('"', '').strip()
        print('Defina o idioma da imagem:\n1. Portugês\n2. Inglês\n3. Francês\n4. Alemão\n5. Italiano\n6. Espanhol\n7. Japonês\n8. Russo\n9. Coreano\n10. Chinês')
        idioma = input('Qual o idioma da imagem? ').strip()
        if idioma not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            print('Idioma inválido!')
            return
        idioma = {'1': 'por', '2': 'eng', '3': 'fra', '4': 'deu', '5': 'ita', '6': 'spa', '7': 'jpn', '8': 'rus', '9': 'kor', '10': 'chn'}[idioma]
        imagem = cv2.imread(caminho)
        texto = pytesseract.image_to_string(imagem, lang=idioma)
        print(texto.strip())
        opc = input('Deseja salvar o texto em um arquivo? [S/N] ').strip().lower()
        if opc == 's':
            nome = input('Informe o nome que desejado para salvar o arquivo: ')
            documento = Document()
            documento.add_paragraph(texto)
            documento.save(f'{nome}.docx')
            with open(f'{nome}.txt', 'w', encoding='utf-8') as file:
                file.write(texto)
            return texto
        elif opc == 'n':
            return texto
        else:
            print('Opção inválida!')
            return

    def menu(self):
        memory = self.memory
        pyperclip.copy('')
        menu = 'MENU\n1. Bora conversar?\n2. Informações sobre um site\n3. Informações sobre um vídeo do YouTube\n4. Informações sobre um PDF\n5. OCR imagem\n6. Sair'
        print(menu)
        nova_informacao = ''
        mensagens = [(tipo, conteudo) for tipo, conteudo in self.load_conversations()]
        while True:
            opcao = input('Escolha uma opção: ')
            if opcao not in '1234567':
                print('Opção inválida!')
            else:
                if opcao == '1':
                    print('Comece a conversar ou digite "menu" para voltar ao menu. Digite "sair" para sair do programa')
                    while True:
                        paste = pyperclip.paste()
                        if not paste:
                            pergunta = input()
                            if pergunta.lower().strip() == 'menu':
                                print(menu)
                                break
                            if pergunta.lower().strip() == 'sair':
                                print('Saindo...')
                                exit()
                            mensagens.append(('user', pergunta))
                            resposta = self.resposta_bot(mensagens, nova_informacao)
                            mensagens.append(('assistant', resposta))
                            memory.save_context({'input': pergunta}, {'output': resposta})
                            self.save_conversation(pergunta, resposta)
                            print()
                            print(resposta)
                        else:
                            pergunta = []
                            while True:
                                linha = input()
                                if linha == 'menu':
                                    print(menu)
                                    break
                                if linha == '':
                                    break
                                if linha == 'sair':
                                    print('Saindo...')
                                    exit()
                                pergunta.append(linha)
                            pergunta = '\n'.join(pergunta).strip()
                            mensagens.append(('user', pergunta))
                            resposta = self.resposta_bot(mensagens, nova_informacao)
                            mensagens.append(('assistant', resposta))
                            memory.save_context({'input': pergunta}, {'output': resposta})
                            self.save_conversation(pergunta, resposta)
                            print()
                            print(resposta)
                            pyperclip.copy('')
                elif opcao == '2':
                    try:
                        nova_informacao = self.carrega_site()
                    except:
                        print('URL inválido!')
                        continue
                    print('Me faça perguntas sobre esse site. Digite "menu" para voltar ao menu ou "sair" para sair do programa')
                    while True:
                        pergunta = input()
                        if pergunta.lower().strip() == 'menu':
                            print(menu)
                            break
                        if pergunta.lower().strip() == 'sair':
                            print('Saindo...')
                            exit()
                        mensagens.append(('user', pergunta))
                        resposta = self.resposta_bot(mensagens, nova_informacao)
                        mensagens.append(('assistant', resposta))
                        memory.save_context({'input': pergunta}, {'output': resposta})
                        self.save_conversation(pergunta, resposta)
                        print()
                        print(resposta)
                elif opcao == '3':
                    try:
                        nova_informacao = self.carrega_video()
                    except:
                        print('URL inválido!')
                        continue
                    print('Faça perguntas sobre o vídeo. Digite "menu" para voltar ao menu ou "sair" para sair do programa')
                    while True:
                        pergunta = input('')
                        if pergunta.lower().strip() == 'menu':
                            print(menu)
                            break
                        if pergunta.lower().strip() == 'sair':
                            print('Saindo...')
                            exit()
                        mensagens.append(('user', pergunta))
                        resposta = self.resposta_bot(mensagens, nova_informacao)
                        mensagens.append(('assistant', resposta))
                        memory.save_context({'input': pergunta}, {'output': resposta})
                        self.save_conversation(pergunta, resposta)
                        print()
                        print(resposta)
                elif opcao == '4':
                    try:
                        nova_informacao = self.carrega_pdf()
                    except:
                        print('Caminho inválido!')
                        continue
                    print('Me faça perguntas sobre esse PDF. Digite "menu" para voltar ao menu ou "sair" para sair do programa')
                    while True:
                        pergunta = input()
                        if pergunta.lower().strip() == 'menu':
                            print(menu)
                            break
                        if pergunta.lower().strip() == 'sair':
                            print('Saindo...')
                            exit()
                        mensagens.append(('user', pergunta))
                        resposta = self.resposta_bot(mensagens, nova_informacao)
                        mensagens.append(('assistant', resposta))
                        memory.save_context({'input': pergunta}, {'output': resposta})
                        self.save_conversation(pergunta, resposta)
                        print()
                        print(resposta)
                elif opcao == '5':
                    try:
                        nova_informacao = self.carrega_imagem_ocr()
                    except:
                        print('URL inválido!')
                        continue
                    print('OCR imgem. Digite "menu" para voltar ao menu ou "sair" para sair do programa')
                    while True:
                        pergunta = input('')
                        if pergunta.lower().strip() == 'menu':
                            print(menu)
                            break
                        if pergunta.lower().strip() == 'sair':
                            print('Saindo...')
                            exit()
                        mensagens.append(('user', pergunta))
                        resposta = self.resposta_bot(mensagens, nova_informacao)
                        mensagens.append(('assistant', resposta))
                        memory.save_context({'input': pergunta}, {'output': resposta})
                        self.save_conversation(pergunta, resposta)
                        print()
                        print(resposta)
                elif opcao == '6':
                    print('Saindo...')
                    break

if __name__ == '__main__':
    api_key = 'SUA CHAVE AQUI'
    os.environ['GROQ_API_KEY'] = api_key
    api_model = 'llama-3.1-8b-instant'
    city_bot = CityBot(api_key, api_model)
    city_bot.menu()
    # llama-3.3-70b-versatile
    # llama-3.1-8b-instant
    # llama3-70b-8192
    # llama3-8b-8192
    # gemma2-9b-it
    # llama-3.2-1b-preview
    # llama-3.2-3b-preview
    # llama-3.2-11b-vision-preview
    # llama-3.2-90b-vision-preview