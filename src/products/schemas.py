from pydantic import BaseModel


class NewProdForm(BaseModel):
    name: str
    price: str
    cover: str
    amount: str
    category: str
    subcategory: str
