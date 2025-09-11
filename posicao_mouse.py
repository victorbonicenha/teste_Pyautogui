import pyautogui
import keyboard
import time
import webbrowser
import os

webbrowser.open("file:///" + os.path.abspath("teclado.html"))

print("Passe o mouse e aperte espaço para capturar posições...")
coords = []
while len(coords) < 10:  # 5 botões → 2 pontos cada
    if keyboard.is_pressed("space"):
        coords.append(pyautogui.position())
        print("Capturado:", coords[-1])
        time.sleep(0.3)  # debounce


'''
# pontos que você salvou
x1, y1 = 486, 610   # canto superior esquerdo
x2, y2 = 1163, 729  # canto inferior direito

# garante que x1,y1 sempre seja o canto superior esquerdo
x = min(x1, x2)
y = min(y1, y2)
w = abs(x2 - x1)
h = abs(y2 - y1)

# tira print da região
img = pyautogui.screenshot(region=(x, y, w, h))
img.save("botao_debug.png")

print(f"📸 Screenshot salva! Região capturada: x={x}, y={y}, w={w}, h={h}")
'''

