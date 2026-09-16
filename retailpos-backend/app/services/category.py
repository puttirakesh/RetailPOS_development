"""Category business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.group import GroupRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryRead,
    CategoryUpdate,
)


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.repo = CategoryRepository(db)
        self.groups = GroupRepository(db)

    def list_items(
        self,
        *,
        active_only: bool = True,
        group_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> CategoryListResponse:
        items = self.repo.get_all(
            active_only=active_only, group_id=group_id, search=search, skip=skip, limit=limit
        )
        total = self.repo.count(active_only=active_only, group_id=group_id, search=search)
        return CategoryListResponse(
            total=total, items=[CategoryRead.model_validate(i) for i in items]
        )

    def get(self, category_id: int) -> CategoryRead:
        row = self.repo.get_by_id(category_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
        return CategoryRead.model_validate(row)

    def create(self, payload: CategoryCreate) -> CategoryRead:
        if self.groups.get_by_id(payload.group_id) is None:
            raise HTTPException(status_code=400, detail=f"Group {payload.group_id} does not exist")
        category_id = self.repo.next_id()
        row = self.repo.create(
            category_id=category_id,
            category_code=payload.category_code,
            category_name=payload.category_name,
            group_id=payload.group_id,
            is_active=payload.is_active,
        )
        return CategoryRead.model_validate(row)

    def update(self, category_id: int, payload: CategoryUpdate) -> CategoryRead:
        row = self.repo.get_by_id(category_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "group_id" in data and self.groups.get_by_id(data["group_id"]) is None:
            raise HTTPException(status_code=400, detail=f"Group {data['group_id']} does not exist")
        for k, v in data.items():
            setattr(row, k, v)
        return CategoryRead.model_validate(self.repo.update(row))

    def delete(self, category_id: int) -> CategoryRead:
        row = self.repo.get_by_id(category_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"Category {category_id} already inactive")
        return CategoryRead.model_validate(self.repo.soft_delete(row))