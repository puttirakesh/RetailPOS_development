"""Phase 2 verification: load Brand model and print a few rows.

Usage (from backend/):
    uv run python scripts/verify_brand.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select, text

from app.core.database import SessionLocal, check_db_connection, engine
from app.models.brand import Brand


def main() -> None:
    print("1. Checking raw connectivity …")
    if not check_db_connection():
        print("   FAIL: cannot connect to SQL Server")
        sys.exit(1)
    print("   OK")

    print("2. Selecting TOP 5 from RG_Brand via SQLAlchemy …")
    with SessionLocal() as db:
        brands = db.scalars(
            select(Brand).order_by(Brand.brand_id).limit(5)
        ).all()
        if not brands:
            print("   WARNING: table is empty (no rows returned)")
        for b in brands:
            print(
                f"   id={b.brand_id:>4}  code={b.brand_code!r:12}  "
                f"name={b.brand_name!r:30}  margin={b.margin_percentage}  "
                f"active={b.is_active}"
            )

    print("3. Raw count via text() …")
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM dbo.RG_Brand")).scalar()
        print(f"   Total rows in RG_Brand: {count}")

    print("\nPhase 2 model verification PASSED.")


if __name__ == "__main__":
    main()