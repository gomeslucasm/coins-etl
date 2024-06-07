## Visão Geral

Este projeto implementa pipelines ETL (Extract, Transform, Load) utilizando a ferramenta Prefect para orquestração de fluxos de trabalho. O objetivo principal é extrair dados de preços de criptomoedas da API CoinGecko, transformá-los para calcular indicadores técnicos como SMA e RSI, e carregar esses dados em um banco de dados para armazenamento e análise. Alertas são enviados com base nos indicadores técnicos para notificar sobre condições de compra e venda.

## Arquitetura

A arquitetura do sistema é baseada no padrão ETL (Extract, Transform, Load), onde dados são extraídos de uma fonte externa (API do CoinGecko), transformados para gerar indicadores técnicos e insights, e finalmente carregados em um banco de dados para armazenamento e análise. O sistema é construído utilizando Prefect, uma ferramenta de orquestração de fluxo de trabalho, para gerenciar e automatizar as tarefas ETL.

Os principais componentes da arquitetura são:

    1. Extração de Dados: Coleta de dados de criptomoedas utilizando a API do CoinGecko.
    2. Transformação de Dados: Processamento e cálculo de indicadores técnicos (SMA, RSI).
    3. Carga de Dados: Armazenamento dos dados transformados em um banco de dados.
    4. Notificações: Envio de alertas baseados em indicadores técnico

### Fluxos Implementados

#### Fluxo 1: trending_coins_market_data

Este fluxo orquestra a busca de moedas em tendência e seus dados de mercado. O fluxo realiza os seguintes passos:

    1. Fetch Trending Coins: Busca as moedas em tendência usando a API CoinGecko.
    2. Format Trending Coins Data: Formata os dados das moedas em tendência.
    3. Save Coins Trending: Salva os dados das moedas em tendência no banco de dados.
    4. Send Price Change Alerts: Envia alertas se a variação percentual do preço em USD exceder o limiar especificado.rket_chart_price_indicator salva os indicadores técnicos calculados no banco de dados.

#### Fluxo 2: analyze_bitcoin_prices

Descrição

Este fluxo analisa os preços históricos do Bitcoin e calcula indicadores técnicos. O fluxo realiza os seguintes passos:

    1. Fetch Historical Prices: Busca os preços históricos do Bitcoin em USD nos últimos 30 dias.
    2. Format Market Chart Data: Formata os dados do gráfico de mercado.
    3. Calculate Price Indicators: Calcula indicadores técnicos como RSI e SMA.
    4. Save Market Chart Price Indicator: Salva o indicador de preço mais recente no banco de dados.
    5. Send RSI Alert: Envia alertas de RSI com base nos indicadores calculados.

## Como executar

...