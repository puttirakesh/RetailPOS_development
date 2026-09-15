"""Brand repository – pure data-access layer."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.brand import Brand


class BrandRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        active_only: bool = True,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Brand]:
        stmt = select(Brand).order_by(Brand.brand_id)
        if active_only:
            stmt = stmt.where(Brand.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Brand.brand_name.ilike(term)) | (Brand.brand_code.ilike(term))
            )
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Brand)
        if active_only:
            stmt = stmt.where(Brand.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Brand.brand_name.ilike(term)) | (Brand.brand_code.ilike(term))
            )
        return self.db.scalar(stmt) or 0

    def get_by_id(self, brand_id: int) -> Brand | None:
        return self.db.get(Brand, brand_id)

    def get_by_name(self, brand_name: str, *, exclude_id: int | None = None) -> Brand | None:
        stmt = select(Brand).where(Brand.brand_name == brand_name)
        if exclude_id is not None:
            stmt = stmt.where(Brand.brand_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        current = self.db.scalar(select(func.max(Brand.brand_id))) or 0
        return int(current) + 1

    def create(
        self,
        *,
        brand_id: int,
        brand_code: str,
        brand_name: str,
        margin_percentage: Decimal,
        is_active: bool,
    ) -> Brand:
        brand = Brand(
            brand_id=brand_id,
            brand_code=brand_code,
            brand_name=brand_name,
            margin_percentage=margin_percentage,
            is_active=is_active,
        )
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def update(self, brand: Brand) -> Brand:
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def soft_delete(self, brand: Brand) -> Brand:
        brand.is_active = False
        return self.update(brand)