# Gera os ícones do app (PNG) a partir de _fonte/icone-fonte.png (desenho da marca feito no ChatGPT, fundo cheio).
#   python _fonte/icones.py
import os
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), 'img', 'icones')
os.makedirs(SAIDA, exist_ok=True)
fonte = Image.open(os.path.join(AQUI, 'icone-fonte.png')).convert('RGB')

def arredondado(lado, raio=.22):
    im = fonte.resize((lado, lado), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (lado * 4, lado * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, lado * 4 - 1, lado * 4 - 1], radius=int(lado * 4 * raio), fill=255)
    im.putalpha(m.resize((lado, lado), Image.LANCZOS))
    return im

arredondado(192).save(os.path.join(SAIDA, 'icone-192.png'))
arredondado(512).save(os.path.join(SAIDA, 'icone-512.png'))
fonte.resize((512, 512), Image.LANCZOS).save(os.path.join(SAIDA, 'icone-maskable-512.png'))  # fundo cheio: o sistema recorta
fonte.resize((180, 180), Image.LANCZOS).save(os.path.join(SAIDA, 'apple-touch-180.png'))      # iOS arredonda sozinho
arredondado(32).save(os.path.join(SAIDA, 'favicon-32.png'))
print('ok:', sorted(os.listdir(SAIDA)))
