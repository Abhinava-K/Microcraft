from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from app.services.mfapi import search_schemes, get_scheme_history, calculate_cagr_since_inception
from app.services.coingecko import get_crypto_prices
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize the Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

@tool
async def search_mutual_funds_tool(query: str) -> str:
    """Search for mutual funds by name and return top results with 3Y CAGR."""
    try:
        results = await search_schemes(query)
        if not results: return "No funds found."
        top_results = results[:3]
        
        info = []
        for fund in top_results:
            hist = await get_scheme_history(fund['schemeCode'])
            cagr = calculate_cagr_since_inception(hist)
            info.append(f"Name: {fund['schemeName']} | Code: {fund['schemeCode']} | Inception CAGR: {cagr}%")
        return "\n".join(info)
    except Exception as e:
        return str(e)

@tool
async def get_crypto_price_tool(coin_ids: str) -> str:
    """Fetch current price and 24h change for crypto coins. coin_ids should be comma-separated like 'bitcoin,ethereum'."""
    try:
        ids = coin_ids.split(",")
        data = await get_crypto_prices(ids)
        res = []
        for coin, stats in data.items():
            res.append(f"{coin.capitalize()}: ${stats.get('usd', 0)} (24h change: {stats.get('usd_24h_change', 0)}%)")
        return "\n".join(res)
    except Exception as e:
        return str(e)

tools = [search_mutual_funds_tool, get_crypto_price_tool]
system_message = "You are an expert AI Investment Advisor. Answer the user's queries using the provided tools to fetch live data. Always format comparisons in Markdown tables. Add a disclaimer that this is not financial advice."

agent_executor = create_react_agent(llm, tools, prompt=system_message)
