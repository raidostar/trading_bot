from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/walrus")
async def walrus(request: Request):
    data = await request.json()
    print("📩 Webhook 수신됨:", data)

        # walusdt 웹훅 처리 예시
    if data.get("id") == "Long":
        print("✅ [알림] 📈 WALUSDT 롱 포지션 진입 요청 감지! 가격: ", data.get("price", "N/A"))
        # place_order(side="Buy")
    
    elif data.get("id") == "Short":
        print("✅ [알림] 📉 WALUSDT 숏 포지션 진입 요청 감지! 가격: ", data.get("price", "N/A"))
        # place_order(side="Sell")
    
    elif data.get("id") == "Long Exit":
        print("🔔 [알림] 🟡 WALUSDT 롱 포지션 종료 조건 충족! 가격: ", data.get("price", "N/A"))
        # close_position(side="Sell")
    
    elif data.get("id") == "Short Exit":
        print("🔔 [알림] 🔴 WALUSDT 숏 포지션 종료 조건 충족! 가격: ", data.get("price", "N/A"))
        # close_position(side="Buy")
    
    else:
        print("⚠️ [경고] 인식되지 않은 ID 수신: ", data.get("id"))
    

    return {"status": "ok"}
