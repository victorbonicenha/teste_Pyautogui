import pyautogui
import easyocr
import time

class ItauApp:
    def __init__(self):
        # inicializa o OCR do easyocr
        self.reader = easyocr.Reader(['pt', 'en'], gpu=False)

    def mapear_botoes(self):
        """
        Lê os botões do teclado virtual (ex: "1 ou 5") e retorna
        um dicionário que mapeia cada dígito para a posição (x, y).
        """
        botoes = {}

        # regiões fixas dos botões no protótipo HTML ou app real
        regioes = [
            (300, 400, 100, 80),  # botão 1
            (420, 400, 100, 80),  # botão 2
            (540, 400, 100, 80),  # botão 3
            (300, 500, 100, 80),  # botão 4
            (420, 500, 100, 80),  # botão 5
        ]

        for regiao in regioes:
            img = pyautogui.screenshot(region=regiao)
            caminho = "temp.png"
            img.save(caminho)

            results = self.reader.readtext(caminho)
            if results:
                texto = results[0][1].strip()

                if "ou" in texto:
                    nums = [n.strip() for n in texto.split("ou")]
                    # calcula o centro da região
                    x = regiao[0] + regiao[2] // 2
                    y = regiao[1] + regiao[3] // 2
                    for n in nums:
                        if n.isdigit():
                            botoes[n] = (x, y)

        return botoes

    def digitar_senha(self, senha, botoes):
        """
        Digita a senha clicando nos botões mapeados
        senha = string da senha (ex: '1234')
        botoes = dict {'1': (x,y), '2': (x,y), ...}
        """
        for digito in senha:
            if digito in botoes:
                x, y = botoes[digito]
                pyautogui.click(x, y)
                time.sleep(0.5)

    def login_app(self, senha, botoes):
        """Fluxo de login no app"""
        print("Iniciando login no app Itaú...")

        # Digitar senha
        self.digitar_senha(senha, botoes)

        # Confirmar login (exemplo: clica no botão confirmar fixo)
        # aqui você precisa colocar a região ou coordenada do botão "confirmar"
        pyautogui.click(600, 600)  # ajustar coordenada real
        time.sleep(1)

        print("Login finalizado.")

