import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.app:app", port=8080, reload=True, host="192.168.1.4")