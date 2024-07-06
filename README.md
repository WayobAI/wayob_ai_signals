# Wayob Labs AI Signals API

## Overview
Wayob Labs AI Signals API is a development AI signal API designed to provide cryptocurrency trading signals, news reports, on-chain data analysis, and social media sentiment analysis. The API is built using FastAPI.

## Features
- **Cryptocurrency Trading Signals**: Get AI-generated trading signals for different cryptocurrencies.
- **News Reports**: Access the latest news reports related to a specific cryptocurrency.
- **On-Chain Data Analysis**: Analyze short-term and long-term on-chain data for cryptocurrencies.
- **Social Media Sentiment Analysis**: Understand the social media sentiment surrounding a specific cryptocurrency.

## Endpoints
- `/signal`: Get trading signals for a specified cryptocurrency.
    - Parameters:
        - `coin_symbol`: The symbol of the coin (e.g., `btc`).
        - `order_type`: The type of order (`market` or `limit`).
- `/news_report`: Get news reports for a specified cryptocurrency.
    - Parameters:
        - `coin_name`: The name of the coin (e.g., `bitcoin`).
- `/onchain_report`: Get on-chain reports for a specified term.
    - Parameters:
        - `term`: The term to report on (`short` or `long`).
- `/social_report`: Get social media sentiment analysis for a specified cryptocurrency.
    - Parameters:
        - `coin_name`: The name of the coin (e.g., `ethereum`).