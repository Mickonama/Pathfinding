class Cell(object):
    def __init__(self, this=None, parent=None, level=0) -> None:
        super().__init__()
        self.pos = this
        self.parent = parent
        self.level = level

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cell):
            return self.pos == o.pos

    def __hash__(self):
        return hash(self.pos)

    def __str__(self):
        return str(self.pos)