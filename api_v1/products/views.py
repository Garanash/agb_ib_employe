from fastapi import APIRouter, status, Depends, Request, Form
from src.core.models.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=['Products'])


@router.get('/', response_model=list[Product])
async def get_products(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    products = await crud.get_products(session=session)
    return templates.TemplateResponse('index.html', {"request": request, "products": products})


@router.post('/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(

        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}", response_model=Product)
async def get_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return product


@router.put("/{product_id}")
async def update_product(
        product_update: ProductUpdate,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update
    )


@router.patch("/{product_id}")
async def update_product_partial(
        product_update: ProductUpdatePartial,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
