from decimal import Decimal
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


class Item(BaseModel):
    name: str = ""
    price: Decimal = Field(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        json_schema_extra={"examples": [19.99]},
    )
    cover: str = ""
    available: bool = True


async def select_item(search_query: str) -> list[Item]:
    results = []
    for item in mock_db:
        if search_query in item["name"]:
            results.append(
                Item(name=item["name"], price=item["price"], cover=item["cover"])
            )

    # if len(results) > 0:
    # return results

    #    return [Item(available=False)]
    return results


async def get_all_items() -> list[Item]:
    results = []
    for item in mock_db:
        if item["amount"] > 0:
            results.append(
                Item(name=item["name"], price=item["price"], cover=item["cover"])
            )

    return results
