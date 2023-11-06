import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


CLIENT_ID="122ef8b501854f81"
CLIENT_SECRET="8909165fb44aa8f05fed8620336533073949ba75"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")