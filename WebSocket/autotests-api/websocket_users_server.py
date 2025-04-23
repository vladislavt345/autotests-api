import asyncio
import websockets


# Обработчик входящих сообщений
async def handle_connection(websocket):
    async for message in websocket:
        print(f"Получено сообщение от пользователя: {message}")
        
        # Отправляем 5 ответных сообщений
        for i in range(1, 6):
            response = f"{i} Сообщение от сервера: {message}"
            await websocket.send(response)


# Запуск WebSocket-сервера на порту 8765
async def main():
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket сервер запущен на ws://localhost:8765")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())