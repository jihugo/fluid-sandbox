"""Fluid Physics Module"""

from typing import Optional, Iterable
import numpy as np

OOSR3 = 1 / (3**0.5)
OOSR2 = 1 / (2**0.5)
UJ_DIRS = {
    4: (
        np.array(
            [
                [1, 0, -OOSR2],
                [-1, 0, -OOSR2],
                [0, 1, OOSR2],
                [0, -1, OOSR2],
            ]
        ),
        0,
    ),
    6: (
        np.array(
            [
                [1, 0, 0],
                [-1, 0, 0],
                [0, 1, 0],
                [0, -1, 0],
                [0, 0, 1],
                [0, 0, -1],
            ]
        ),
        np.pi / 2,
    ),
    8: (
        np.array(
            [
                [OOSR3, OOSR3, OOSR3],
                [OOSR3, OOSR3, -OOSR3],
                [OOSR3, -OOSR3, OOSR3],
                [OOSR3, -OOSR3, -OOSR3],
                [-OOSR3, OOSR3, OOSR3],
                [-OOSR3, OOSR3, -OOSR3],
                [-OOSR3, -OOSR3, OOSR3],
                [-OOSR3, -OOSR3, -OOSR3],
            ]
        ),
        np.arccos(-1 / 3),
    ),
}


def normalize(vector: np.ndarray) -> np.ndarray:
    """Normalize array"""
    return np.array(vector) / np.linalg.norm(np.array(vector))


def angle(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """Find the angle between 2 3D vectors"""
    dot = np.dot(normalize(vector_1), normalize(vector_2))
    if abs(dot - 1) < 1e-8:
        return 0
    if abs(dot + 1) < 1e-8:
        return np.pi
    return np.arccos(dot)


class Point:
    """Point in space"""

    __slots__ = ["position", "pressure", "neighbors", "wall"]

    def __init__(
        self, x: float, y: float, z: float, wall: bool, pressure: float = 0
    ) -> None:
        self.position = np.array([x, y, z])
        self.pressure = pressure
        self.neighbors = {}  # Cell : (to-direction, distance)
        self.wall = wall


class Cell(Point):
    """Cell"""

    __slots__ = ["velocity", "acceleration", "uj_dirs", "uj_tol", "contained"]

    def __init__(
        self, x: float, y: float, z: float, uj_factor: int, pressure: float = 0
    ) -> None:
        super().__init__(x, y, z, wall=False, pressure=pressure)
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])
        if uj_factor not in UJ_DIRS:
            raise UserWarning(f"U-joint Factor of {uj_factor} is not supported")
        self.uj_dirs: np.ndarray = UJ_DIRS[uj_factor][0]
        self.uj_tol: float = UJ_DIRS[uj_factor][1]
        self.contained = False

    def check_containment(self) -> None:
        """Check if cell is contained in each of the u-joint directions"""
        for direction in self.uj_dirs:
            for neighbor_dir, _ in self.neighbors.values():
                if angle(direction, neighbor_dir) < self.uj_tol:
                    break
            else:
                return
        self.contained = True

    def run(self) -> None:
        """One step of the simulation"""


class CV:
    """Control Volume"""

    __slots__ = ["grid", "CV_factor"]


