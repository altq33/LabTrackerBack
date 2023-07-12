from src.auth.schemas import UserInDB


def check_items_access_permissions(current_user: UserInDB, target) -> bool:
    if current_user.id == target.user_id:
        return True
    return False
