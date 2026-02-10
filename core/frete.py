import math

TRANSPORTADORAS = {
    "PAC": 18.0, 
    "SEDEX": 35.0, 
    "JADLOG": 28.0, 
    "TOTAL EXPRESS": 26.0
}

REGIOES = {
    "São Paulo (Capital/Interior)": 1.0, 
    "Sudeste (RJ/MG/ES)": 1.3, 
    "Sul / Centro-Oeste": 1.6, 
    "Norte / Nordeste": 2.2
}

def calcular_frete_consolidado(peso_total, volumes, regiao):
    resultados = {}
    multiplicador = REGIOES.get(regiao, 1.0)
    for nome, base in TRANSPORTADORAS.items():
        valor = (base + (peso_total * 3.5) + (volumes * 5)) * multiplicador
        resultados[nome] = round(valor, 2)
    return resultados
