from typing import Optional


class Button:
    def __init__(self, id: int = 0, label: str = "", redirect_to: Optional[str] = None):
        self.id = id
        self.label = label
        self.redirect_to = redirect_to
