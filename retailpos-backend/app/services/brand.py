"""Brand business logic."""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.brand import BrandRepository
from app.schemas.brand import BrandCreate, BrandListResponse, BrandRead, BrandUpdate


class BrandService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = BrandRepository(db)

    def list_brands(
        self,
        *,
        active_only: bool = True,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> BrandListResponse:
        if limit < 1 or limit > 200:
            raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
        if skip < 0:
            raise HTTPException(status_code=422, detail="skip must be >= 0")
        items = self.repo.get_all(
            active_only=active_only, search=search, skip=skip, limit=limit
        )
        total = self.repo.count(active_only=active_only, search=search)
        return BrandListResponse(
            total=total,
            items=[BrandRead.model_validate(b) for b in items],
        )

    def get_brand(self, brand_id: int) -> BrandRead:
        brand = self.repo.get_by_id(brand_id)
        if brand is None:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")
        return BrandRead.model_validate(brand)

    def create_brand(self, payload: BrandCreate) -> BrandRead:
        existing = self.repo.get_by_name(payload.brand_name)
        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail=f"Brand name '{payload.brand_name}' already exists",
            )
        brand_id = self.repo.next_id()
        brand = self.repo.create(
            brand_id=brand_id,
            brand_code=str(brand_id),
            brand_name=payload.brand_name,
            margin_percentage=payload.margin_percentage,
            is_active=payload.is_active,
        )
        return BrandRead.model_validate(brand)

    def update_brand(self, brand_id: int, payload: BrandUpdate) -> BrandRead:
        brand = self.repo.get_by_id(brand_id)
        if brand is None:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")

        if "brand_name" in data:
            conflict = self.repo.get_by_name(data["brand_name"], exclude_id=brand_id)
            if conflict is not None:
                raise HTTPException(
                    status_code=409,
                    detail=f"Brand name '{data['brand_name']}' already exists",
                )
            brand.brand_name = data["brand_name"]

        if "margin_percentage" in data:
            brand.margin_percentage = data["margin_percentage"]

        if "is_active" in data:
            brand.is_active = data["is_active"]

        brand = self.repo.update(brand)
        return BrandRead.model_validate(brand)

    def delete_brand(self, brand_id: int) -> BrandRead:
        if brand_id == 1:
            raise HTTPException(
                status_code=403,
                detail="Default Brand (BrandId=1) cannot be deleted",
            )
        brand = self.repo.get_by_id(brand_id)
        if brand is None:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")
        if not brand.is_active:
            raise HTTPException(
                status_code=409,
                detail=f"Brand {brand_id} is already inactive",
            )
        brand = self.repo.soft_delete(brand)
        return BrandRead.model_validate(brand)