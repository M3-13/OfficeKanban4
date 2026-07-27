from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.auth import get_current_user

router = APIRouter(prefix="/boards/{board_id}/columns", tags=["columns"])


@router.get("")
def list_columns(board_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.post("")
def create_column(board_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.put("/{column_id}")
def update_column(board_id: int, column_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.delete("/{column_id}")
def delete_column(board_id: int, column_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})
