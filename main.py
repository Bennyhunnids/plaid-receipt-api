import os
from fastapi import FastAPI
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
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