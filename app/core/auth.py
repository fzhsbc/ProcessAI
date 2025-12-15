from fastapi import Header, HTTPException, status
import os

def api_token_auth(x_api_token: str = Header(..., alias="X-API-TOKEN")):
    expected = os.getenv("AUTH_TOKEN")
    #print("打印预期的Tokening")
    #print(expected)
    if expected is None or x_api_token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)