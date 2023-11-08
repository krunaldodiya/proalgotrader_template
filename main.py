import uvicorn

from proalgotrader_manager.main import app

app.state = {"host": "127.0.0.1", "port": 5555}

if __name__ == "__main__":
    uvicorn.run(app, host=app.state["host"], port=app.state["port"])
