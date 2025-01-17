"""Fluid Physics Module"""

from typing import Optional, Iterable


class Cell:
    """Cell in space"""

    __slots__ = ["exists", "weight"]

    def __init__(self, exists: bool, weight: float = 0) -> None:
        self.exists = exists
        self.weight = weight

    def __repr__(self) -> str:
        return (
            " "
            if not self.exists
            else (
                "■"
                if self.weight > 0.8
                else "▤" if self.weight > 0.5 else "▪" if self.weight > 0.2 else "▫"
            )
        )


class CV:
    """Control Volume"""

    __slots__ = ["grid"]

    def __init__(self, grid = None):
        self.grid: Optional[Iterable] = grid

    def __repr__(self) -> str:
        if self.grid is None:
            return "Unitiated Control Volume"

        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.grid])


class CVRectangle(CV):
    """Rectangular Control Volume"""

    def __init__(self, width: float, height: float, resolution: float):
        grid_width = int((width + 0.5 * resolution) / resolution)
        grid_height = int((height + 0.5 * resolution) / resolution)
        grid = [
            [Cell(True) for _ in range(grid_width)] for _ in range(grid_height)
        ]
        super().__init__(grid)
