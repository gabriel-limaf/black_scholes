import numpy as np
from scipy.stats import norm
import yfinance as yf


def volatility():
    # Obtenha os preços históricos da ação
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    # Calcule os retornos diários
    stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()
    # Calcule a volatilidade usando o desvio padrão dos retornos diários
    sigma = stock_data['Daily_Return'].std()
    print(f"Volatilidade histórica de {ticker_symbol} durante o período de {start_date} a {end_date}: {sigma:.4f}")
    return sigma


def current_price():
    stock = yf.Ticker(ticker_symbol)
    # Acesse as informações atuais da ação
    S = stock.history(period="1d")["Close"][0]
    print(f"Preço atual de {ticker_symbol}: {S:.4f}")
    return S


def black_scholes_call(sigma, S, K, T, r):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    fair_value = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return fair_value


#  Parâmetros
ticker_symbol = str(input('Qual o código do ticker? ')) + '.SA'
start_date = str(input('Qual a data de inicio para calcular a volatilidade da ação (Escreva no formato AAAA-MM-DD?)'))
end_date = str(input('Qual a data de término para calcular a volatilidade da ação (Escreva no formato AAAA-MM-DD?)'))
K = float(input('Qual o preço de exercicio da opção? (Separe o valor por . e não ,)'))
T = float(input('Tempo até a expiração da opção em anos? (Separe o valor por . e não ,)'))
r = float(input('Qual a taxa de juros livre de risco (Selic)? (Separe o valor por . e não ,)'))
fair_value = black_scholes_call(volatility(), current_price(), K, T, r)
print(f"Fair value da opção de compra: R$ {fair_value:.4f}")
