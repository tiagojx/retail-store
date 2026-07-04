from decimal import Decimal
from typing import Annotated, Optional
from fastapi import Form
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
    id: int
    name: str = ""
    price: Decimal = Field(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        json_schema_extra={"examples": [19.99]},
    )
    cover: str = ""
    available: bool = True
    amount: int = 1


class NewProdForm(BaseModel):
    name: str
    price: str
    cover: str
    amount: str


class StatusHandler(BaseModel):
    message: str
    status_code: int


async def new_product(
    data: Annotated[NewProdForm, Form()], db: Optional[psycopg.Connection] = None
) -> StatusHandler:
    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    try:
        with db.cursor() as cur:
            insert_stmt = "INSERT INTO products (name, price, cover, amount) VALUES (%s, %s, %s, %s);"
            cur.execute(insert_stmt, (data.name, data.price, data.cover, data.amount))
            db.commit()
        cur.close()
    except Exception:
        return StatusHandler(message="Internal server error", status_code=500)

    return StatusHandler(message="New product added into database", status_code=201)


async def get_item_by_id(p_id: int, db: Optional[psycopg.Connection] = None) -> Product:
    results = []

    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT name, price, cover, available, amount FROM products WHERE id = %s;",
                (p_id,),
            )
            rows = cur.fetchall()

            for row in rows:
                price_fix = Decimal(str(row[1])) / Decimal("100")
                results.append(
                    Product(
                        id=p_id,
                        name=row[0],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[2],
                        available=row[3],
                        amount=row[4],
                    )
                )
        cur.close()
    except Exception as e:
        print(e)

    return results[0]


async def select_item(
    search_query: str, db: Optional[psycopg.Connection] = None
) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    with db.cursor() as cur:
        cur.execute("SELECT id, name, price, cover, available FROM products;")
        rows = cur.fetchall()

        for row in rows:
            if search_query in row[1]:
                price_fix = Decimal(str(row[2])) / Decimal("100")
                results.append(
                    Product(
                        id=row[0],
                        name=row[1],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[3],
                        available=row[4],
                    )
                )
    cur.close()

    return results


async def select_item_mock(search_query: str) -> list[Product]:
    results = []
    for item in mock_db:
        if search_query in item["name"]:
            results.append(
                Product(
                    id=item["id"],
                    name=item["name"],
                    price=item["price"],
                    cover=item["cover"],
                )
            )

    return results


async def get_all_items(db: Optional[psycopg.Connection] = None) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connect is not open. Shall stabilish a connection first."
        )
    with db.cursor() as cur:
        cur.execute("SELECT id, name, price, cover, amount, available FROM products;")
        rows = cur.fetchall()

        for row in rows:
            if row[4] > 0:
                price_fix = Decimal(str(row[2])) / Decimal("100")
                results.append(
                    Product(
                        id=row[0],
                        name=row[1],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[3],
                        available=row[5],
                    )
                )
    cur.close()

    return results


async def get_all_items_mock() -> list[Product]:
    results = []
    for item in mock_db:
        if item["amount"] > 0:
            results.append(
                Product(
                    id=item["id"],
                    name=item["name"],
                    price=item["price"],
                    cover=item["cover"],
                )
            )

    return results
