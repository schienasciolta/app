# Monta o app da Schiena Sciolta a partir de _fonte/: junta exercícios e plano em conteudo.js e gera uma cópia do app
# em cada pasta de acesso. O acesso vai no CAMINHO (nunca na query): a query some quando a pessoa instala o PWA e ela
# perde o que comprou. Subir VERSAO a cada mudança publicada, senão o celular segue com o arquivo velho.
#   python _fonte/gerar.py
import json, os, re, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(AQUI)

# pasta -> o que ela libera. Cada compra leva ao link da sua pasta; o aparelho soma tudo o que já abriu.
PASTAS = {
    'k4r8tz': ['base'],                                   # front: o plano de 3 semanas
    'v2m9sa': ['base', 'sveglia'],                        # bump Sveglia senza rigidità
    'c7n3qe': ['base', 'collo'],                          # bump Collo e spalle
    'f5w1pd': ['base', 'forte'],                          # upsell Schiena Forte
    'x9t6lb': ['base', 'sveglia', 'collo', 'forte'],      # teste interno: tudo liberado (fora do ar, ver .gitignore)
}
# checkouts avulsos dos pacotes, abertos pelo cadeado dentro do app (preencher quando a Cakto existir)
CHECKOUT = {'sveglia': '#', 'collo': '#', 'forte': '#'}
VERSAO = 1

esercizi = json.load(open(os.path.join(AQUI, 'conteudo', 'esercizi.json'), encoding='utf-8'))
piano = json.load(open(os.path.join(AQUI, 'conteudo', 'piano.json'), encoding='utf-8'))
esercizi.pop('_nota', None); piano.pop('_nota', None)

# todo exercício citado no plano existe na biblioteca
usados = {e for d in piano['giorni'] for e, _ in d}
for k in ('sveglia', 'collo'):
    usados |= {e for e, _ in piano['pacchetti'][k]['esercizi']}
usados |= {e for g in piano['pacchetti']['forte']['giornate'].values() for e, _ in g}
falta = usados - set(esercizi)
assert not falta, f'exercícios sem ficha: {sorted(falta)}'
assert len(piano['giorni']) == 21, 'o plano tem de ter 21 dias'

with open(os.path.join(APP, 'conteudo.js'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('/* gerado por _fonte/gerar.py a partir de _fonte/conteudo/ */\nwindow.CONTEUDO=' +
            json.dumps({'esercizi': esercizi, 'piano': piano}, ensure_ascii=False, separators=(',', ':')) + ';\n')
shutil.copy2(os.path.join(AQUI, 'figura.js'), os.path.join(APP, 'figura.js'))

modelo = open(os.path.join(AQUI, 'app.html'), encoding='utf-8').read()

def pagina(acesso, raiz):
    s = modelo.replace('__ACESSO__', json.dumps(acesso)).replace('__RAIZ__', raiz)
    for k, v in CHECKOUT.items():
        s = s.replace(f'__CK_{k.upper()}__', v)
    assert not re.search(r'__[A-Z_]+__', s), 'sobrou marcador no modelo'
    return s

def manifesto(raiz_scope):
    return {
        'name': 'Schiena Sciolta', 'short_name': 'Schiena', 'lang': 'it',
        'description': 'Il piano di 3 settimane per la schiena, da fare a casa.',
        'start_url': './', 'scope': raiz_scope, 'display': 'standalone', 'orientation': 'portrait',
        'background_color': '#f4eee6', 'theme_color': '#f4eee6',
        'icons': [
            {'src': ('' if raiz_scope == './' else '../') + 'img/icones/icone-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': ('' if raiz_scope == './' else '../') + 'img/icones/icone-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': ('' if raiz_scope == './' else '../') + 'img/icones/icone-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }

# raiz: sem acesso (mostra o aviso de abrir pelo link do e-mail, a não ser que o aparelho já tenha acesso guardado)
open(os.path.join(APP, 'index.html'), 'w', encoding='utf-8', newline='\n').write(pagina([], './'))
json.dump(manifesto('./'), open(os.path.join(APP, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for pasta, acesso in PASTAS.items():
    os.makedirs(os.path.join(APP, pasta), exist_ok=True)
    open(os.path.join(APP, pasta, 'index.html'), 'w', encoding='utf-8', newline='\n').write(pagina(acesso, '../'))
    json.dump(manifesto('../'), open(os.path.join(APP, pasta, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

sw = open(os.path.join(AQUI, 'sw.js'), encoding='utf-8').read()
sw = sw.replace('__VERSAO__', str(VERSAO)).replace('__PASTAS__', json.dumps(list(PASTAS)))
open(os.path.join(APP, 'sw.js'), 'w', encoding='utf-8', newline='\n').write(sw)
open(os.path.join(APP, '.nojekyll'), 'w').close()
open(os.path.join(APP, '.gitignore'), 'w', encoding='utf-8', newline='\n').write(
    '# pasta de teste interno com tudo liberado: só local, nunca no ar\nx9t6lb/\n')

print('ok:', len(esercizi), 'exercícios,', len(piano['giorni']), 'dias,', len(PASTAS), 'pastas, conteudo.js com',
      os.path.getsize(os.path.join(APP, 'conteudo.js')) // 1024, 'KB, versão', VERSAO)
