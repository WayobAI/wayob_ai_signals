import logging

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from wayob_ai_signals.constants import INTERNAL_API_PORT, SSL_CERT, SSL_KEY
from wayob_ai_signals.reports import (
    news_report,
    onchain_report,
    signal_report,
    social_report,
)
from wayob_ai_signals.tools import extract_investment_details

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

app = FastAPI(
    title='Wayob Labs AI.',
    description='Development AI signal API.',
    version='1.2.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/signal")
async def signal_endpoint(
    coin_symbol: str = Query(
        ...,
        description="The symbol of the coin to get the signal for",
        example="btc",
    ),
    order_type: str = Query(
        ...,
        description="The type of order",
        example="limit",
        enum=["market", "limit"],
    ),
):
    ai_reponse = await signal_report(coin_symbol, order_type=order_type)
    if ai_reponse is None:
        return f"No data found for {coin_symbol}"
    elif ai_reponse == "Sorry, I couldn't process your request. Please try again later.":
        return ai_reponse
    details = extract_investment_details(ai_reponse)

    details["order_type"] = order_type
    details["ai_message"] = ai_reponse

    return details


@app.get("/news_report")
async def news_report_endpoint(
    coin_name: str = Query(
        ...,
        description="The name of the coin to get the news report for",
        example="bitcoin",
    ),
):
    return await news_report(coin_name)


@app.get("/onchain_report")
async def onchain_report_endpoint(
    term: str = Query(
        ...,
        description="The term to report on",
        example="short",
        enum=["short", "long"],
    ),
):
    return await onchain_report(term.lower())


@app.get("/social_report")
async def social_report_endpoint(
    coin_name: str = Query(
        ...,
        description="The name of the coin to get the social report for",
        example="ethereum",
    ),
):
    return await social_report(coin_name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=INTERNAL_API_PORT,
        ssl_keyfile=SSL_KEY,
        ssl_certfile=SSL_CERT,
    )
