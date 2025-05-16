from fastapi import FastAPI, Request
import requests
import time
import hmac
import hashlib
import os

app = FastAPI()

# === Bybit 테스트넷 API 키 설정 ===
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY") or "YOUR_TESTNET_API_KEY"
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET") or "YOUR_TESTNET_API_SECRET"
BYBIT_URL = "https://api-testnet.bybit.com"  # 테스트넷 전용 URL

# === 공통 서명 생성 함수 ===
def sign(params, secret):
    sorted_params = sorted(params.items())
    query = "&".join([f"{k}={v}" for k, v in sorted_params])
    return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

# === 시장가 주문 함수 ===
def place_order(side: str, symbol="WALUSDT", qty="5"):
    url = BYBIT_URL + "/v5/order/create"
    timestamp = str(int(time.time() * 1000))
    params = {
        "apiKey": BYBIT_API_KEY,
        "timestamp": timestamp,
        "category": "linear",
        "symbol": symbol,
        "side": side,  # "Buy" or "Sell"
        "orderType": "Market",
        "qty": qty,
        "timeInForce": "IOC",
    }
    params["sign"] = sign(params, BYBIT_API_SECRET)

    try:
        res = requests.post(url, params=params)
        print("📦 주문 응답:", res.status_code, res.text)
    except Exception as e:
        print("❌ 주문 실패:", str(e))

# === FastAPI Webhook 엔드포인트 ===
@app.post("/walrus")
async def walrus(request: Request):
    try:
        body = await request.body()
        if not body:
            print("⚠️ 빈 본문 수신됨 (본문 없음)")
            return {"error": "empty body"}

        data = await request.json()
        print("📩 Webhook 수신됨:", data)

        symbol = data.get("symbol", "WALUSDT")
        price = data.get("price", "N/A")
        order_id = data.get("id")

        if order_id == "Long":
            print(f"✅ [롱 진입 요청] {symbol} @ {price}")
            # place_order(side="Buy", symbol=symbol)
        elif order_id == "Short":
            print(f"✅ [숏 진입 요청] {symbol} @ {price}")
            # place_order(side="Sell", symbol=symbol)
        elif order_id == "Long Exit":
            print(f"🔔 [롱 종료 요청] {symbol} @ {price}")
            # place_order(side="Sell", symbol=symbol)
        elif order_id == "Short Exit":
            print(f"🔔 [숏 종료 요청] {symbol} @ {price}")
            # place_order(side="Buy", symbol=symbol)
        else:
            print(f"⚠️ [경고] 인식되지 않은 ID: {order_id}")

        return {"status": "ok"}

    except Exception as e:
        print("❌ 요청 처리 중 오류:", str(e))
        return {"error": str(e)}
