class Button:
    def __init__(self, id: int = 0, label: str = "", redirect_to: str | None = None):
        self.id = id
        self.label = label
        self.redirect_to = redirect_to
