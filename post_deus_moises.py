"""
Script para criar imagem e postar no Instagram sobre o Deus de Moisés.

Na sua máquina local:
    pip install instagrapi Pillow
    python post_deus_moises.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "post_deus_moises.png")

CAPTION = """🔥 O DEUS DE MOISÉS 🔥

O Deus que abriu o Mar Vermelho é o mesmo Deus que abre caminhos na sua vida!

📖 Lições poderosas da história de Moisés:

1️⃣ Deus chama os imperfeitos — Moisés gaguejava, mas Deus o escolheu para libertar um povo inteiro. Suas limitações não limitam Deus!

2️⃣ A sarça que arde e não se consome — Deus se revelou no lugar mais improvável. Ele pode se revelar a você hoje, onde você estiver.

3️⃣ "EU SOU O QUE SOU" — Deus não precisa de apresentação. Ele é o mesmo ontem, hoje e sempre. (Êxodo 3:14)

4️⃣ O Mar se abriu! — Quando não havia saída, Deus criou um caminho no meio do impossível. Ele faz o mesmo por você!

5️⃣ O deserto tem propósito — 40 anos no deserto não foram castigo, foram preparação. Seu deserto também tem propósito!

💪 Se Deus é por nós, quem será contra nós? (Romanos 8:31)

🙏 O mesmo Deus de Moisés é o SEU Deus. Confie!

#DeusDeMoises #Fe #Biblia #DeusEFiel #PalavradeDeus #ExodoBiblico #MarVermelho #Jesus #Cristo #VidaCrista #FeCrista #DevocionalDiario #MensagemDeDeus
"""


def criar_imagem(output_path=IMAGE_PATH):
    """Cria uma imagem 1080x1080 para o post do Instagram."""
    largura, altura = 1080, 1080

    # Fundo degradê escuro (azul escuro para preto)
    img = Image.new("RGB", (largura, altura), (10, 10, 40))
    draw = ImageDraw.Draw(img)

    # Criar efeito de degradê manual
    for y in range(altura):
        r = int(10 + (25 - 10) * (y / altura))
        g = int(10 + (15 - 10) * (y / altura))
        b = int(40 + (60 - 40) * (y / altura))
        draw.line([(0, y), (largura, y)], fill=(r, g, b))

    # Fontes
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 58)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_texto = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_versiculo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_rodape = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except OSError:
        font_titulo = ImageFont.load_default()
        font_sub = font_titulo
        font_texto = font_titulo
        font_versiculo = font_titulo
        font_rodape = font_titulo

    cor_dourada = (255, 200, 50)
    cor_branca = (255, 255, 255)
    cor_fogo = (255, 100, 30)
    cor_clara = (200, 200, 220)

    # === Borda dourada ===
    draw.rectangle([8, 8, largura - 8, altura - 8], outline=cor_dourada, width=3)
    draw.rectangle([16, 16, largura - 16, altura - 16], outline=(255, 200, 50, 128), width=1)

    # === Símbolo da sarça ardente (fogo estilizado) ===
    centro_x = 540
    # Chamas (triângulos simples)
    chama_pontos = [
        [(centro_x, 50), (centro_x - 30, 110), (centro_x + 30, 110)],
        [(centro_x - 20, 60), (centro_x - 45, 110), (centro_x + 5, 110)],
        [(centro_x + 20, 60), (centro_x - 5, 110), (centro_x + 45, 110)],
    ]
    for pontos in chama_pontos:
        draw.polygon(pontos, fill=cor_fogo)
    # Chama central amarela
    draw.polygon([(centro_x, 65), (centro_x - 15, 105), (centro_x + 15, 105)], fill=cor_dourada)

    # === Título ===
    draw.text((540, 160), "O DEUS DE", fill=cor_branca, font=font_titulo, anchor="mm")
    draw.text((540, 230), "MOISES", fill=cor_dourada, font=font_titulo, anchor="mm")

    # Linha decorativa
    draw.line([(300, 280), (780, 280)], fill=cor_dourada, width=2)

    # === Tópicos ===
    topicos = [
        "Deus chama os imperfeitos",
        "A sarca que arde e nao",
        "se consome",
        "\"EU SOU O QUE SOU\"",
        "O Mar se abriu!",
        "O deserto tem proposito",
    ]

    y_pos = 340
    marcador = 1
    for texto in topicos:
        if texto in ("se consome",):
            # Continuação da linha anterior
            draw.text((540, y_pos), texto, fill=cor_clara, font=font_texto, anchor="mm")
            y_pos += 50
            continue
        draw.text((540, y_pos), f"{marcador}. {texto}", fill=cor_clara, font=font_texto, anchor="mm")
        marcador += 1
        y_pos += 50

    # === Versículo destaque ===
    draw.line([(300, y_pos + 20), (780, y_pos + 20)], fill=cor_fogo, width=2)

    draw.text((540, y_pos + 70), "\"Se Deus e por nos,", fill=cor_dourada, font=font_sub, anchor="mm")
    draw.text((540, y_pos + 120), "quem sera contra nos?\"", fill=cor_dourada, font=font_sub, anchor="mm")
    draw.text((540, y_pos + 170), "Romanos 8:31", fill=cor_branca, font=font_versiculo, anchor="mm")

    # === Rodapé ===
    draw.line([(300, altura - 120), (780, altura - 120)], fill=cor_dourada, width=1)
    draw.text((540, altura - 80), "O mesmo Deus de Moises e o SEU Deus!", fill=cor_fogo, font=font_rodape, anchor="mm")
    draw.text((540, altura - 45), "Confie!", fill=cor_dourada, font=font_versiculo, anchor="mm")

    img.save(output_path, "PNG")
    print(f"✅ Imagem criada: {output_path}")
    return output_path


if __name__ == "__main__":
    criar_imagem()
    print(f"\n📝 Legenda do post:\n{CAPTION}")
