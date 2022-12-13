from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from numpy import ravel
from typing import Dict

from ..models.db import db_minesweeper, minesweeper_pydantic, db_spot, spot_pydantic, msInWs_pydantic
from ..models.socketManager import WebsocketManager
from .field import open, set_Flag
from ..minesweeper import Minesweeper

router = APIRouter(prefix="/ws", tags=["Websocket"])

managers: Dict[str, WebsocketManager] = {}


@router.websocket("/game/{code}")
async def ws_open(websocket: WebSocket, code: int):
    """The Websocket that is used for the entire game, to allow broadcasting one players actions to the other participants.

    Args:
        websocket (WebSocket): The Websocket used for the connection
        code (int): The Code that uniquely identifies a single game
    """
    NAME: str = ""

    if str(code) not in managers.keys():
        managers.update({str(code): WebsocketManager()})
    await managers[str(code)].connect(websocket)

    manager: WebsocketManager = managers[str(code)]

    field_exists = await db_minesweeper.exists(code=code)
    spot_exists = await db_spot.exists(code=code, col=0, row=0)

    if spot_exists == True:
        ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
        ms = ms.dict()
        field = await spot_pydantic.from_queryset(db_spot.filter(code=code))

        field = [spot.dict() for spot in field]
        await websocket.send_json({"field": field, "n_cols": ms["n_cols"], "n_rows": ms["n_rows"], "n_mines": ms["n_mines"]})

    elif field_exists == True:
        ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
        ms = ms.dict()
        await websocket.send_json({"n_cols": ms["n_cols"], "n_rows": ms["n_rows"], "n_mines": ms["n_mines"]})
    else:
        await websocket.send_json({"error": "The Game you requested does not exist"})
        return None

    try:
        while True:
            data = await websocket.receive_json()

            if data["intent"] == "open":
                data["col"] = int(data["col"])
                data["row"] = int(data["row"])

                exists = await db_spot.exists(code=code, col=data["col"], row=data["row"])
                if exists != True:
                    ms_dict = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
                    ms_dict = ms_dict.dict()
                    ms = Minesweeper(
                        ms_dict["n_cols"],
                        ms_dict["n_rows"],
                        data["col"],
                        data["row"]
                    )
                    ms.place_mines(ms_dict["n_mines"])
                    default_values = {"opened": False,
                                      "code": ms_dict["code"], "flagged": False}
                    for spot in ravel(ms.field):
                        db_sp_obj = await db_spot.create(**{**spot.get_db_attribs(), **default_values})

                    field = await spot_pydantic.from_queryset(db_spot.filter(code=code))
                    field = [spot.dict() for spot in field]
                    await manager.broadcast({"field": field})

                opened = await open(code, int(data["col"]), int(data["row"]))
                if type(opened) == list:
                    await manager.broadcast({"opened": opened})
                else:
                    if "game_status" in opened.keys():
                        await manager.broadcast({"opened": opened, "message": f"{NAME} threw the game"})
                    else:
                        await manager.broadcast({"opened": opened})
                    await db_spot.filter(code=code).delete()
                    await db_minesweeper.filter(code=code).delete()

            elif data["intent"] == "flag":
                exists = await db_spot.exists(code=code, col=int(data["col"]), row=int(data["row"]))

                if exists != True:
                    await websocket.send_json({"error": "Can't set a flag on the first Move"})
                    continue

                status = await set_Flag(code, int(data["col"]), int(data["row"]))

                await manager.broadcast({"flagged": status})
            elif data["intent"] == "restart":
                await db_minesweeper.create(code=code,
                                            n_cols=data["n_cols"],
                                            n_rows=data["n_rows"],
                                            solvable=False,
                                            n_mines=data["n_mines"]
                                            )
            elif data["intent"] == "name":
                NAME = data["name"]
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # TODO send message to other clients that sb disconnected
