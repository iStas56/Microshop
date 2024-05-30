from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import get_product_by_id

router = APIRouter(tags=["Products"])


@router.get("/", response_model=List[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product: Product = Depends(get_product_by_id)):
    return product


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product: Product = Depends(get_product_by_id),
):
    return await crud.update_product(
        session=session,
        product_update=product_update,
        product=product,
    )


@router.patch("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product: Product = Depends(get_product_by_id),
):
    return await crud.update_product(
        session=session,
        product_update=product_update,
        product=product,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )
