from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: str
    cover: str
    amount: str
    category: str
    subcategory: str
