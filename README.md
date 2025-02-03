# Stellar Trades Stream Discord Bot

This bot streams large trades from the Stellar DEX to a Discord channel using webhooks. It monitors trades involving a specific token and sends alerts when the trade amount exceeds a specified minimum.

## Features

- Streams trades from the Stellar DEX in real-time.
- Sends alerts to a Discord channel using webhooks.
- Configurable token symbol, issuer, and minimum trade amount.
- Provides trade details including amount, price, and transaction link.

## Requirements

- Python 3.7+
- `stellar-sdk[aiohttp]`
- `python-dotenv`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Stellar-Trades-Stream-Discord-Bot.git
    cd Stellar-Trades-Stream-Discord-Bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Edit the `.env` file in the project directory and add your configuration:
    ```properties
    WEBHOOK_URL=your_discord_webhook_url
    BUY_URL=your_buy_url
    EXPLORER_URL=desired_explorer_url
    TOKEN_SYMBOL=your_token_symbol
    TOKEN_ISSUER=your_token_issuer_address
    MIN_AMOUNT=minimum_amount_to_stream
    ```

4. Edit the `cursor.json` file in the project directory to store the last processed cursor:
    ```json
    {
        "LAST_CURSOR": "now"
    }
    ```

## Usage

Run the bot using the following command:
```sh
python main.py
```

The bot will start streaming trades and sending alerts to the configured Discord webhook.

## Configuration

- `WEBHOOK_URL`: The Discord webhook URL to send alerts to.
- `BUY_URL`: The URL for buying the token.
- `EXPLORER_URL`: The URL for exploring the token on Stellar.
- `TOKEN_SYMBOL`: The symbol of the token to monitor.
- `TOKEN_ISSUER`: The issuer account of the token.
- `MIN_AMOUNT`: The minimum trade amount to trigger an alert.

## License

This project is licensed under the MIT License.
