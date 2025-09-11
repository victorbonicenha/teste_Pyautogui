import pyautogui
import easyocr
import time
import mss
import numpy as np
import cv2
from PIL import Image

class ItauApp:
    def __init__(self):
        self.reader = easyocr.Reader(['pt', 'en'], gpu=False)

    def screenshot_regiao(self, regiao, nome="temp.png"):
        """Captura uma região específica da tela usando mss."""
        x, y, w, h = regiao
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            Image.fromarray(img).save(nome)
        return nome

    def mapear_botoes(self):
        """Mapeia os botões do teclado virtual na tela usando OCR em regiões fixas."""
        botoes = {}

        # Regiões calibradas (x, y, w, h) -> já medidas com o mouse
        regioes = [
            (640, 349, 120, 80),  # botão 1
            (760, 349, 120, 80),  # botão 2
            (880, 349, 120, 80),  # botão 3
            (640, 449, 120, 80),  # botão 4
            (760, 449, 120, 80),  # botão 5
        ]

        for i, regiao in enumerate(regioes, start=1):
            caminho = self.screenshot_regiao(regiao, f"debug_botao_{i}.png")
            print(f"[DEBUG] Screenshot salvo: debug_botao_{i}.png")

            results = self.reader.readtext(caminho)
            if results:
                texto = results[0][1].strip().lower()
                texto = texto.replace("0u", "ou")  # corrige erro comum
                print(f"[OCR Botão {i}] → {texto}")

                if "ou" in texto:
                    nums = [n.strip() for n in texto.split("ou")]
                    cx = regiao[0] + regiao[2] // 2
                    cy = regiao[1] + regiao[3] // 2
                    for n in nums:
                        if n.isdigit():
                            botoes[n] = (cx, cy)

        # botão confirmar (coordenada manual que você pegou)
        botoes["confirmar"] = (541, 548)

        print("Botões detectados:", botoes)
        return botoes

    def digitar_senha(self, senha, botoes):
        """Digita a senha clicando nos botões mapeados."""
        for digito in senha:
            if digito in botoes:
                x, y = botoes[digito]
                pyautogui.click(x, y)
                time.sleep(0.5)
            else:
                print(f"Dígito {digito} não encontrado!")

    def login_app(self, senha, botoes):
        """Fluxo completo de login."""
        print("Iniciando login no app Itaú...")
        self.digitar_senha(senha, botoes)

        if "confirmar" in botoes:
            pyautogui.click(botoes["confirmar"])
            print("Clique no botão Confirmar.")
        else:
            print("Botão Confirmar não encontrado!")

        time.sleep(1)
        print("Login finalizado.")
