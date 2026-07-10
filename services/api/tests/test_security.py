from cryptography.fernet import Fernet
import pytest

from app.security import OAuthState, TokenCipher, session_expiry, utc_now


def test_token_cipher_round_trip_and_rejects_tampering() -> None:
    cipher = TokenCipher(Fernet.generate_key().decode())
    encrypted = cipher.encrypt("refresh-token")
    assert encrypted != "refresh-token"
    assert cipher.decrypt(encrypted) == "refresh-token"
    with pytest.raises(ValueError):
        cipher.decrypt(encrypted[:-2] + "xx")


def test_oauth_state_expires_and_round_trips() -> None:
    state = OAuthState("test-secret")
    value = state.issue("nonce")
    assert state.verify(value) == "nonce"


def test_session_expiry_is_in_the_future() -> None:
    assert session_expiry() > utc_now()
