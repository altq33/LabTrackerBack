from fastapi import HTTPException, status

already_busy_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already busy")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
incorrect_auth_data_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )