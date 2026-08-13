from decimal import Decimal
from typing import Annotated, Optional
from fastapi import Form
import psycopg
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: Optional[int] = None
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
    category: str = "General"
    subcategory: Optional[str] = None


class NewProdForm(BaseModel):
    name: str
    price: str
    cover: str
    amount: str
    category: str
    subcategory: str


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
            insert_stmt = "INSERT INTO products (name, price, cover, amount, category, subcategory) VALUES (%s, %s, %s, %s, %s, %s);"
            cur.execute(
                insert_stmt,
                (
                    data.name,
                    data.price,
                    data.cover,
                    data.amount,
                    data.category,
                    data.subcategory,
                ),
            )
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
                "SELECT name, price, cover, available, amount, category, subcategory FROM products WHERE id = %s;",
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
                        category=row[5],
                        subcategory=row[6],
                    )
                )
        cur.close()
    except Exception as e:
        print(e)

    return results[0]


async def get_item_by_category(
    category: str = "General",
    subcategory: Optional[str] = None,
    db: Optional[psycopg.Connection] = None,
) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    try:
        with db.cursor() as cur:
            if subcategory is not None:
                cur.execute(
                    "SELECT id, name, price, cover, available, amount, category, subcategory FROM products WHERE subcategory = %s;",
                    (subcategory,),
                )
            else:
                cur.execute(
                    "SELECT id, name, price, cover, available, amount, category, subcategory FROM products WHERE category = %s;",
                    (category,),
                )

            rows = cur.fetchall()

            for row in rows:
                price_fix = Decimal(str(row[2])) / Decimal("100")
                results.append(
                    Product(
                        id=row[0],
                        name=row[1],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[3],
                        available=row[4],
                        amount=row[5],
                        category=row[6],
                        subcategory=row[7],
                    )
                )
        cur.close()
    except Exception as e:
        print(e)

    return results


async def select_item(
    search_query: str, db: Optional[psycopg.Connection] = None
) -> list[Product]:
    results = []

    if not db:
        raise RuntimeError(
            "Database connection is not open. Shall stabilish a connection first."
        )

    with db.cursor() as cur:
        cur.execute("SELECT id, name, price, cover, amount, available FROM products;")
        rows = cur.fetchall()

        for row in rows:
            if search_query.lower() in row[1].lower():
                price_fix = Decimal(str(row[2])) / Decimal("100")
                results.append(
                    Product(
                        id=row[0],
                        name=row[1],
                        price=price_fix.quantize(Decimal("0.00")),
                        cover=row[3],
                        amount=row[4],
                        available=row[5],
                    )
                )
    cur.close()

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
                        amount=row[4],
                        available=row[5],
                    )
                )
    cur.close()

    return results

                )
            )

    return results
