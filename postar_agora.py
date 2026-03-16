"""
Script SIMPLES para postar no Instagram usando instagrapi.
Não precisa de navegador, API do Facebook, nem nada complicado.

Na sua máquina local:
    pip install instagrapi Pillow
    python postar_agora.py
"""

import os
import sys
from pathlib import Path

# Tenta importar instagrapi
try:
    from instagrapi import Client
except ImportError:
    print("❌ Biblioteca instagrapi não instalada.")
    print("   Execute: pip install instagrapi Pillow")
    sys.exit(1)

# ===================== CONFIGURAÇÃO =====================
INSTAGRAM_USER = os.environ.get("INSTAGRAM_USER", "maiconpode@hotmail.com")
INSTAGRAM_PASS = os.environ.get("INSTAGRAM_PASS", "Maicon26.")
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "post_ia_futuro.png")

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

via Pri Brand ✅

#InteligenciaArtificial #IA #FuturoDaTecnologia #AI #Tecnologia #Inovacao #TransformacaoDigital #FuturoDigital #IAGenerativa #MachineLearning
"""
# ========================================================


def gerar_imagem():
    """Gera a imagem do post se ela não existir."""
    if Path(IMAGE_PATH).exists():
        print(f"✅ Imagem já existe: {IMAGE_PATH}")
        return

    print("🎨 Gerando imagem do post...")
    from post_instagram import criar_imagem
    criar_imagem(IMAGE_PATH)


def postar():
    """Faz login e posta no Instagram."""
    # Verificar imagem
    if not Path(IMAGE_PATH).exists():
        gerar_imagem()

    if not Path(IMAGE_PATH).exists():
        print("❌ Imagem não encontrada e não foi possível gerar.")
        sys.exit(1)

    print("=" * 50)
    print("📸 POSTANDO NO INSTAGRAM")
    print(f"   Conta: {INSTAGRAM_USER}")
    print(f"   Imagem: {IMAGE_PATH}")
    print("=" * 50)

    # Login
    print("\n🔐 Fazendo login no Instagram...")
    cl = Client()

    # Tentar reutilizar sessão salva
    session_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".instagrapi_session.json")
    try:
        if Path(session_file).exists():
            cl.load_settings(session_file)
            cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)
            cl.get_timeline_feed()  # testar se sessão é válida
            print("   Sessão anterior reutilizada!")
        else:
            raise Exception("Sem sessão salva")
    except Exception:
        print("   Fazendo login novo...")
        cl = Client()
        cl.login(INSTAGRAM_USER, INSTAGRAM_PASS)

    # Salvar sessão para próxima vez
    cl.dump_settings(session_file)
    print("✅ Login realizado com sucesso!")

    # Postar
    print("\n📤 Enviando post...")
    media = cl.photo_upload(
        path=IMAGE_PATH,
        caption=CAPTION,
    )
    print(f"\n🎉 POST PUBLICADO COM SUCESSO!")
    print(f"   ID do post: {media.pk}")
    print(f"   Link: https://www.instagram.com/p/{media.code}/")


if __name__ == "__main__":
    postar()
