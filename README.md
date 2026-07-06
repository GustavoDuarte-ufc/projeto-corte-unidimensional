# Projeto Acadêmico de Corte Unidimensional

Este projeto é uma aplicação acadêmica para demonstrar a resolução do problema de corte unidimensional, combinando uma API backend, uma interface web frontend e um solver de otimização.

# Link

## API
https://projeto-corte-unidimensional.onrender.com/
## WEB
https://projeto-corte-unidimensional-git-main-corte-uni.vercel.app/

## Objetivo

O sistema permite cadastrar itens com comprimento e quantidade, calcular o melhor aproveitamento de barras padrão e retornar um plano de corte otimizado. A solução foi implementada como um exemplo prático de aplicação de algoritmos e arquitetura web.

## Funcionalidades

- Autenticação de usuários com JWT
- Cadastro e login
- Geração de padrões de corte
- Cálculo de barras necessárias e desperdício
- Interface web para interação com o sistema
- Testes automatizados para o backend

## Tecnologias utilizadas

### Backend
- Python
- FastAPI
- MongoDB com Motor
- Pydantic
- Passlib / bcrypt
- OR-Tools
- Pytest

### Frontend
- React
- Vite
- React Router
- Axios

## Estrutura do projeto

- backend/: API, serviços, modelos, banco de dados e testes
- frontend/: aplicação web em React/Vite

## Pré-requisitos

- Python 3.10+
- Node.js 18+
- MongoDB acessível

## Como executar

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API ficará disponível em:
- http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

A interface ficará disponível em:
- http://localhost:5173

## Testes

Para executar os testes do backend:

```bash
cd backend
pytest -q
```

## Observação

Este projeto foi desenvolvido com fins acadêmicos, servindo como exemplo de integração entre backend, frontend, banco de dados e otimização computacional.
