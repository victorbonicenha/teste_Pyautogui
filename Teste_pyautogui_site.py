from Teste_Pyautogui import ItauApp
import webbrowser
import time
import os

if __name__ == "__main__":
    app = ItauApp()
    senha = "7243"

    # 1. Abre o protótipo no navegador
    webbrowser.open("file:///" + os.path.abspath("teclado.html"))
    time.sleep(2)  # espera carregar

    # 2. Mapeia os botões no HTML
    botoes = app.mapear_botoes()

    # 3. Digita a senha 7243
    app.login_app(senha, botoes)
