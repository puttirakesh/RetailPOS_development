"""Customer business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.repositories.state import StateRepository
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerRead,
    CustomerUpdate,
)


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.repo = CustomerRepository(db)
        self.states = StateRepository(db)

    def list_items(
        self,
        *,
        active_only: bool = True,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> CustomerListResponse:
        items = self.repo.get_all(
            active_only=active_only, search=search, skip=skip, limit=limit
        )
        total = self.repo.count(active_only=active_only, search=search)
        return CustomerListResponse(
            total=total, items=[CustomerRead.model_validate(i) for i in items]
        )

    def get(self, customer_id: int) -> CustomerRead:
        row = self.repo.get_by_id(customer_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return CustomerRead.model_validate(row)

    def create(self, payload: CustomerCreate) -> CustomerRead:
        if self.states.get_by_id(payload.state_id) is None:
            raise HTTPException(status_code=400, detail=f"State {payload.state_id} does not exist")
        if payload.mobile_no and self.repo.get_by_mobile(payload.mobile_no):
            raise HTTPException(
                status_code=409, detail=f"Mobile '{payload.mobile_no}' already exists"
            )
        customer_id = self.repo.next_id()
        code = payload.customer_code or str(customer_id)
        row = self.repo.create(
            customer_id=customer_id,
            customer_code=code,
            customer_name=payload.customer_name,
            mobile_no=payload.mobile_no,
            address=payload.address,
            city_id=payload.city_id,
            state_id=payload.state_id,
            gst_no=payload.gst_no,
            credit_days=payload.credit_days,
            credit_limit=payload.credit_limit,
            opening_balance=payload.opening_balance,
            ledger_required=payload.ledger_required,
            email_id=payload.email_id,
            is_active=payload.is_active,
            discount_percentage=payload.discount_percentage,
            discount_amount=payload.discount_amount,
        )
        return CustomerRead.model_validate(row)

    def update(self, customer_id: int, payload: CustomerUpdate) -> CustomerRead:
        row = self.repo.get_by_id(customer_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "state_id" in data and self.states.get_by_id(data["state_id"]) is None:
            raise HTTPException(status_code=400, detail=f"State {data['state_id']} does not exist")
        if "mobile_no" in data and data["mobile_no"]:
            conflict = self.repo.get_by_mobile(data["mobile_no"], exclude_id=customer_id)
            if conflict:
                raise HTTPException(
                    status_code=409, detail=f"Mobile '{data['mobile_no']}' already exists"
                )
        for k, v in data.items():
            setattr(row, k, v)
        return CustomerRead.model_validate(self.repo.update(row))

    def delete(self, customer_id: int) -> CustomerRead:
        row = self.repo.get_by_id(customer_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"Customer {customer_id} already inactive")
        return CustomerRead.model_validate(self.repo.soft_delete(row))