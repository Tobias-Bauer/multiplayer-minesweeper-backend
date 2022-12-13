from fastapi import APIRouter

from ..models.db import minesweeperIn_pydantic, db_minesweeper
from ..models.pydantic_models import join_pyd

router = APIRouter(prefix="", tags=["General Options"])


@router.post("/join")
async def join_page(data: join_pyd):
    """The join backend route to check whether or not the game identified by the code the user enters exists

    Args:
        code (join_pyd): The code as Pydantic Model for type validation

    Returns:
        dict[str, bool]: "exists": bool whether or not the game exists
    """
    data = data.dict()
    field_exists = await db_minesweeper.exists(code=data["code"])
    return {"exists": field_exists}


@router.post("/create")
async def create_new_game(msIn: minesweeperIn_pydantic):
    """The create backend route to make a new game

    Args:
        msIn (minesweeperIn_pydantic): Pydantic model for the required data to create a new game.

    Returns:
        dict[str, str]: either error with specific information or succes with "Game successfully created"
    """
    msIn = msIn.dict()

    if msIn["n_cols"] <= 5:
        return {"error": "Number of colums is too small"}
    elif msIn["n_cols"] > 60:
        return {"error": "Number of columns must be at or below 60"}
    elif msIn["n_rows"] <= 5:
        return {"error": "Number of rows is too small"}
    elif msIn["n_rows"] > 60:
        return {"error": "Number of rows must be at or below 60"}
    elif msIn["n_mines"] < 1:
        return {"error": "Number of mines too small"}
    elif msIn["n_mines"] >= msIn["n_rows"]*msIn["n_cols"] - 9:
        return {"error": "Number of mines too big"}
    else:
        await db_minesweeper.create(**msIn)
        return {"success": "Game successfully created"}
