import pytest
from app.auth import utils
from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def test_hash_and_verify_password():
    password = "supersecret"
    hashed = utils.hash_password(password)
    assert hashed != password
    assert utils.verify_password(password, hashed) is True
    assert utils.verify_password("wrongpassword", hashed) is False

def test_create_access_token_contains_expected_data():
    data = {"sub": "123"}
    token = utils.create_access_token(data)
    assert isinstance(token, str)
    
    # Decode the token to check payload
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "123"
    assert "exp" in payload
    
    # Check expiration is roughly now + ACCESS_TOKEN_EXPIRE_MINUTES
    expire_timestamp = payload["exp"]
    now = datetime.utcnow()
    expire_dt = datetime.utcfromtimestamp(expire_timestamp)
    diff = expire_dt - now
    # On tolère un délai de 1 minute d'écart
    assert 0 <= diff.total_seconds() <= (ACCESS_TOKEN_EXPIRE_MINUTES + 1) * 60

def test_create_access_token_expired_token():
    # Création d'un token expiré manuellement pour test d'erreur
    data = {"sub": "123", "exp": datetime.utcnow() - timedelta(minutes=1)}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    # Le token est expiré, la décodage doit lever une erreur
    with pytest.raises(ExpiredSignatureError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
