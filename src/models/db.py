from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class db_minesweeper(Model):
    """The Database model for a minesweeper game.

    Attributes / fields:
     - id [UUIDField] : Is the primary key for identifying a game.
     - code [IntField] : The Code players need to enter to join a game.
     - n_cols [SmallIntField]: The number of columns
     - n_rows [SmallIntField]: The number of rows
     - solvable [BooleanField]: True if the board is solvable only with logic
     - start_col [SmallIntField]: The players start column.
     - start_row [SmallIntField]: The players start row.
     - n_mines [SmallIntField]: The total number of mines in the game.
    """
    id = fields.UUIDField(pk=True)
    code = fields.SmallIntField(unique=True)  # the code to enter the same game
    n_cols = fields.SmallIntField()
    n_rows = fields.SmallIntField()
    solvable = fields.BooleanField()
    n_mines = fields.SmallIntField()


class db_spot(Model):
    """The database model for a single spot of a minesweeper board. Each Spot is tied to a single board with the foreignKey field of db_minesweeper.

    Attributes/Fields:
     - id [UUIDField]: The primary key for each spot.
     - code [SmallIntField]: The Code of the minesweeper board a spot belongs to.
     - col [SmallIntField]: Holds the column of the spot in its minesweeper board 16bit signed integer.
     - row [SmallIntField]: Holds the row of the spot in its minesweeper board. 16bit signed integer.
     - opened [BooleanField]: True if the players already opened the spot or not, default:False
     - mine [BooleanField]: True if the spot contains a mine false if it does not.
     - n_mines [SmallIntField]: Contains the number of neighboring mines. 16bit signed integer.
     - flagged [BooleanField]: Whether or not the field is flagged, default: False
    """
    id = fields.UUIDField(pk=True)
    code = fields.SmallIntField()
    col = fields.SmallIntField()
    row = fields.SmallIntField()
    opened = fields.BooleanField(default=False)
    mine = fields.BooleanField()
    n_mines = fields.SmallIntField()
    flagged = fields.BooleanField(default=False)


minesweeper_pydantic = pydantic_model_creator(
    db_minesweeper, name="minesweeper_pydantic")
minesweeperIn_pydantic = pydantic_model_creator(
    db_minesweeper, name="minesweeperIn_pydantic", exclude_readonly=True, exclude=("id"))
msInWs_pydantic = pydantic_model_creator(
    db_minesweeper, name="msInWs_pydantic", exclude=("id", "code"))
spot_pydantic = pydantic_model_creator(
    db_spot, exclude_readonly=True, name="spot_pydantic")
