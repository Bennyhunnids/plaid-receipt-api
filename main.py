from fastapi import FastAPI, HTTPException
import os
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from dotenv import load_dotenv
from plaid import ApiClient, Configuration

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Plaid Configuration
configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET")
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Store access tokens in memory (for testing)
ACCESS_TOKENS = {}

# Root Route
@app.get("/")
def read_root():
    return {"message": "Plaid of Receipts API is running!"}

# Create Link Token
@app.post("/plaid/create_link_token")
def create_link_token():
    request = LinkTokenCreateRequest(
        client_name="Plaid Test App",
        language="en",
        country_codes=[CountryCode('US')],
        user=LinkTokenCreateRequestUser(client_user_id="user-id"),
        products=[Products('transactions')]
    )
    response = client.link_token_create(request)
    return response.to_dict()

# Exchange Public Token
@app.post("/plaid/exchange_public_token")
def exchange_public_token(public_token: dict):
    try:
        request = ItemPublicTokenExchangeRequest(public_token=public_token["public_token"])
        response = client.item_public_token_exchange(request)
        access_token = response.access_token
        item_id = response.item_id
        ACCESS_TOKENS[item_id] = access_token  # Store access token
        return {"access_token": access_token, "item_id": item_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Transactions
@app.post("/plaid/transactions")
def get_transactions(request_data: dict):
    try:
        access_token = request_data["access_token"]
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date="2024-01-01",
            end_date="2024-03-16",
            options=TransactionsGetRequestOptions(count=10, offset=0)
        )
        response = client.transactions_get(request)
        return response.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))