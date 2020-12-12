"""

--- Day 11: Seating System ---
Your plane lands with plenty of time to spare.
The final leg of your journey is a ferry that goes directly to the tropical island where you
can finally start your vacation.
As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're
pretty sure you can predict the best place to sit.
You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either
    floor (.),
    an empty seat (L),
    or an occupied seat (#).

For example, the initial seat layout might look like this:

```
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```

Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set of rules.
All decisions are based on the number of occupied seats adjacent to a given seat
(one of the eight positions immediately up, down, left, right, or diagonal from the seat).
The following rules are applied to every seat simultaneously:

```
If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.
```

After one round of these rules, every seat in the example layout becomes occupied:

```
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
```

After a second round, the seats with four or more occupied adjacent seats become empty again:

```
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
```

This process continues for three more rounds:

```
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
```
```
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
```
```
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
```
At this point, something interesting happens: the chaos stabilizes and further applications
of these rules cause no seats to change state!
Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?

--- Part Two ---
As soon as people start to arrive, you realize your mistake.
People don't just care about adjacent seats - they care about the first seat they can see in
each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat
in each of those eight directions.
For example, the empty seat below would see eight occupied seats:

```
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
```
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

```
.............
.L.L.#.#.#.#.
.............
```
The empty seat below would see no occupied seats:

```
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
```
Also, people seem to be more tolerant than you expected: it now takes five or more visible
occupied seats for an occupied seat to become empty (rather than four or more from the previous rules).
The other rules still apply: empty seats that see no occupied seats become occupied, seats matching
no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

```
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```
```
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
```
```
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
```
```
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
```
```
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
```
```
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
```
```
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
```

Again, at this point, people stop shifting around and the seating area reaches equilibrium.
Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is
reached, how many seats end up occupied?

"""
import timeit
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

from utils import timeit


directions = (
    (-1, -1,),
    (-1, 0,),
    (-1, 1,),
    (0, -1,),
    (0, 1,),
    (1, -1,),
    (1, 0,),
    (1, 1,),
)


@dataclass
class SeatStatus:
    seats_changed: int
    seat_counter: Counter


def get_surrounding_areas(coord, layout, shape):
    for d in directions:
        x, y = coord

        while True:
            x_, y_ = x+d[0], y+d[1]
            if 0 <= x_ < shape[0] and 0 <= y_ < shape[1]:
                value = layout[x_][y_]
                if value in ("#", "L"):
                    yield value
                    break
                x, y = x_, y_

            else:
                break


def update_layout(
        layout: List[str],
        shape: Tuple[int, int]
) -> Tuple[List[str], SeatStatus]:
    new_layout = []
    seat_counter = Counter()
    seats_changed = 0

    for i, row in enumerate(layout):
        new_row = ""
        for j, char in enumerate(row):
            surrounding_area_occupied = False
            surrounding_area_occupied_count = 0

            for area in get_surrounding_areas((i, j), layout, shape=shape):
                if area == "#":
                    surrounding_area_occupied = True
                    surrounding_area_occupied_count += 1

            current_area = layout[i][j]
            if current_area == "L" and not surrounding_area_occupied:
                new_row += "#"
                seats_changed += 1
            elif current_area == "#" and surrounding_area_occupied_count >= 5:
                new_row += "L"
                seats_changed += 1
            else:
                new_row += current_area

            seat_counter[current_area] += 1
        new_layout.append(new_row)

    return new_layout, SeatStatus(seats_changed=seats_changed, seat_counter=seat_counter)


@timeit(iterations=10)
def main():
    layout = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()

    shape = len(layout), len(layout[0])
    while True:
        layout, seat_status = update_layout(layout, shape=shape)
        if not seat_status.seats_changed:
            return seat_status.seat_counter["#"]


if __name__ == '__main__':
    # print(timeit.timeit("main()", setup="from __main__ import main", number=10)/10)
    main()
