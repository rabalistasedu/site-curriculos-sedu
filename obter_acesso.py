#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para obter os links de acesso ao site SEDU
Mostra: IP externo, ngrok URL, localhost
Executa: python obter_acesso.py
"""

import socket
import subprocess
import json
import time
import urllib.request
import urllib.error

def clear_screen():
    """Limpa a tela"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Header"""
    print("\n" + "=" * 70)
    print("  LINKS DE ACESSO - SITE CURRICULOS SEDU")
    print("=" * 70 + "\n")

def get_internal_ip():
    """Pega o IP interno da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_external_ip():
    """Pega o IP externo da máquina"""
    try:
        response = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=3)
        data = json.loads(response.read().decode())
        return data['ip']
    except:
        return "Indisponível (verifique conexão)"

def get_ngrok_url():
    """Tenta obter a URL do ngrok via API local"""
    try:
        response = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=2)
        data = json.loads(response.read().decode())

        for tunnel in data['tunnels']:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
        return None
    except:
        return None

def check_django():
    """Verifica se Django está rodando"""
    try:
        urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)
        return True
    except:
        return False

def main():
    clear_screen()
    print_header()

    # Verificar Django
    print("[VERIFICANDO...]")
    print()

    django_ok = check_django()
    if django_ok:
        print("✅ Django está rodando em http://127.0.0.1:8000/")
    else:
        print("❌ Django NÃO está rodando!")
        print("   Execute em outro CMD:")
        print("   python manage.py runserver")
        print()

    # IPs e URLs
    print()
    internal_ip = get_internal_ip()
    external_ip = get_external_ip()
    ngrok_url = get_ngrok_url()

    print("=" * 70)
    print("  🔗 LINKS PARA COMPARTILHAR COM SEU GERENTE")
    print("=" * 70)
    print()

    # Acesso Local
    print("📍 ACESSO LOCAL (mesma rede):")
    print()
    print(f"   http://{internal_ip}:8000")
    print()
    print("   ⚠️  Funciona apenas se o gerente estiver na mesma rede WiFi/LAN")
    print()

    # Acesso via IP externo
    print("🌍 ACESSO VIA IP EXTERNO (Internet):")
    print()
    print(f"   http://{external_ip}:8000")
    print()
    print("   ⚠️  Geralmente bloqueado por firewall (não recomendado)")
    print()

    # Acesso via ngrok (MELHOR)
    print("⭐ MELHOR OPÇÃO - ACESSO VIA NGROK (Internet Seguro):")
    print()

    if ngrok_url:
        print(f"   {ngrok_url}")
        print()
        print("   ✅ Funciona de qualquer lugar do mundo!")
        print("   ✅ Válido por 2 horas (versão gratuita)")
        print("   ✅ Sem configurar firewall!")
    else:
        print("   ngrok NÃO está rodando!")
        print("   Clique 2x em: BAT SEDU\\INICIAR ngrok.bat")
        print()

    print()
    print("=" * 70)
    print()

    # Instruções
    print("📋 COMO USAR:")
    print()
    print("1. Deixe Django rodando em um CMD")
    print("2. Clique 2x em: BAT SEDU\\INICIAR ngrok.bat")
    print("3. Copie o link NGROK e envie para seu gerente")
    print()

    print("📊 MONITORAR EM TEMPO REAL:")
    print()
    print("   http://127.0.0.1:4040")
    print("   (Veja todas as requisições que chegam via ngrok)")
    print()

    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
    input("Pressione ENTER para sair...")
