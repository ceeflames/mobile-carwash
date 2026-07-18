import httpx

from app.core.config import settings


class PaystackService:

    def __init__(self):

        self.base_url = settings.PAYSTACK_BASE_URL

        self.headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30,
        )

    def initialize_transaction(
        self,
        email: str,
        amount: int,
        reference: str,
    ) -> dict:

        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "currency": "NGN",
        }

        response = self.client.post(
            "/transaction/initialize",
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    def verify_transaction(
        self,
        reference: str,
    ) -> dict:

        response = self.client.get(
            f"/transaction/verify/{reference}",
        )

        response.raise_for_status()

        return response.json()