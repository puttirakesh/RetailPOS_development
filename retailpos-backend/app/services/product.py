"""Product business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductRead,
    ProductUpdate,
)


class ProductService:
    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)
        self.categories = CategoryRepository(db)

    def list_items(
        self,
        *,
        active_only: bool = True,
        category_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> ProductListResponse:
        items = self.repo.get_all(
            active_only=active_only,
            category_id=category_id,
            search=search,
            skip=skip,
            limit=limit,
        )
        total = self.repo.count(
            active_only=active_only, category_id=category_id, search=search
        )
        return ProductListResponse(
            total=total, items=[ProductRead.model_validate(i) for i in items]
        )

    def get(self, product_id: int) -> ProductRead:
        row = self.repo.get_by_id(product_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        return ProductRead.model_validate(row)

    def create(self, payload: ProductCreate) -> ProductRead:
        if self.categories.get_by_id(payload.category_id) is None:
            raise HTTPException(
                status_code=400, detail=f"Category {payload.category_id} does not exist"
            )
        product_id = self.repo.next_id()
        code = payload.product_code or str(product_id)
        if self.repo.get_by_code(code):
            raise HTTPException(status_code=409, detail=f"Product code '{code}' already exists")
        row = self.repo.create(
            product_id=product_id,
            product_code=code,
            product_name=payload.product_name,
            category_id=payload.category_id,
            hsn_code=payload.hsn_code,
            remarks=payload.remarks,
            is_unique=payload.is_unique,
            is_bulk=payload.is_bulk,
            auto_ean_required=payload.auto_ean_required,
            entry_wise_ean_required=payload.entry_wise_ean_required,
            discount_not_applicable=payload.discount_not_applicable,
            manual_barcode_restriction=payload.manual_barcode_restriction,
            non_inventory=payload.non_inventory,
            uom_id=payload.uom_id,
            is_active=payload.is_active,
        )
        
        return ProductRead.model_validate(row)

    def update(self, product_id: int, payload: ProductUpdate) -> ProductRead:
        row = self.repo.get_by_id(product_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "category_id" in data and self.categories.get_by_id(data["category_id"]) is None:
            raise HTTPException(
                status_code=400, detail=f"Category {data['category_id']} does not exist"
            )
        if "product_code" in data and data["product_code"]:
            conflict = self.repo.get_by_code(data["product_code"], exclude_id=product_id)
            if conflict:
                raise HTTPException(
                    status_code=409,
                    detail=f"Product code '{data['product_code']}' already exists",
                )
        for k, v in data.items():
            setattr(row, k, v)
        return ProductRead.model_validate(self.repo.update(row))

    def delete(self, product_id: int) -> ProductRead:
        row = self.repo.get_by_id(product_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"Product {product_id} already inactive")
        return ProductRead.model_validate(self.repo.soft_delete(row))