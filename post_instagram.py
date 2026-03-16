"""
Script para postar no Instagram sobre o Futuro da Inteligência Artificial.

Requisitos:
    pip install requests Pillow

Configuração:
    1. Crie um app em https://developers.facebook.com/
    2. Conecte sua conta Instagram Business/Creator
    3. Gere um token de acesso com permissão instagram_content_publish
    4. Preencha as variáveis ACCESS_TOKEN e INSTAGRAM_ACCOUNT_ID abaixo
"""

import requests
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ===================== CONFIGURAÇÃO =====================
ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "SEU_TOKEN_AQUI")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "SEU_ID_AQUI")
GRAPH_API_URL = "https://graph.facebook.com/v19.0"
# ========================================================

CAPTION = """🤖 O Futuro da Inteligência Artificial 🚀

A inteligência artificial está transformando o mundo como nunca antes. Veja o que nos espera:

🔮 Previsões para os próximos anos:

1️⃣ IA Generativa Avançada — Criação de conteúdo, arte, música e código cada vez mais sofisticados e personalizados.

2️⃣ Agentes Autônomos — IAs que executam tarefas complexas de forma independente, desde pesquisas até gestão de projetos.

3️⃣ IA na Saúde — Diagnósticos mais precisos, descoberta acelerada de medicamentos e medicina personalizada.

4️⃣ Robótica Inteligente — Robôs com IA integrada trabalhando lado a lado com humanos no dia a dia.

5️⃣ IA Ética e Regulamentada — Governos e empresas criando regras para uso responsável da tecnologia.

💡 O futuro não é sobre substituir humanos, mas sobre potencializar nossas capacidades!

A pergunta não é SE a IA vai mudar sua vida, mas COMO você vai usar ela a seu favor. 💪

#InteligenciaArtificial #IA #FuturoDaTecnologia #AI #Tecnologia #Inovacao #TransformacaoDigital #FuturoDigital #IAGenerativa #MachineLearning
"""


def criar_imagem(output_path="post_ia_futuro.png"):
    """Cria uma imagem 1080x1080 para o post do Instagram."""
    largura, altura = 1080, 1080
    img = Image.new("RGB", (largura, altura))
    draw = ImageDraw.Draw(img)

    # Fundo gradiente roxo/azul
    for y in range(altura):
        r = int(30 + (100 - 30) * y / altura)
        g = int(0 + (50 - 0) * y / altura)
        b = int(120 + (200 - 120) * y / altura)
        draw.line([(0, y), (largura, y)], fill=(r, g, b))

    # Elementos decorativos (circulos)
    for cx, cy, radius, alpha in [(200, 200, 80, 60), (880, 300, 60, 40),
                                   (500, 800, 100, 50), (150, 700, 40, 30),
                                   (900, 750, 70, 45)]:
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                     outline=(255, 255, 255, alpha), width=2)

    # Texto
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_rodape = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except OSError:
        font_titulo = ImageFont.load_default()
        font_sub = font_titulo
        font_rodape = font_titulo

    # Título
    titulo = "O FUTURO DA"
    titulo2 = "INTELIGÊNCIA"
    titulo3 = "ARTIFICIAL"

    draw.text((540, 200), titulo, fill="white", font=font_titulo, anchor="mm")
    draw.text((540, 270), titulo2, fill="white", font=font_titulo, anchor="mm")
    draw.text((540, 340), titulo3, fill=(0, 220, 255), font=font_titulo, anchor="mm")

    # Separador
    draw.line([(340, 400), (740, 400)], fill=(0, 220, 255), width=3)

    # Tópicos
    topicos = [
        "🔮 IA Generativa Avançada",
        "🤖 Agentes Autônomos",
        "🏥 IA na Saúde",
        "⚙️ Robótica Inteligente",
        "📋 IA Ética e Regulamentada",
    ]
    y_pos = 460
    for topico in topicos:
        draw.text((540, y_pos), topico, fill="white", font=font_sub, anchor="mm")
        y_pos += 60

    # Rodapé
    draw.text((540, 920), "O futuro é agora. Prepare-se! 🚀",
              fill=(0, 220, 255), font=font_rodape, anchor="mm")

    # Borda
    draw.rectangle([10, 10, largura - 10, altura - 10],
                   outline=(0, 220, 255), width=2)

    img.save(output_path, "PNG")
    print(f"Imagem criada: {output_path}")
    return output_path


def postar_no_instagram(image_url, caption):
    """
    Posta uma imagem no Instagram via Graph API.
    NOTA: A imagem precisa estar hospedada em uma URL pública acessível.
    """
    if ACCESS_TOKEN == "SEU_TOKEN_AQUI" or INSTAGRAM_ACCOUNT_ID == "SEU_ID_AQUI":
        print("\n⚠️  ATENÇÃO: Configure suas credenciais!")
        print("   1. Defina a variável de ambiente INSTAGRAM_ACCESS_TOKEN")
        print("   2. Defina a variável de ambiente INSTAGRAM_ACCOUNT_ID")
        print("   Ou edite as variáveis no topo deste script.")
        print(f"\n📝 Legenda do post:\n{caption}")
        return None

    # Etapa 1: Criar container de mídia
    print("📤 Criando container de mídia...")
    response = requests.post(
        f"{GRAPH_API_URL}/{INSTAGRAM_ACCOUNT_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN,
        },
    )
    response.raise_for_status()
    creation_id = response.json()["id"]
    print(f"   Container criado: {creation_id}")

    # Etapa 2: Publicar
    print("📸 Publicando no Instagram...")
    response = requests.post(
        f"{GRAPH_API_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN,
        },
    )
    response.raise_for_status()
    post_id = response.json()["id"]
    print(f"✅ Post publicado com sucesso! ID: {post_id}")
    return post_id


if __name__ == "__main__":
    # 1. Criar a imagem do post
    imagem_path = criar_imagem()

    # 2. Para postar, a imagem precisa estar em uma URL pública
    #    Exemplos: Hospede no Imgur, AWS S3, ou seu servidor
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASSOS:")
    print("=" * 60)
    print(f"1. A imagem foi salva em: {imagem_path}")
    print("2. Hospede a imagem em uma URL pública (ex: Imgur, S3)")
    print("3. Configure suas credenciais do Instagram Graph API")
    print("4. Execute novamente passando a URL da imagem")
    print("=" * 60)

    # Descomente a linha abaixo após configurar tudo:
    # postar_no_instagram("https://sua-url.com/imagem.png", CAPTION)
