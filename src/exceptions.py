from fastapi import HTTPException, status

not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
empty_body_exception = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                     detail="At least one parameter for updating must be passed")
