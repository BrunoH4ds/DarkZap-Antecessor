import flet as ft
import threading
import time

def main(pagina: ft.Page):
    pagina.title = "DarkZap"
    pagina.favicon = r"favicon.ico"
    pagina.bgcolor = ft.colors.BLACK
    pagina.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    # Título do aplicativo
    texto = ft.Text("DarkZap", size=40, weight="bold", color=ft.colors.WHITE)
    texto_container = ft.Container(content=texto, padding=10, alignment=ft.alignment.center)

    # Popup de boas-vindas
    nome_usuario = ft.TextField(label="Escreva seu nome", width=700, border_color=ft.colors.ORANGE_500)

    def entrar_popup(evento):
        if nome_usuario.value.strip():
            pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
            iniciar_chat()
            popup.open = False
            pagina.update()
        else:
            popup.title = ft.Text("Por favor, insira um nome.", color=ft.colors.RED)
            pagina.update()

    def sair_popup(evento):
        popup.open = False
        nome_usuario.value = ""
        pagina.update()

    def entrar_chat(evento):
        pagina.overlay.append(popup)
        popup.open = True
        pagina.update()

    def iniciar_chat():
        popup.open = False
        pagina.add(ft.Column(
            [
                chat_container,
                ft.Row(
                    [
                        botao_sair,
                        campo_mensagem,
                        botao_enviar_mensagem
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                texto_container_info
            ],
            expand=True,
        ))
        pagina.remove(container_titulo, botao_iniciar_chat_content)
        pagina.update()

    def sair_chat(evento):
        pagina.clean()  # Limpa a página
        pagina.add(container_titulo)
        pagina.add(botao_iniciar_chat_content)
        nome_usuario.value = ""
        pagina.update()

    botao_sair = ft.ElevatedButton("Sair", on_click=sair_chat, color=ft.colors.RED, height=50, width=100)

    chat = ft.ListView(spacing=10, expand=True)  # Usando ListView para o chat
    chat_container = ft.Container(
        content=chat,
        expand=True,
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(10),
        padding=10,
    )

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=lambda e: enviar_mensagem(), expand=True, border_color=ft.colors.ORANGE_500)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=lambda e: enviar_mensagem(), color=ft.colors.ORANGE_500, height=50, width=100)

    texto_info = ft.Text("AVISO: Todas as mensagens são apagadas após 1 minuto.", color=ft.colors.RED)
    texto_container_info = ft.Container(content=texto_info, padding=5, alignment=ft.alignment.center)

    def enviar_mensagem():
        if campo_mensagem.value.strip():
            pagina.pubsub.send_all({
                "texto": campo_mensagem.value,
                "usuario": nome_usuario.value,
                "tipo": "mensagem"
            })
            campo_mensagem.value = ""
            pagina.update() 

    def remover_mensagem(mensagem):
        time.sleep(60)
        if mensagem in chat.controls:  # Verifica se a mensagem ainda está presente
            chat.controls.remove(mensagem)
            pagina.update()

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            nova_mensagem = ft.Text(f"{usuario_mensagem}: {texto_mensagem}", color=ft.colors.WHITE, size=16)
            chat.controls.append(nova_mensagem)
            pagina.update()

            threading.Thread(target=remover_mensagem, args=(nova_mensagem,)).start()

        else:
            usuario_mensagem = mensagem["usuario"]
            nova_entrada = ft.Text(f"{usuario_mensagem} entrou no chat", size=12, italic=True, color=ft.colors.ORANGE_500)
            chat.controls.append(nova_entrada)
            pagina.update()

            threading.Thread(target=remover_mensagem, args=(nova_entrada,)).start()



    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    container_titulo = ft.Container(
        content=texto_container,
        alignment=ft.alignment.center,
        expand=True  # Ocupará toda a altura disponível
    )

    botao_iniciar_chat = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat, color=ft.colors.ORANGE_500, height=50, width=200)
    botao_iniciar_chat_content = ft.Container(content=botao_iniciar_chat, margin=40, alignment=ft.alignment.center)
    pagina.add(container_titulo)
    pagina.add(botao_iniciar_chat_content)
    # Definindo o texto da mensagem e o título do popup
    mensagem_lembrete = ft.Text("Lembrete: Deslize a página para ver novas mensagens", color=ft.colors.WHITE)
    titulo_popup = ft.Text("Bem-vindo ao DarkZap!", color=ft.colors.WHITE)  # Removida a vírgula

    # Container para o título (opcional, você pode manter isso se quiser)
    titulo_popup_container = ft.Container(content=titulo_popup, padding=10, alignment=ft.alignment.center)

    # Criando o popup
    # Criando o popup com tamanho mínimo
    popup = ft.AlertDialog(
    open=False,
    modal=True,
    title=titulo_popup,
    content=ft.Column(
        controls=[
            nome_usuario,
            mensagem_lembrete,
        ],
        expand=False,height=90
    ),
    actions=[
        ft.ElevatedButton("Entrar", on_click=entrar_popup, color=ft.colors.ORANGE_500),
        ft.ElevatedButton("Sair", on_click=sair_popup, color=ft.colors.RED)
    ],
)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8081)
