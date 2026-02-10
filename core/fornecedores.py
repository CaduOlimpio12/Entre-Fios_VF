FORNECEDORES = {
    "QUALIJU": {
        "Básica Algodão": {"valor": 19.40, "base": 16.52, "curva": 0.80},
        "Poliviscose": {"valor": 17.20, "base": 16.52, "curva": 0.80},
        "Poliéster": {"valor": 13.40, "base": 16.52, "curva": 0.80},
        "Poliviscose Manga Longa": {"valor": 18.90, "base": 16.52, "curva": 0.95},
        "Manga Longa UV": {"valor": 31.90, "base": 16.53, "curva": 1.50},
        "Dry Fit": {"valor": 18.60, "base": 16.52, "curva": 0.80},
        "Oversized 165g": {"valor": 22.90, "base": 16.53, "curva": 1.15},
        "Oversized 200g": {"valor": 31.90, "base": 16.53, "curva": 1.15},
        "Cropped Femino": {"valor": 14.50, "base": 16.52, "curva": 0.80},
        "Baby Look Feminina": {"valor": 14.80, "base": 16.52, "curva": 0.80},
        "Básica Infantil Algodão": {"valor": 12.90, "base": 16.52, "curva": 0.79},
        "Regata Básica": {"valor": 16.60, "base": 16.52, "curva": 0.80},
        "Baby Look Feminina Gola V": {"valor": 14.80, "base": 16.52, "curva": 0.80},
        "Manga Longa em Algodão": {"valor": 18.90, "base": 16.52, "curva": 0.95},
        "Gola Polo": {"valor": 25.00, "base": 16.52, "curva": 0.95}
    },
    "USMARK": {
        "Street Wear": {
            "faixas": {9: 38.50, 10: 23.87, 25: 21.56, 50: 20.41, 100: 20.02, 500: 19.25},
            "base": 18.40, "curva": 0.99
        },
        "Básica Masculina Regular Fit": {
            "faixas": {9: 36.85, 10: 22.85, 25: 20.64, 50: 19.53, 100: 19.16, 500: 18.43},
            "base": 21.32, "curva": 0.64
        },
        "Dry Fit UV": {
            "faixas": {9: 24.00, 10: 14.88, 25: 13.44, 50: 12.72, 100: 12.48, 500: 12.00},
            "base": 20.61, "curva": 0.60
        },
        "Gola Polo": {
            "faixas": {9: 53.90, 10: 33.42, 25: 30.18, 50: 28.57, 100: 28.03, 500: 26.95},
            "base": 27.84, "curva": 1.14
        },
        "Básica Oversized Malhão": {
            "faixas": {9: 55.55, 10: 34.44, 25: 31.11, 50: 29.44, 100: 28.89, 500: 27.78},
            "base": 23.33, "curva": 1.08
        },
        "Básica Plus Size": {
            "faixas": {9: 49.23, 10: 30.52, 25: 27.57, 50: 26.09, 100: 25.60, 500: 24.62},
            "base": 25.05, "curva": 0.82
        },
        "Básica Infantil": {
            "faixas": {9: 25.50, 10: 15.81, 25: 14.28, 50: 13.52, 100: 13.26, 500: 12.75},
            "base": 20.28, "curva": 0.58
        },
        "Bermuda Tactel": {
            "faixas": {9: 44.55, 10: 27.62, 25: 24.95, 50: 23.61, 100: 23.17, 500: 22.88},
            "base": 19.48, "curva": 0.89
        },
        "Moletom Canguru com Capuz": {
            "faixas": {9: 99.90, 10: 61.94, 25: 55.94, 50: 52.95, 100: 51.95, 500: 49.95},
            "base": 17.60, "curva": 2.00
        },
        "Moletom Gola Careca 3 Cabos": {
            "faixas": {9: 87.18, 10: 54.05, 25: 48.82, 50: 46.21, 100: 45.33, 500: 43.59},
            "base": 27.19, "curva": 1.34
        },
        "Básica Feminina": {
            "faixas": {9: 30.94, 10: 19.18, 25: 17.33, 50: 16.40, 100: 16.09, 500: 15.47},
            "base": 21.31, "curva": 0.56
        }
    },
    "MN POLOS": {
        "Gola Polo Masculina": {"valor": 25.00, "base": 16.52, "curva": 0.90},
        "Gola Polo Feminina Baby Look": {"valor": 20.00, "base": 16.52, "curva": 0.90},
        "Básica Algodão": {"valor": 14.00, "base": 16.52, "curva": 0.90},
        "Dry Fit": {"valor": 15.00, "base": 16.52, "curva": 0.80}
    }
}

def get_preco_usmark(produto, quantidade):
    if produto not in FORNECEDORES["USMARK"]:
        return 0, 0, 0
    dados = FORNECEDORES["USMARK"][produto]
    faixas = sorted(dados["faixas"].items())
    preco = faixas[-1][1]
    for q_limite, p_valor in faixas:
        if quantidade <= q_limite:
            preco = p_valor
            break
    return preco, dados["base"], dados["curva"]
