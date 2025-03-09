from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Plaid of Receipts API is running!"}