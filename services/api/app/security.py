from datetime import datetime, timedelta, timezone

from cryptography.fernet import Fernet, InvalidToken
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


class TokenCipher:
    def __init__(self, key: str) -> None:
        self._fernet = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        try:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        except InvalidToken as exc:
            raise ValueError("invalid encrypted token") from exc


class OAuthState:
    def __init__(self, secret: str, max_age_seconds: int = 600) -> None:
        self._serializer = URLSafeTimedSerializer(secret, salt="google-oauth-state")
        self.max_age_seconds = max_age_seconds

    def issue(self, nonce: str) -> str:
        return self._serializer.dumps({"nonce": nonce})

    def verify(self, state: str) -> str:
        try:
            return self._serializer.loads(state, max_age=self.max_age_seconds)["nonce"]
        except (BadSignature, SignatureExpired, KeyError) as exc:
            raise ValueError("invalid oauth state") from exc


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def session_expiry(days: int = 7) -> datetime:
    return utc_now() + timedelta(days=days)

