import os
from fastapi import FastAPI
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure Plaid Client
configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET")
    }
)
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "Plaid of Receipts API is running!"}

# Endpoint to create a Plaid link token
@app.post("/plaid/create_link_token")
def create_link_token():
    request = LinkTokenCreateRequest(
        user={"client_user_id": "unique_user_id"},
        client_name="Plaid Receipts API",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en",
    )
    response = plaid_client.link_token_create(request)
    return response.to_dict()

# NEW: Endpoint to exchange public_token for access_token
@app.post("/plaid/exchange_public_token")
def exchange_public_token(public_token: dict):
    request = ItemPublicTokenExchangeRequest(public_token=public_token["public_token"])
    response = plaid_client.item_public_token_exchange(request)
    return {"access_token": response["access_token"], "item_id": response["item_id"]}