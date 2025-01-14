from fastapi import APIRouter, Path
from typing import Annotated


router = APIRouter(prefix="/core")


@router.put("/{item}")
def get_item(item):
    ...
    return {}


@router.get("/item/{item_id}")
def get_item_by_id(item_id: Annotated[int, Path(ge=0, lt=100_000)]):
    return {"item": {
        "id": item_id
    }}


@router.post("/update_item")
def update_item(item):
    ...
    return {}


@router.delete("/{item}")
def get_item(item):
    ...
    return {}
