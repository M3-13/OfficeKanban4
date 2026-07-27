from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.auth import get_current_user

router = APIRouter(prefix="/columns/{column_id}/cards", tags=["cards"])


@router.get("")
def list_cards(column_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.post("")
def create_card(column_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.put("/{card_id}")
def update_card(column_id: int, card_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})


@router.delete("/{card_id}")
def delete_card(column_id: int, card_id: int, _=Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented"})
