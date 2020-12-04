"""
--- Day 3: Toboggan Trajectory ---
With the toboggan login problems resolved, you set off toward the airport.
While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the
area is covered in trees.
You'll need to see which angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer coordinates in a grid.
You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#

These aren't the only trees, though; due to something you read about once involving
arboreal genetics and biome stability, the same pattern repeats to the right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

You start on the open square (.) in the top-left corner and need to reach the bottom (below the
bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers);
start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1.
Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where there was an open square and X
where there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

In this example, traversing the map using this slope would cause you to encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you
encounter?

"""
from collections import Counter, deque
from dataclasses import dataclass
from enum import Enum

import numpy as np

from utils import timeit


class Terrain(str, Enum):
    tile = "."
    tree = "#"


@dataclass
class Slope:
    x_change: int
    y_change: int


@dataclass
class Coordinate:
    x: int
    y: int

    def navigate(self, slope: Slope):
        return Coordinate(
            x=self.x+slope.x_change,
            y=self.y+slope.y_change
        )


def navigate(map_: np.array, slope: Slope):
    row_len, col_len = map_.shape
    row_pointer = deque([_ for _ in range(row_len)])
    col_pointer = deque([_ for _ in range(col_len)])

    try:
        while True:
            for _ in range(slope.y_change):
                _ = row_pointer.popleft()

            col_pointer.rotate(-slope.x_change)
            current_coordinate = Coordinate(x=col_pointer[0], y=row_pointer[0])

            element = map_[current_coordinate.y, current_coordinate.x]
            yield element

    except IndexError:
        pass


def create_map(input_: str):
    return np.array([[c for c in line] for line in input_.split("\n")])


def expand_map(map_: np.array, slope: Slope):
    """Based on the slope, we can determine how far 'left' we need to go"""
    col_len, row_len = map_.shape
    desired_col_size = col_len*slope.x_change

    for _ in range(desired_col_size // row_len):
        map_ = np.append(
            map_,
            np.copy(map_),
            axis=1
        )

    return map_


@timeit()
def main(input_: str, slope: Slope):
    map_ = create_map(input_)
    navigator = navigate(map_, slope)

    counts = Counter()

    for element in navigator:
        counts[element] += 1

    return counts


if __name__ == '__main__':
    print(main(input_=""".#..........#......#..#.....#..
....#.............#.#....#..#..
.....##...###....#..#.......#..
.#....#..#......#........#.....
.#.........###.#..........##...
...............##........#.....
#..#..........#..##..#....#.#..
....#.##....#..#...#.#....#....
...###...#............#.#......
#.........#..#...............#.
#.#...........#...............#
..#.#......#..###.#...#..##....
.....#..#..#..#............#...
......#.......#.....#....##....
#......#...#.......#.#.#.......
...........##.#.............#..
.#.........#..#.####...........
..#...........#....##..........
#...........#.......#..#.#.....
.....##...#.....#..##..#..#....
#.#..........................#.
##.....#..........#.......##..#
....#..#............#.#.#......
.......#.......#..#............
...#.#..........#..#.....#.....
.....#...##..##.....##........#
.#.....#........##............#
..#....#.#...#.....#.##........
........##.....#......##...##..
......#..................#.....
..##......##.....##...##.......
......#..#...##......##........
.#..#..#.#.....................
.#....#.#...#....#.......##...#
.####.#..##...#.#.#....#...#...
.#....#.....#...#..#.........##
...........#.#####.#.#..##..#..
.#......##...#..###.#.#....#...
...#.....#........#..###...#...
.......#................##.#...
.##...#.#..................#...
..#........#....#..........#..#
..#.........#..................
...#.#..........#.#..##........
...#.##..........##...........#
...........#..#........#.......
.#....#.#...........#....#.##..
.#...#..#............#....#.#..
...#..#...#.........####.#.#...
..#...#...........###..#...##.#
......##...#.#.#....##....#....
#..#.#.....##....#.......#...#.
.#.....#.....#..#..##..........
................#.#.#...##.....
.#.....#............#......#...
...#...#..#.#....######.....#..
..#..........##......##.....#..
......#..#.##...#.#............
....#.......#..#...#..#.#......
#......##.#..#........#.....#..
..#.........#..#.........#.....
..#.........##.......#.#.#..##.
...#....##.................#.#.
...#........##.#.......#.##..##
....#.#...#...#....#...........
.........#....##........#......
...#........#..#.......#...#...
#.......#....#...#...........#.
.......#......#...##...........
.#.#......##.#.......#..#...#..
.#.....##.#...#......#..#......
........#.............#.#..#..#
#...........#....#.....#.##.#.#
................#...#........##
#..#.##..#.....#...##.#........
#.....#.#..##......#.#..#..###.
....#...#.....#................
......#...#..##...........#....
......#.........##.#...#......#
#...#.#.....#..#.#..#..#......#
...#.#..#..#.#........###.#....
..#...#.......#.#.......#......
...#....#.....#.......#......#.
#...........#....#..#..#.......
..........##......##.........##
##............#..#.#...#..#.#..
..#.##....##...##..#...#.......
............##.##..###..#..#...
......#....##...##.........#...
......#..#.#......####..#......
..............#....#..#..##....
...#.#..#...##.#.......#.#.....
...#.#....#.......#..#..#..##..
..........#.........#..........
...#.....#............#.....##.
....#.#......................#.
.........#...#.#...#...........
...#........#..##.....#...#.#..
......##.....#.#..#...###.#...#
#....#..#.#.....#...#..........
.#.##.###.........#..##.#....#.
#.........#....#........#...#..
...........#...............#..#
###....................#....#..
.................#....#.....#..
..........#.........#.......#..
........#..#....#.....##.......
#...##.#...#.#.#............#..
....#.........##.#.#..#...###..
.##..............#...#.....##.#
###...#..................#...#.
.....#..#...#..#...#...........
.#.................#...#..#..#.
.#.........###...#.##......###.
.####............#......#..#...
....#........#..#.#....#..##..#
..#....#.#...#.#.....##....#...
..###..#..#....##....#..#..#...
...#.#.....#.#....#.....#......
.....#..........#.#............
.......#...........#.#..#..#...
......##........#.....#.......#
..#.#.....##............#..##..
....#.#........#...........##..
#......#..##........#.....#....
#...#...###..............##....
#..#........#........#.....##.#
......##.####........#..#....#.
...##..#.##.....#...#...#..#...
#..............###.##..##......
......................#.....#..
.........#.#.......#...##.#....
....#......#..........###..#...
#...####.#.................#..#
##.#....#....#.....##..#....#.#
..#.....#..##.........#.#..#.#.
.....#.....#...................
#....##.#.........###....#.....
#........#.#.......#.#.........
.##.#...#.....#...#.......##.##
#..#.............#.............
..........#.........####.......
..##..............#..#.#.......
..#.#.....#........#......##...
#.#.......#.#................#.
.#...#........#....##....#.##..
.#..#...#...#......#.#.........
......##............#.........#
.#....#.#.#.........#..#..##...
#....#......#.......###........
.......#........##..#...#..###.
#.##..........#..###..#..#.#...
.#..#....#..........#.#.##.....
#..#...#.#...#..#..#.#...#.....
.........#...#.#............#..
#..#.............#......##.##..
...##.......#..................
....#......#...#.....#......#..
.....##..#......#....#....#....
....#...#...#...#.....#........
.#....#........##....#..#.#...#
#.......#..#......#......#...#.
..............#......#......#..
#......#..##...#........#....#.
#..#..#..#.....#..#........#...
#...#.....#...#..........#...##
........#.......#...#.....#.#..
...................##.......#..
.#......#........#.##..#....#..
.....#.....#...#..#..#......#..
........##.#..##.........#....#
.........#.......#.............
............#.###.###..#.#.....
.............#....#...........#
..#.....#.#..##.##........#....
...#....#....#.........#.....#.
.#............#......#.........
..#.#..........##.##......#.#..
....#.........................#
..........##...................
#.......#.#..............#...#.
...##..#..##...##.#..#.#.#.....
...########.#..##....#.........
##.#........##.....#........#..
#.#.....#........#..#....#...#.
..#............#.......###.##.#
#.#............................
...#.#.#....#..........#..#....
..###.#.....#.#..#.............
#........#..........#.#..#.....
...........#..#....#.........#.
..#............#.....#.#.......
#.#............#..#.....#.#.#..
...#...#.......................
.#.#.#...##.............#..#..#
..#.........#..#.....##....##..
.#...#............#.......#..##
....#..#.#.#...####............
#.......#....#..##....##....#..
.....##.#....#.#..#.......#....
...........#.......#....##.#.##
..........#...#....##...#.#....
..#.............#.............#
....#..#.....#....#.#..###.#...
.......#.##.#......#...##...#.#
.#..#.#..#.#.......#....###.#..
#..........##...##.........##..
##..#......##.#.####.#.....#...
....#.#...#........#..##..#.#..
.#.............................
.##..#.#...##.....#....#.....#.
..##.........#......#.........#
.#.#........#...#.#.#....##....
.#.................##.........#
...#...............#....#......
..#...#..#..........###..#...##
..........#..#..........##..#..
...#.............#.##.#...#....
...#...........#...............
......#.........##.#...#...#...
...#.#........#..#.....#..#...#
#.#...#....##...#.....#....#...
#.#.#..#.....#.........#.......
##...........#..####...........
#..........#........###...#..#.
#..#.......#....#......###.....
..#.....#......#.###......##...
...#.##..#............#...#....
.##........#.....#.............
#....#.##..#...........##.#.#..
..#.....#.#....#.......#......#
#..#.......#............#......
#.......##....#...#..#.........
.................#..##.........
..............#..#..#.##.......
#.#.......................#..#.
..#..##...........#....#..#..#.
...#....#.......#.......#....#.
.....#.#..#.#.....#.........#.#
..#.#.........#.....#..........
...#.#.#.......#.#.......#.#..#
...##...#.#.#.....#.....##....#
##.......#.#.#.#.......#...##..
....#.#...........#......#.....
.#.....#........####...........
#......#........#.....#..#..#..
..#..#......#...##.......#....#
#........#..........#.....#.#..
.#...........#.....#.....#.....
..........#..#...#....#....##..
.....#.#..........#.....##..#..
......#.........##.............
..#..#.....##......##........#.
.#.#.#.#..#.#..#.......#.......
#.#...####.#.#....#.#........#.
....#...#.....#......#..##.....
##.........#.........#..#.#..#.
..#.#........#.#........#.##...
#....#......#...#....#.........
.##.............###....###.#...
..##.#.......#...#..#......#...
.....#.##..................#...
.....#.#...#..#................
........#..#..#...........#.#.#
....#.###.....#..#.#.....##..##
....##.#.........#..##.........
.##........#......#..###..#.##.
.........##...............#.##.
..#...............#.#...#..#.#.
....#....##.....#...#..#.....#.
#...#.....................#....
.....#.#............#...##.#.#.
...#......#.......#........##.#
.#.#..#.#....#.##.......##....#
.........#...#..##.........#...
.#...#..#....................#.
.......#...#........#.#..#.#.##
.#.............#......#..#.#...
............##.........#....#.#
#.........##..##...............
.#.#....#.#..#..........##.....
..###...#..#.#.......#..#...##.
.....#....#.#............##.#..
##.....#.#..#..#...............
...##...#......#....#..#..#....
.............#....#..#..##...##
#.......#............#....##..#
..#.##.....#.......#....#....#.
..........#...#.............###
..#....#.#..................#..
#.#...#..#...........#.........
....##..#..##..#..........#....
#...#...#.#....#.##...#.......#
#......##.#...##..#.....#......
....#.......#.#............#...
#....#...........###...........
#..#...#...#......#.#..#.......
...............................
#........##.............#.#....
.............#........#....#.##
........##.####.....##..#......
#.#.#.#.......##....##.....#...
.......#..##..#...#............
..........#...#....#..#.#.#.##.
...#........##....#...#........
#..#.##....#....#........#.....
.##...#.....##...#.............
.#...#..#.#.....#.##.....#.....
...........#.............#...#.
.#..#................#...#..#..
#..........#......##..##....#..
####..#...........#.#....#.....
..#.#.##..#...##........#....##
.#.......##........#.....#.....
............#................#.
.#...#...#.....#.#....#.##..#..
..#.............#.#....#.#.....
..............#...........#....
..............#........#....#..
..........##........#..#...#...
...#.#....#.#....#..#.....#...#
..#......#...........#..#..#.#.
.....##.....#.####....#........""",
         slope=Slope(3, 1)))