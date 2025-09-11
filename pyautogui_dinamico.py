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
        botoes = {}
        tela = pyautogui.screenshot()
        tela.save("tela_completa.png")

        results = self.reader.readtext("tela_completa.png")

        for (bbox, texto, conf) in results:
            texto = texto.lower().replace("0u", "ou").strip()
            if "ou" in texto:
                nums = [n.strip() for n in texto.split("ou")]
                # centro do bounding box
                x = int((bbox[0][0] + bbox[2][0]) / 2)
                y = int((bbox[0][1] + bbox[2][1]) / 2)
                for n in nums:
                    if n.isdigit():
                        botoes[n] = (x, y)

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
