"""Customer repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        active_only: bool = True,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Customer]:
        stmt = select(Customer).order_by(Customer.customer_id)
        if active_only:
            stmt = stmt.where(Customer.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Customer.customer_name.ilike(term))
                | (Customer.customer_code.ilike(term))
                | (Customer.mobile_no.ilike(term))
            )
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Customer)
        if active_only:
            stmt = stmt.where(Customer.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Customer.customer_name.ilike(term))
                | (Customer.customer_code.ilike(term))
                | (Customer.mobile_no.ilike(term))
            )
        return self.db.scalar(stmt) or 0

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_mobile(self, mobile: str, *, exclude_id: int | None = None) -> Customer | None:
        if not mobile:
            return None
        stmt = select(Customer).where(Customer.mobile_no == mobile)
        if exclude_id is not None:
            stmt = stmt.where(Customer.customer_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Customer.customer_id))) or 0) + 1

    def create(self, **kwargs) -> Customer:
        row = Customer(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Customer) -> Customer:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Customer) -> Customer:
        row.is_active = False
        return self.update(row)