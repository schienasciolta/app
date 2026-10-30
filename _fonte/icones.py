# Gera os ícones do app (PNG) com o desenho da marca: fundo verde e a coluna em pontos, solta, em curva suave.
#   python _fonte/icones.py
import math, os
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), 'img', 'icones')
os.makedirs(SAIDA, exist_ok=True)

VERDE, CREME = (47, 111, 98), (244, 238, 230)

def icone(lado, margem_segura=False, cantos=True):
    k = 4  # desenha grande e reduz, para a borda sair lisa
    L = lado * k
    im = Image.new('RGBA', (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if cantos:
        d.rounded_rectangle([0, 0, L - 1, L - 1], radius=int(L * .22), fill=VERDE)
    else:
        d.rectangle([0, 0, L, L], fill=VERDE)
    escala = .62 if margem_segura else .78
    # a coluna: 7 vértebras numa curva em S suave, cada uma uma pílula
    n = 7
    for i in range(n):
        t = i / (n - 1)
        y = L * (.5 - escala / 2 + escala * t)
        x = L * .5 + math.sin(t * math.pi * 1.6 - .5) * L * .07 * escala / .78
        w = L * (.20 - .03 * abs(t - .55)) * escala / .78
        h = L * .062 * escala / .78
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=int(h / 2), fill=CREME)
    return im.resize((lado, lado), Image.LANCZOS)

icone(192).save(os.path.join(SAIDA, 'icone-192.png'))
icone(512).save(os.path.join(SAIDA, 'icone-512.png'))
icone(512, margem_segura=True, cantos=False).save(os.path.join(SAIDA, 'icone-maskable-512.png'))
icone(180, cantos=False).convert('RGB').save(os.path.join(SAIDA, 'apple-touch-180.png'))
icone(32).save(os.path.join(SAIDA, 'favicon-32.png'))
print('ok:', sorted(os.listdir(SAIDA)))
