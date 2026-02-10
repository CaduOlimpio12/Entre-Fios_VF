from fastapi import FastAPI, HTTPException
from api.schemas import OrcamentoRequest, OrcamentoResponse
from services.orcamento import gerar_orcamento_consolidado

app = FastAPI(title="API Entre-Fios")

@app.post("/orcamento", response_model=OrcamentoResponse)
def criar_orcamento(dados: OrcamentoRequest):
    try:
        itens_dict = [item.model_dump() for item in dados.itens]
        return gerar_orcamento_consolidado(itens=itens_dict, regiao=dados.regiao, forma_pagamento=dados.forma_pagamento, parcelas=dados.parcelas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
