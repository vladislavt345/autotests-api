from dotenv import dotenv_values
import uvicorn

config = dotenv_values(".env")  # Загружаем .env как словарь

host = config.get("HOST", "127.0.0.1")
port = int(config.get("PORT", 8000))
reload = config.get("RELOAD", "False").lower() == "true"

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
