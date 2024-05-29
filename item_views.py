from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
def read_items():
    return [
        'item1',
        'item2',
        'item3',
    ]


@router.get("/{item_id}")
def read_item(item_id: Annotated[int, Path(ge=1, lt=100)], q: str = 'check'):
    return {"item_id": item_id, "q": q}
