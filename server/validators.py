from fastapi import HTTPException


def validate_input_string(input_string: str):
    """Validate to make sure request isn't BS.

    Args:
        input_string (str): Query string.

    Raises:
        HTTPException: If there's just one letter like wat do u want.
    """
    letters = [char for char in input_string if char.isalpha()]
    if len(letters) <= 1:
        raise HTTPException(status_code=400, detail="tf are u tryna predict??")
