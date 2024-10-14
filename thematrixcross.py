import requests
import time
import numpy as np
from datetime import datetime, timedelta
import traceback

# Constants
API_URL = "https://api.binance.com/api/v3"
TELEGRAM_TOKEN = "7584193648:AAHPS_awtYRVJN02KPeLhUe7RSbRa3EN3tY"
CHANNEL_ID = "-1002480885898"
THREAD_ID = "134559"
RSI_PERIOD = 14
RISK_REWARD_RATIO = 2
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

def send_telegram_message(message):
    payload = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'reply_to_message_id': THREAD_ID
    }
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=payload)

def fetch_historical_data(symbol, interval='1h'):
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=5)  # Fetch 5 days of 1-hour data
        start_str = int(start_time.timestamp() * 1000)

        response = requests.get(f"{API_URL}/klines", params={
            'symbol': symbol,
            'interval': interval,
            'startTime': start_str,
            'limit': 1000
        })

        if response.status_code != 200:
            print(f"Error fetching data for {symbol}: {response.text}")
            return []

        data = response.json()
        print(f"Fetched {len(data)} data points for {symbol}")
        return [float(candle[4]) for candle in data]  # Closing prices
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        traceback.print_exc()
        return []

def calculate_moving_average(prices, period):
    if len(prices) < period:
        print(f"Not enough data to calculate MA{period}.")
        return None
    return np.mean(prices[-period:])

def calculate_rsi(prices, period):
    if len(prices) < period:
        print(f"Not enough data to calculate RSI.")
        return None
    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gain[-period:])
    avg_loss = np.mean(loss[-period:])

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

def scan_futures_pair(symbol):
    try:
        print(f"\nScanning pair: {symbol}")
        closing_prices = fetch_historical_data(symbol)

        if not closing_prices:
            print(f"No data received for {symbol}")
            return

        rsi = calculate_rsi(closing_prices, RSI_PERIOD)
        ma_50 = calculate_moving_average(closing_prices, 50)
        ma_100 = calculate_moving_average(closing_prices, 100)

        latest_price = closing_prices[-1]

        print(f"Latest Price: {latest_price:.3f}")
        print(f"MA 50: {ma_50:.3f}" if ma_50 else "MA 50: Not enough data")
        print(f"MA 100: {ma_100:.3f}" if ma_100 else "MA 100: Not enough data")
        print(f"RSI: {rsi:.2f}" if rsi else "RSI: Not enough data")

        if ma_50 is not None and ma_100 is not None:
            if ma_50 > ma_100:
                message = f"Buy Signal Detected for {symbol} 🔼\nLatest Price: {latest_price:.3f}"
                send_telegram_message(message)

            if ma_50 < ma_100:
                message = f"Sell Signal Detected for {symbol} 🔻\nLatest Price: {latest_price:.3f}"
                send_telegram_message(message)

        if rsi is not None:
            if rsi <= RSI_BUY_THRESHOLD:
                stop_loss = latest_price * 0.98
                take_profit = latest_price + (latest_price - stop_loss) * RISK_REWARD_RATIO
                message = f"RSI Buy Signal for {symbol}:\nLatest Price: {latest_price:.3f}\nStop Loss: {stop_loss:.2f}\nTake Profit: {take_profit:.2f}"
                send_telegram_message(message)

            if rsi >= RSI_SELL_THRESHOLD:
                stop_loss = latest_price * 1.02
                take_profit = latest_price - (stop_loss - latest_price) * RISK_REWARD_RATIO
                message = f"RSI Sell Signal for {symbol}:\nLatest Price: {latest_price:.3f}\nStop Loss: {stop_loss:.2f}\nTake Profit: {take_profit:.2f}"
                send_telegram_message(message)

    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")
        traceback.print_exc()

def main():
    trading_pairs = [
        'BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'ETCUSDT', 'LTCUSDT', 'XRPUSDT',
        'FETUSDT', 'BNBUSDT', 'ALGOUSDT', 'DOGEUSDT', 'CKBUSDT', 'QTUMUSDT',
        'COMPUSDT', 'XTZUSDT', 'ADAUSDT', 'LINKUSDT', 'DOTUSDT', 'UNIUSDT',
        'FILUSDT', 'EOSUSDT', 'TRXUSDT', 'GMTUSDT', 'APEUSDT', 'KNCUSDT',
        'GTCUSDT', 'XLMUSDT', 'XMRUSDT', 'VETUSDT', 'NEOUSDT', 'THETAUSDT',
        'ZILUSDT', 'ZRXUSDT', 'KAVAUSDT', 'BANDUSDT', 'MKRUSDT', 'SNXUSDT',
        'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT',
        'STORJUSDT', 'AVAXUSDT', 'FTMUSDT', 'FLMUSDT', 'KSMUSDT', 'NEARUSDT',
        'AAVEUSDT', 'RSRUSDT', 'LRCUSDT', 'BELUSDT', 'AXSUSDT', 'GRTUSDT',
        '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'LITUSDT', 'UNFIUSDT', 'REEFUSDT',
        'RVNUSDT', 'MANAUSDT', 'OGNUSDT', 'NKNUSDT', '1000SHIBUSDT', 'ICPUSDT',
        'BAKEUSDT', 'TLMUSDT', 'C98USDT', 'MASKUSDT', 'DYDXUSDT', 'GALAUSDT',
        'ARUSDT', 'ARPUSDT', 'ENSUSDT', 'PEOPLEUSDT', 'ROSEUSDT', 'ATOMUSDT',
        'JASMYUSDT', 'DARUSDT', 'OPUSDT', '1000LUNCUSDT', 'LUNA2USDT', 'FLOWUSDT',
        'STGUSDT', 'APTUSDT', 'QNTUSDT', 'INJUSDT', 'LDOUSDT', 'HOOKUSDT',
        'MAGICUSDT', 'STXUSDT', 'ACHUSDT', 'SSVUSDT', 'USDCUSDT', 'FLOKIUSDT',
        'ARBUSDT', 'IDUSDT', 'JOEUSDT', 'AMBUSDT', 'LEVERUSDT', 'BLURUSDT',
        'SUIUSDT', '1000PEPEUSDT', 'ORDIUSDT', 'WOOUSDT', 'WLDUSDT', 'PENDLEUSDT',
        'AGLDUSDT', 'ARKMUSDT', 'HIGHUSDT'
    ]

    while True:
        print("\nStarting new scan cycle...")
        for pair in trading_pairs:
            scan_futures_pair(pair)
            time.sleep(2)  # Avoid API rate limit errors

        time.sleep(60)  # Wait for 60 seconds before starting another scan cycle

if __name__ == "__main__":
    main()