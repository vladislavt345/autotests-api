import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"  # url сервера
    async with websockets.connect(uri) as websocket:
        message = "Hola-hola"  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Отправляем сообщение

        # Получаем 5 ответных сообщений от сервера
        for _ in range(5):
            message = await websocket.recv()
            print(message)


if __name__ == "__main__":
    asyncio.run(client())