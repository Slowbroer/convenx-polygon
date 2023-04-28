class Point:
    """
    A point class
    """
    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    def __getitem__(self, index):
        return (self.x, self.y)[index]