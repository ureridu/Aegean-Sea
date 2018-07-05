# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 00:13:16 2018

@author: Ureridu
"""

import pandas as pd
import itertools
import heapq
from collections import defaultdict, namedtuple


def endDist(tile):
    return abs(tile.row - end.row) + abs(tile.col - end.col)


class Tile(namedtuple('Tile', ['row', 'col'])):

    def __add__(self, b):
        row = self.row + b.row
        col = self.col + b.col
        return Tile(row, col)


class mDict(dict):
    def __missing__(self, key):
        self[key] = mDict()
        return self[key]

    def __add__(self, val):
        if isinstance(self, mDict):
            return val
        else:
            return self + val



vect = [-1, 0, 1]
m = namedtuple('Move', ['row', 'col'])

#moves = [m(x, y) for x in vect for y in vect]
#moves.remove((0, 0))
moves = [m(1, 0), m(0, 1), m(0, -1), m(-1, 0)]

'***********************'
start = Tile(16, 0)
end = Tile(18, 1)

vDict = {
        1: 5,
        2: 0,
        3: 0,
        }


mapBase = pd.read_csv('map2.csv')
del mapBase[mapBase.columns[0]]
mapBase.columns = [int(x) for x in mapBase.columns]

rowMin = int(mapBase.index[0])
rowMax = int(mapBase.index[-1])
colMin = int(mapBase.columns[0])
colMax = int(mapBase.columns[-1])


path = mDict()
path[start]['cost'] = 0
path[start]['parent'] = None
q = [(0, start)]
heapq.heapify(q)
curTile = start
beat = 0
while q:
    curCost, curTile = heapq.heappop(q)
    print('current', curTile)

    if curTile == end:
        if not beat:
            beat = curCost
        else:
            if curCost < beat:
                beat = curCost
    elif beat:
        break

    for move in moves:
        nextTile = curTile + move
        print('   next', nextTile)

        if rowMin <= nextTile.row <= rowMax and colMin <= nextTile.col <= colMax:
            velocity = vDict[mapBase.loc[nextTile.row, nextTile.col]]
            print('    ', velocity)
            if velocity:
                nextCost = path[curTile]['cost'] + velocity
                if nextTile not in path or (nextTile in path and nextCost < path[nextTile]['cost']):
                    path[nextTile]['cost'] =  nextCost
                    path[nextTile]['parent'] = curTile
                    cost = endDist(nextTile) + path[nextTile]['cost']
                    heapq.heappush(q, (cost, nextTile))


x = end
print(x)
while x != start:
    print(path[x]['parent'])
    x = path[x]['parent']













#import os
#import html2text
#from multithreading import ThreadPoolExecutor
#
#
#
#files = [file for file in os.listdir('your file path here') if '.html' in file]
#
# do html2text "$file" > "$file.txt"; done:

