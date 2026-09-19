"""Product repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        active_only: bool = True,
        category_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Product]:
        stmt = select(Product).order_by(Product.product_id)
        if active_only:
            stmt = stmt.where(Product.is_active == True)  # noqa: E712
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Product.product_name.ilike(term)) | (Product.product_code.ilike(term))
            )
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(
        self,
        *,
        active_only: bool = True,
        category_id: int | None = None,
        search: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Product)
        if active_only:
            stmt = stmt.where(Product.is_active == True)  # noqa: E712
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Product.product_name.ilike(term)) | (Product.product_code.ilike(term))
            )
        return self.db.scalar(stmt) or 0

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_code(self, code: str, *, exclude_id: int | None = None) -> Product | None:
        stmt = select(Product).where(Product.product_code == code)
        if exclude_id is not None:
            stmt = stmt.where(Product.product_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Product.product_id))) or 0) + 1

    def create(self, **kwargs) -> Product:
        row = Product(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Product) -> Product:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Product) -> Product:
        row.is_active = False
        return self.update(row)