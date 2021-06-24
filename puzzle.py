import numpy as np
import pandas as pd


def back_ground(mon, day):
    mon -= 1
    day -= 1
    back_ground = np.zeros([7, 7], dtype='i1')
    back_ground[mon // 6][mon % 6] = 9
    back_ground[day // 7 + 2][day % 7] = 9
    back_ground[0][-1] = 9
    back_ground[1][-1] = 9
    back_ground[-1][3:] = 9
    return pd.DataFrame(back_ground)


def find_coord(df, bg=0):
    coord = False
    for i in df.index:
        if not coord:
            for j in df.columns:
                if not bg:
                    if df[i][j] == 0:
                        coord = (i, j)
                        break
                elif bg:
                    if df[i][j] != 0:
                        coord = (i, j)
                        break
                else:
                    pass
    return coord


class puzzle:
    def __init__(self, mon, day):
        self.bg = back_ground(mon, day)
        self.shape = self.bg.shape

    def check(self, cube):
        shape = cube.shape
        bg_start = find_coord(self.bg)
        cube_start = find_coord(cube, bg=1)
        off_set = bg_start[1] - cube_start[1]
        if bg_start[1] < cube_start[1]:
            return False
        elif off_set + shape[1] > self.shape[1]:
            return False
        elif bg_start[0] + shape[0] > self.shape[0]:
            return False
        else:
            insert = True
            for row in cube.index:
                if insert:
                    for col in cube.columns:
                        if self.bg[bg_start[0] + row][off_set + col] != 0 and cube[row][col] != 0:
                            insert = False
                            break
            return insert

    def insert(self, cube):
        shape = cube.shape
        bg_start = find_coord(self.bg)
        cube_start = find_coord(cube, bg=1)
        off_set = bg_start[1] - cube_start[1]
        for row in cube.index:
            for col in cube.columns:
                self.bg[off_set + col][bg_start[0] + row] += cube[col][row]


if __name__ == "__main__":
    a = puzzle(1, 8)
    cube = pd.DataFrame([[0,1],[1,1],[1,0]])
    # cube = pd.DataFrame([[0, 1, 1], [1, 1, 1]])
    print(a.bg)
    print(cube)
    print(a.check(cube))
    if a.check(cube):
        a.insert(cube)
    print(a.bg)
