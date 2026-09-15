"""List active users for Postman login testing.

Usage:
    uv run python scripts/list_users.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select, text

from app.core.database import SessionLocal, check_db_connection, engine
from app.models.user import User


def main() -> None:
    if not check_db_connection():
        print("FAIL: cannot connect to SQL Server")
        sys.exit(1)

    print("Password column width:")
    with engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'dbo'
                  AND TABLE_NAME = 'RG_User'
                  AND COLUMN_NAME = 'Password'
                """
            )
        ).fetchone()
        width = row[0] if row else None
        print(f"  VARCHAR({width})")
        if width is not None and width < 100:
            print(
                "  WARNING: run in SSMS:\n"
                "  ALTER TABLE dbo.RG_User ALTER COLUMN [Password] VARCHAR(100) NOT NULL;"
            )

    print("\nActive users:")
    with SessionLocal() as db:
        users = db.scalars(select(User).order_by(User.user_id)).all()
        if not users:
            print("  (none found)")
        for u in users:
            kind = (
                "bcrypt"
                if (u.password or "").startswith(("$2a$", "$2b$", "$2y$"))
                else "plain/legacy"
            )
            print(
                f"  id={u.user_id:>3}  username={u.username!r:20}  "
                f"admin={bool(u.is_admin)}  role={u.role:8}  password={kind}"
            )

    print("\nUse one username + its desktop-app password in Postman login.")


if __name__ == "__main__":
    main()