import asyncio
from datetime import datetime
from stellar_sdk import AiohttpClient, ServerAsync, Asset
from dotenv import load_dotenv
import os
from utils import send_webhook, get_last_cursor, update_cursor, create_embed_payload

load_dotenv()

HORIZON_URL = "https://horizon.stellar.org"
SYMBOL = os.getenv("TOKEN_SYMBOL")
ISSUER = os.getenv("TOKEN_ISSUER")
OVRL = Asset(SYMBOL, ISSUER)
XLM = Asset.native()
MIN_AMOUNT = float(os.getenv("MIN_AMOUNT"))


async def judge(tx):
    ovrl_amount = tx['base_amount']
    xlm_amount = tx['counter_amount']
    price = round(float(int(tx['price']['n']) / int(tx['price']['d'])), 7)
    typet = "Bought" if tx['base_is_seller'] else "Sold"
    pool = "Trade" if tx['trade_type'] == "orderbook" else "Swap"
    fromt = "Order Book" if tx['trade_type'] == "orderbook" else "Liquidity Pool"
    color = 0x33FF57 if tx['base_is_seller'] else 0xFF5733
    tx_hash = f"https://lumenscan.io/ops/{tx['id'].split('-')[0]}"
    timestamp = datetime.fromisoformat(tx['ledger_close_time'].replace('Z', '')).strftime('%Y-%m-%d %H:%M:%S UTC')
    cursor = tx['paging_token']

    embed_payload = create_embed_payload(typet, pool, fromt, color, xlm_amount, ovrl_amount, price, tx_hash, timestamp, cursor)

    if float(ovrl_amount) >= float(MIN_AMOUNT):
        await send_webhook(embed_payload)
    await update_cursor(cursor)


async def trades():
    last_cursor = await get_last_cursor()
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        print("connected")
        async for trade in server.trades().for_asset_pair(OVRL, XLM).cursor(cursor=last_cursor).stream():
            await judge(trade)


async def listen():
    await asyncio.gather(trades())


if __name__ == "__main__":
    asyncio.run(listen())