from decimal import Decimal
from typing import Optional

from . import db


class SQL(db.DB):
    def __init__(self):
        super().__init__()

    def add_product(
        self,
        name: str,
        price: Decimal,
        amount: int,
        available: bool = True,
        cover: Optional[str] = None,
    ) -> None:
        if not self.conn:
            raise RuntimeError(
                "Database connection is not open. Shall stabilish a connection first."
            )

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, price, cover, amount, available) VALUES (%s, %s, %s, %s, %s);",
                (name, price, cover, amount, available),
            )

            self.conn.commit()
            print("New product added successfully.")
