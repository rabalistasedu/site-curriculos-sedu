#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para compartilhar o site SEDU com ngrok usando pyngrok
Executa: python ngrok_compartilhar.py
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Importa pyngrok
try:
    from pyngrok import ngrok, conf
except ImportError:
    print("❌ ERRO: pyngrok não está instalado!")
    print("\nExecute:")
    print("  pip install pyngrok")
    sys.exit(1)

def clear_screen():
    """Limpa a tela"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Exibe o header"""
    print("\n" + "=" * 60)
    print("  COMPARTILHAR SITE CURRICULOS SEDU COM NGROK")
    print("=" * 60 + "\n")

def configure_ngrok():
    """Configura o token do ngrok"""
    print("[1] Configurando ngrok...")

    token = "3GDq7YemLYPBMCKKzwjhpQiRhUg_4sGSn9v8nXaN6V4YurPko"
    ngrok.set_auth_token(token)

    print("    ✅ Token configurado com sucesso!\n")

def check_django():
    """Verifica se Django está rodando"""
    print("[2] Verificando se Django está rodando em http://127.0.0.1:8000/...")

    try:
        import urllib.request
        urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)
        print("    ✅ Django está rodando!\n")
        return True
    except Exception as e:
        print("    ⚠️  Django NÃO está rodando!\n")
        print("    Abra outro CMD e execute:")
        print("      cd \"C:\\ridan\\Claude\\Projects\\Site Curriculos SEDU\"")
        print("      venv\\Scripts\\activate")
        print("      python manage.py runserver\n")
        input("    Pressione ENTER após iniciar Django...")
        return False

def start_ngrok():
    """Inicia ngrok e exibe o link"""
    print("[3] Iniciando ngrok...\n")

    try:
        # Inicia ngrok apontando para localhost:8000
        public_url = ngrok.connect(8000, "http")

        print("\n" + "=" * 60)
        print("  ✅ NGROK ATIVADO COM SUCESSO!")
        print("=" * 60)
        print("\n")
        print("  🔗 LINK PARA COMPARTILHAR COM SEU GERENTE:")
        print("\n")
        print(f"  📌 {public_url}")
        print("\n")
        print("=" * 60)
        print("\n")
        print("  INFORMAÇÕES:")
        print(f"  - Válido por: 2 horas (versão gratuita)")
        print(f"  - Acesso: Seu gerente pode acessar de qualquer lugar")
        print(f"  - Dashboard: http://127.0.0.1:4040")
        print(f"  - Para parar: Pressione Ctrl+C\n")
        print("=" * 60 + "\n")

        # Mantém ngrok rodando
        print("ngrok está ativo! Compartilhe o link acima com seu gerente.\n")
        print("Pressione Ctrl+C para parar ngrok...\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Parando ngrok...")
            ngrok.kill()
            print("✅ ngrok desligado!\n")

    except Exception as e:
        print(f"\n❌ ERRO ao iniciar ngrok: {e}\n")
        sys.exit(1)

def main():
    """Função principal"""
    clear_screen()
    print_header()

    # Passo 1: Configurar ngrok
    configure_ngrok()

    # Passo 2: Verificar Django
    check_django()

    # Passo 3: Iniciar ngrok
    start_ngrok()

if __name__ == "__main__":
    main()
