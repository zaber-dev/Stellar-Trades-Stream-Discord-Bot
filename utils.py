import os
import time
import requests
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("WEBHOOK_URL")
buy_url = os.getenv("BUY_URL")
explorer = os.getenv("EXPLORER_URL")


async def send_webhook(payload):
    while True:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            return
        else:
            print(f"Failed to send webhook. Status code: {response.status_code}. Retrying...")
            await asyncio.sleep(5)


async def get_last_cursor():
    try:
        with open("cursor.json", "r") as file:
            data = json.load(file)
            return data.get("LAST_CURSOR", "now")
    except Exception as e:
        print(f"Error fetching last cursor: {e}")
        return "now"


async def update_cursor(cursor):
    cursor = str.split(cursor, "-")[0]
    try:
        with open("cursor.json", "w") as file:
            json.dump({"LAST_CURSOR": cursor}, file)
    except Exception as e:
        print(f"Error updating cursor: {e}")


def create_embed_payload(typet, pool, fromt, color, xlm_amount, ovrl_amount, price, tx_hash, timestamp, cursor):
    return {
        "embeds": [
            {
                "title": f":{'scales' if pool == 'Trade' else 'repeat'}: New Large {pool} Alert!",
                "description": f"Someone **{typet}** OVRL from the {fromt} on Stellar DEX!",
                "color": color,
                "fields": [
                    {
                        "name": "Spent",
                        "value": f"**{str(xlm_amount) + ' XLM' if typet == 'Bought' else str(ovrl_amount) + ' OVRL'}**",
                        "inline": True
                    },
                    {
                        "name": "Received",
                        "value": f"**{str(ovrl_amount) + ' OVRL' if typet == 'Bought' else str(xlm_amount) + ' XLM'}**",
                        "inline": True
                    },
                    {
                        "name": "Price",
                        "value": f"**{price} XLM/OVRL**",
                        "inline": False
                    },
                    {
                        "name": " ",
                        "value": f"[**Tx**]({tx_hash}) | [**Buy OVRL**]({buy_url}) | [**Token Explorer**]({explorer})"
                    }
                ],
                "footer": {
                    "text": f"Trade Time: {timestamp} | Cursor: {cursor}"
                },
            }
        ]
    }
