"""Fluid Physics Module"""

from typing import Optional, Iterable

import numpy as np


class Cell:
    """Cell in space"""

    __slots__ = [
        "exists",
        "weight",
        "velocity",
        "acceleration",
        "pressure",
        "num_neighbors",
    ]

    def __init__(self, exists: bool, weight: float = 0) -> None:
        self.exists = exists
        self.weight = weight
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])
        self.pressure = 0
        self.num_neighbors = 0

    def __repr__(self) -> str:
        return (
            "◦"
            if not self.exists
            else (
                "■"
                if self.weight > 0.8
                else "▤" if self.weight > 0.5 else "▪" if self.weight > 0.2 else "▫"
            )
        )
    
    def 

    def run() -> None:
        """One step of the simulation"""


class CV:
    """Control Volume"""

    __slots__ = ["grid"]

    def __init__(self, grid=None):
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
        grid = np.concat(
            [
                [[Cell(False) for _ in range(grid_width + 2)]],
                [
                    np.concat(
                        [
                            [Cell(False)],
                            [Cell(True) for _ in range(grid_width)],
                            [Cell(False)],
                        ]
                    )
                    for _ in range(grid_height)
                ],
                [[Cell(False) for _ in range(grid_width + 2)]],
            ]
        )
        super().__init__(grid)
