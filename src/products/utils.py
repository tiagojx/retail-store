from src.products.models import Product


async def alphabetical_sorting(product_list: list[Product]) -> list[Product]:
    products_sorted = []

    names = []
    for product in product_list:
        names.append(product.name)

    names_sorted = sorted(names, key=str.lower)

    for name in names_sorted:
        for product in product_list:
            if name == product.name:
                products_sorted.append(product)

    return products_sorted
