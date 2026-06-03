from decimal import Decimal
from typing import Optional
import psycopg
from pydantic import BaseModel, Field


mock_db = [
    {
        "name": "hat",
        "price": Decimal("20"),
        "cover": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpZqAc-BZPyvRq28q5E3pshM5LP6L3vPr7VA&s",
        "amount": 375,
    },
    {
        "name": "pencil",
        "price": Decimal("2.89"),
        "cover": "https://musgravepencil.com/cdn/shop/products/320_Harvest_2048px.jpg?v=1569116504",
        "amount": 1023,
    },
    {
        "name": "rock in cd",
        "price": Decimal("899.90"),
        "cover": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpbNMvJgbyrnZyg2P1pGB10kdnqDVVTBJULw&s",
        "amount": 2,
    },
]


class Product(BaseModel):
    name: str = ""
    price: Decimal = Field(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        json_schema_extra={"examples": [19.99]},
    )
    cover: str = ""
    available: bool = True


async def select_item(
    search_query: str, db: Optional[psycopg.Connection] = None
) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    with db.cursor() as cur:
        cur.execute("SELECT name, price, cover, available FROM products;")
        rows = cur.fetchall()

        for row in rows:
            if search_query in row[0]:
                price_fix = Decimal(str(row[1])) / Decimal("100")
                results.append(
                    Product(
                        name=row[0],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[2],
                        available=row[3],
                    )
                )
    cur.close()

    return results


async def select_item_mock(search_query: str) -> list[Product]:
    results = []
    for item in mock_db:
        if search_query in item["name"]:
            results.append(
                Product(name=item["name"], price=item["price"], cover=item["cover"])
            )

    return results


async def get_all_items(db: Optional[psycopg.Connection] = None) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connect is not open. Shall stabilish a connection first."
        )
    with db.cursor() as cur:
        cur.execute("SELECT name, price, cover, amount, available FROM products;")
        rows = cur.fetchall()

        for row in rows:
            if row[3] > 0:
                price_fix = Decimal(str(row[1])) / Decimal("100")
                results.append(
                    Product(
                        name=row[0],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[2],
                        available=row[4],
                    )
                )
    cur.close()

    return results


async def get_all_items_mock() -> list[Product]:
    results = []
    for item in mock_db:
        if item["amount"] > 0:
            results.append(
                Product(name=item["name"], price=item["price"], cover=item["cover"])
            )

    return results
