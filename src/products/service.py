from decimal import Decimal

from fastapi import Form

from models import Product


async def new_product(
    data: Annotated[NewProdForm, Form()], db):
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
        raise HTTPException()


async def get_product_by_id(p_id: int, db) -> Product:
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


async def get_product_by_category(
    category: str = "General",
    subcategory: str | None = None,
    db,
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


async def search_product(
    search_query: str, db
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


async def get_all(db) -> list[Product]:
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
