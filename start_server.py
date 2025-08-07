#!/usr/bin/env python3
"""
Script para iniciar o servidor de suporte técnico Cisco
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Verificar se estamos no diretório correto
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"
    
    if not backend_dir.exists():
        print("❌ Erro: Diretório 'backend' não encontrado!")
        print("Certifique-se de estar executando este script na raiz do projeto.")
        sys.exit(1)
    
    # Verificar se o arquivo .env existe
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  Aviso: Arquivo .env não encontrado!")
        print("Copie o arquivo env.example para .env e configure sua chave da OpenAI:")
        print("cp env.example .env")
        print("Depois edite o arquivo .env com sua chave da API OpenAI.")
        print()
    
    # Verificar se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Erro: Variável OPENAI_API_KEY não configurada!")
        print("Configure sua chave da API OpenAI no arquivo .env")
        sys.exit(1)
    
    print("🚀 Iniciando Sistema de Suporte Técnico Cisco...")
    print("📍 Servidor rodando em: http://localhost:8000")
    print("📖 Documentação da API: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print()
    print("💡 Para acessar o frontend, abra o arquivo frontend/index.html no seu navegador")
    print("   ou execute: python -m http.server 8080 e acesse http://localhost:8080/frontend/")
    print()
    print("⏹️  Para parar o servidor, pressione Ctrl+C")
    print("-" * 60)
    
    # Iniciar o servidor
    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar o servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
