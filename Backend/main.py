from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI(
    title="Calculadora API",
    description="API de Calculadora para Sistemas Distribuídos — com histórico SQLite",
    version="2.0.0"
)


DB_PATH = "calculadora.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            operacao  TEXT    NOT NULL,
            numero1   REAL    NOT NULL,
            numero2   REAL    NOT NULL,
            resultado REAL    NOT NULL,
            criado_em TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def salvar_calculo(operacao: str, numero1: float, numero2: float, resultado: float):
    conn = get_connection()
    conn.execute(
        "INSERT INTO historico (operacao, numero1, numero2, resultado, criado_em) VALUES (?, ?, ?, ?, ?)",
        (operacao, numero1, numero2, resultado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

inicializar_banco()


class OperacaoRequest(BaseModel):
    numero1: float
    numero2: float

class ResultadoResponse(BaseModel):
    operacao: str
    numero1: float
    numero2: float
    resultado: float
    criado_em: str


app = FastAPI(
    title="Calculadora API",
    description="API de Calculadora para Sistemas Distribuídos — com histórico SQLite",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],          
)


@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à Calculadora API!", "docs": "/docs"}


@app.post("/somar", response_model=ResultadoResponse)
def somar(dados: OperacaoRequest):
    resultado = dados.numero1 + dados.numero2
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_calculo("soma", dados.numero1, dados.numero2, resultado)
    return ResultadoResponse(
        operacao="soma", 
        numero1=dados.numero1, 
        numero2=dados.numero2, 
        resultado=resultado, 
        criado_em=criado_em
    )


@app.post("/subtrair", response_model=ResultadoResponse)
def subtrair(dados: OperacaoRequest):
    resultado = dados.numero1 - dados.numero2
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_calculo("subtracao", dados.numero1, dados.numero2, resultado)
    return ResultadoResponse(
        operacao="subtracao", 
        numero1=dados.numero1, 
        numero2=dados.numero2, 
        resultado=resultado, 
        criado_em=criado_em    
    )


@app.post("/multiplicar", response_model=ResultadoResponse)
def multiplicar(dados: OperacaoRequest):
    resultado = dados.numero1 * dados.numero2
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_calculo("multiplicacao", dados.numero1, dados.numero2, resultado)
    return ResultadoResponse(
        operacao="multiplicacao", 
        numero1=dados.numero1, 
        numero2=dados.numero2, 
        resultado=resultado, 
        criado_em=criado_em
    )


@app.post("/dividir", response_model=ResultadoResponse)
def dividir(dados: OperacaoRequest):
    if dados.numero2 == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não é permitida!")
    resultado = dados.numero1 / dados.numero2
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_calculo("divisao", dados.numero1, dados.numero2, resultado)
    return ResultadoResponse(
        operacao="divisao",
        numero1=dados.numero1, 
        numero2=dados.numero2, 
        resultado=resultado, 
        criado_em=criado_em
    )


@app.get("/calcular", response_model=ResultadoResponse)
def calcular_query(numero1: float, numero2: float, operacao: str):
    operacoes = {
        "soma":          lambda a, b: a + b,
        "subtracao":     lambda a, b: a - b,
        "multiplicacao": lambda a, b: a * b,
        "divisao":       lambda a, b: a / b,
    }

    if operacao not in operacoes:
        raise HTTPException(
            status_code=400, 
            detail=f"Operação inválida. Use: {list(operacoes.keys())}"
        )
    
    if operacao == "divisao" and numero2 == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não é permitida!")
    
    resultado = operacoes[operacao](numero1, numero2)
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    salvar_calculo(operacao, numero1, numero2, resultado)

    return ResultadoResponse(
        operacao=operacao,
        numero1=numero1,
        numero2=numero2,
        resultado=resultado,
        criado_em=criado_em
    )


@app.get("/historico")
def listar_historico(limite: int = 20):
    """Retorna os últimos cálculos realizados (padrão: 20 registros)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM historico ORDER BY id DESC LIMIT ?", (limite,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.delete("/historico")
def limpar_historico():
    """Apaga todo o histórico de cálculos."""
    conn = get_connection()
    conn.execute("DELETE FROM historico")
    conn.commit()
    conn.close()
    return {"mensagem": "Histórico apagado com sucesso!"}
