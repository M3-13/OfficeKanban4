from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.auth import get_current_user

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("")
def list_boards(_=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.post("")
def create_board(_=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.get("/{board_id}")
def get_board(board_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.put("/{board_id}")
def update_board(board_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.delete("/{board_id}")
def delete_board(board_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})
