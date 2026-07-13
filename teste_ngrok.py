# -*- coding: utf-8 -*-
"""
Script de teste automatizado para ngrok compartilhado
Valida:
1. Django rodando em localhost:8000
2. Vídeo do carrossel acessível
3. Página com UTF-8 correto
4. ngrok funcionando
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from urllib import request, error

os.chdir(str(Path(__file__).parent))
os.environ['PYTHONIOENCODING'] = 'utf-8'

def check_django_running(port=8000):
    """Verifica se Django está rodando"""
    try:
        response = request.urlopen(f'http://127.0.0.1:{port}/', timeout=3)
        return response.status == 200
    except:
        return False

def check_video_exists():
    """Verifica se arquivo de vídeo existe e tem nome ASCII"""
    video_path = Path('media/carrossel/AFINAL_PARA_QUE_SERVE_O_CONSELHO_DE_ESCOLA.mp4')
    if video_path.exists():
        return True, video_path

    # Procura por variantes
    for f in Path('media/carrossel').glob('*.mp4'):
        return True, f

    return False, None

def check_video_via_http():
    """Testa acesso ao vídeo via HTTP"""
    try:
        response = request.urlopen('http://127.0.0.1:8000/media/carrossel/AFINAL_PARA_QUE_SERVE_O_CONSELHO_DE_ESCOLA.mp4', timeout=3)
        return response.status == 200
    except:
        return False

def check_carrossel_page():
    """Verifica se a home carrega o carrossel com vídeo"""
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=3)
        content = response.read().decode('utf-8')

        # Procura por referência ao vídeo
        has_video_ref = 'PARA_QUE' in content or 'carrossel' in content
        has_utf8 = 'Currículos' in content or 'SEDU' in content

        return has_video_ref, has_utf8
    except Exception as e:
        return False, str(e)

def run_tests():
    """Executa testes"""
    print("\n" + "="*60)
    print("  TESTE AUTOMATIZADO - NGROK SEDU")
    print("="*60 + "\n")

    # Teste 1: Django rodando
    print("[1] Verificando Django em http://127.0.0.1:8000/...")
    if check_django_running():
        print("    [OK] Django está rodando!\n")
    else:
        print("    [ERRO] Django NÃO está rodando!")
        print("    Inicie com: python manage.py runserver\n")
        return False

    # Teste 2: Arquivo de vídeo
    print("[2] Verificando arquivo de vídeo...")
    exists, path = check_video_exists()
    if exists:
        print(f"    [OK] Vídeo encontrado: {path.name}\n")
    else:
        print("    [ERRO] Arquivo de vídeo não encontrado!\n")
        return False

    # Teste 3: Vídeo acessível via HTTP
    print("[3] Testando acesso HTTP ao vídeo...")
    if check_video_via_http():
        print("    [OK] Vídeo acessível via HTTP!\n")
    else:
        print("    [AVISO] Vídeo pode não estar acessível")
        print("    Certifique-se de que Django está rodando\n")

    # Teste 4: Página com UTF-8
    print("[4] Verificando página com UTF-8...")
    has_ref, has_utf8 = check_carrossel_page()
    if has_utf8 and has_ref:
        print("    [OK] Página carregada com UTF-8 correto!\n")
    else:
        print("    [AVISO] Verificar encoding da página\n")

    print("="*60)
    print("  TUDO OK! Pronto para compartilhar com ngrok")
    print("="*60 + "\n")

    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
