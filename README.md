# 🧮 Calculadora API

API REST de calculadora desenvolvida com **FastAPI** e **Python**.

> Projeto Avaliativo desenvolvido para disciplina Programação de Sistemas Distribuídos da Universidade do Grandes Lagos - UNILAGO sob supervisão do Professor Gleydes Oliveira — [@gleydes](https://github.com/gleydes)

---

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/calculadora-api.git
cd calculadora-api
```

### 2. Crie e ative o ambiente virtual
```bash
# Criar
python -m venv venv

# Ativar — Linux/macOS
source venv/bin/activate

# Ativar — Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor
```bash
uvicorn main:app --reload
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## 📖 Documentação interativa

| URL | Descrição |
|-----|-----------|
| [/docs](http://localhost:8000/docs) | Swagger UI |
| [/redoc](http://localhost:8000/redoc) | ReDoc |
| [/openapi.json](http://localhost:8000/openapi.json) | Especificação OpenAPI |

---

## 📡 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Mensagem de boas-vindas |
| POST | `/somar` | Soma dois números |
| POST | `/subtrair` | Subtrai dois números |
| POST | `/multiplicar` | Multiplica dois números |
| POST | `/dividir` | Divide dois números (valida divisão por zero) |
| GET | `/calcular` | Realiza operação via query parameters |

### Exemplo de requisição (POST)
```json
POST /somar
{
  "numero1": 10,
  "numero2": 5
}
```

### Exemplo de resposta
```json
{
  "operacao": "soma",
  "numero1": 10.0,
  "numero2": 5.0,
  "resultado": 15.0
}
```

### Exemplo via query parameter
```
GET /calcular?numero1=20&numero2=4&operacao=divisao
```

---

## 🛠️ Tecnologias

- [Python 3.8+](https://www.python.org/)
- [FastAPI 0.115](https://fastapi.tiangolo.com/)
- [Uvicorn 0.30](https://www.uvicorn.org/)
- [Pydantic 2.9](https://docs.pydantic.dev/)
