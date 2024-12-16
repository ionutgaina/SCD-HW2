from bson import ObjectId


def is_valid_objectid(id: str) -> bool:
    """Helper function to check if the ID is a valid ObjectId"""
    try:
        ObjectId(id)
        return True
    except Exception:
        return False
