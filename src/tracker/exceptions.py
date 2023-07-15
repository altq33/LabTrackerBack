from fastapi import HTTPException, status

not_enough_permissions_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")