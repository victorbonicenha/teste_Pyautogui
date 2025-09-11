from Teste_Pyautogui import ItauApp
import webbrowser
import time, os

if __name__ == "__main__":
    app = ItauApp()
    senha = "7243"

    # Abre o protótipo no navegador
    webbrowser.open("file:///" + os.path.abspath("teclado.html"))
    time.sleep(2)

    # Mapeia os botões
    botoes = app.mapear_botoes()

    # Digita a senha e confirma
    app.login_app(senha, botoes)
