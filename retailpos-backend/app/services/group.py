"""Group business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.group import GroupRepository
from app.schemas.group import GroupCreate, GroupListResponse, GroupRead, GroupUpdate


class GroupService:
    def __init__(self, db: Session) -> None:
        self.repo = GroupRepository(db)

    def list_items(
        self, *, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> GroupListResponse:
        items = self.repo.get_all(search=search, skip=skip, limit=limit)
        total = self.repo.count(search=search)
        return GroupListResponse(total=total, items=[GroupRead.model_validate(i) for i in items])

    def get(self, group_id: int) -> GroupRead:
        row = self.repo.get_by_id(group_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Group {group_id} not found")
        return GroupRead.model_validate(row)

    def create(self, payload: GroupCreate) -> GroupRead:
        if self.repo.get_by_code(payload.group_code):
            raise HTTPException(status_code=409, detail=f"Group code '{payload.group_code}' exists")
        group_id = self.repo.next_id()
        row = self.repo.create(
            group_id=group_id,
            group_code=payload.group_code,
            group_name=payload.group_name,
            slab_req=payload.slab_req,
            tax_id=payload.tax_id,
            b_value=payload.b_value,
            b_tax_id=payload.b_tax_id,
            a_value=payload.a_value,
        )
        return GroupRead.model_validate(row)

    def update(self, group_id: int, payload: GroupUpdate) -> GroupRead:
        row = self.repo.get_by_id(group_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Group {group_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "group_code" in data and self.repo.get_by_code(data["group_code"], exclude_id=group_id):
            raise HTTPException(status_code=409, detail=f"Group code '{data['group_code']}' exists")
        for k, v in data.items():
            setattr(row, k, v)
        return GroupRead.model_validate(self.repo.update(row))

    def delete(self, group_id: int) -> dict[str, str]:
        row = self.repo.get_by_id(group_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Group {group_id} not found")
        self.repo.delete(row)
        return {"detail": f"Group {group_id} deleted"}