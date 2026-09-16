"""City repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.city import City


class CityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        active_only: bool = True,
        state_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[City]:
        stmt = select(City).order_by(City.city_id)
        if active_only:
            stmt = stmt.where(City.is_active == True)  # noqa: E712
        if state_id is not None:
            stmt = stmt.where(City.state_id == state_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((City.city_name.ilike(term)) | (City.city_code.ilike(term)))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(
        self,
        *,
        active_only: bool = True,
        state_id: int | None = None,
        search: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(City)
        if active_only:
            stmt = stmt.where(City.is_active == True)  # noqa: E712
        if state_id is not None:
            stmt = stmt.where(City.state_id == state_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((City.city_name.ilike(term)) | (City.city_code.ilike(term)))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, city_id: int) -> City | None:
        return self.db.get(City, city_id)

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(City.city_id))) or 0) + 1

    def create(self, **kwargs) -> City:
        row = City(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: City) -> City:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: City) -> City:
        row.is_active = False
        return self.update(row)