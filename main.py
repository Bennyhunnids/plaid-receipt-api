import os
from fastapi import FastAPI
from plaid import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Plaid Client
plaid_client = Client(
    client_id=os.getenv("PLAID_CLIENT_ID"),
    secret=os.getenv("PLAID_SECRET"),
    environment=os.getenv("PLAID_ENV", "sandbox")
)

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "Plaid of Receipts API is running!"}

@app.post("/plaid/create_link_token")
def create_link_token():
    response = plaid_client.LinkToken.create({
        "user": {"client_user_id": "unique_user_id"},
        "client_name": "Plaid Receipts API",
        "products": ["transactions"],
        "country_codes": ["US"],
        "language": "en",
    })
    return response