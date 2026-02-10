from pydantic import BaseModel
from typing import List, Optional

class ItemOrcamento(BaseModel):
    fornecedor: str
    produto: str
    quantidade: int
    tamanho: str
    estampa_frente: Optional[str] = "Nenhuma"
    estampa_costas: Optional[str] = "Nenhuma"

class OrcamentoRequest(BaseModel):
    itens: List[ItemOrcamento]
    regiao: str
    forma_pagamento: str
    parcelas: int = 1

class ItemDetalhe(BaseModel):
    produto: str
    descricao: str
    tamanho: str
    fornecedor: str
    quantidade: int
    preco_unitario: float
    subtotal: float
    custo_unitario: float

class FreteOpcao(BaseModel):
    transportadora: str
    valor_frete: float
    subtotal_produtos: float
    valor_taxa: float
    venda_total: float
    custo_total: float
    lucro_total: float
    margem: float

class OrcamentoResponse(BaseModel):
    itens: List[ItemDetalhe]
    peso_total: float
    volumes: int
    regiao: str
    pagamento: str
    taxa_percentual: float
    opcoes: List[FreteOpcao]
