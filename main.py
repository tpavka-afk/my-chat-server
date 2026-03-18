import os
import asyncio
import websockets
import json

# Тот самый пароль (API-key), который мы договорились сделать
ACCESS_PASSWORD = "00000" 

# Список активных пользователей
USERS = set()

async def handler(websocket):
    try:
        # Первое, что делает сервер — ждет пароль от клиента
        auth_message = await websocket.recv()
        auth_data = json.loads(auth_message)
        
        if auth_data.get("password") != ACCESS_PASSWORD:
            await websocket.send(json.dumps({"user": "System", "text": "Wrong Password! Access Denied."}))
            await websocket.close()
            return

        # Если пароль верный, добавляем в чат
        USERS.add(websocket)
        print("Новый пользователь подключен")
        
        async for message in websocket:
            # Рассылаем сообщение всем, кто онлайн
            if USERS:
                await asyncio.wait([user.send(message) for user in USERS])
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if websocket in USERS:
            USERS.remove(websocket)

async def main():
    # Порт для Render
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
    
