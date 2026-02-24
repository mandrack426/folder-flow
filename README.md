# Folder Flow

Folder Flow é uma aplicação desktop para organização automática de pastas de produtos a partir de código de barras.

## 🚀 Funcionalidades

- Leitura de base CSV ou Excel
- Busca por código de barras
- Criação automática de pasta estruturada
- Padronização de nomes (espaços substituídos por "-")
- Interface gráfica simples e rápida

## 📦 Build

O projeto possui pipeline de build automático via GitHub Actions.

São gerados:

- Windows: `FolderFlow.exe`
- Mac: `FolderFlow.app`

## 🖥️ Execução

### Windows

Execute o arquivo `FolderFlow.exe`.

### Mac

Pode ser necessário liberar o app manualmente na primeira execução:

1. Preferências do Sistema
2. Segurança e Privacidade
3. Permitir execução

## 🏗️ Estrutura do Projeto

domain/
application/
infrastructure/
presentation/
.github/
main.py
