import os
from square.client import Client

def get_square_client():
    # Initialize the Square API client
    client = Client(
        access_token=os.getenv("EAAAl3sHoJqaNzO0MZ7MtLGPdPHuGiEXqc2DRhiJrLKvWVgEdOmL3Sj5c91BPszi"),
        environment="sandbox"  # Change to "production" for live transactions
    )
    return client
