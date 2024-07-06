import datetime

from .constants import (
    NEWS_MODE,
    ONCHAIN_MODE,
    ONCHAIN_QUESTION,
    SIGNAL_MODE,
    SIGNAL_QUESTION,
    SOCIAL_MODE,
)
from .llm import AIChatbot
from .tools import get_signal_market_data, get_signal_limit_data, get_onchain_data


async def signal_report(coin_symbol: str, order_type: str = "market") -> str:
    """Returns a report with a signal for a given coin."""
    ai = AIChatbot(mode=SIGNAL_MODE)

    coin_symbol = coin_symbol.lower()

    if order_type == "market":
        signal_data = get_signal_market_data(coin_symbol)
    else:
        signal_data = get_signal_limit_data(coin_symbol)

    if signal_data is None:
        return None

    input = SIGNAL_QUESTION.format(
        signal_data=str(signal_data),
    )
    response = await ai.get_response(input)
    return response


async def news_report(coin_name: str) -> str:
    """Returns a report of the news for a given coin."""
    actual_date = datetime.datetime.now().strftime("%-d %B %Y")
    ai = AIChatbot(mode=NEWS_MODE)
    response = await ai.get_response(f"{coin_name} news {actual_date}")
    return response


async def onchain_report(term: str) -> str:
    """Returns a report of the onchain data for a given 'short' or 'long'."""
    ai = AIChatbot(mode=ONCHAIN_MODE)
    onchain_data = get_onchain_data(term)
    input = ONCHAIN_QUESTION.format(
        term=term,
        indicators_data=onchain_data,
    )
    response = await ai.get_response(input)
    return response


async def social_report(coin_name: str) -> str:
    """Returns a report of the social data for a given coin."""
    ai = AIChatbot(mode=SOCIAL_MODE)
    response = await ai.get_response(f"{coin_name}")
    return response
