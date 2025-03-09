from fastapi import FastAPI

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "Plaid of Receipts API is running!"}