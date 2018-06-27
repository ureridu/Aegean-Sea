# -*- coding: utf-8 -*-
"""
Created on Thu May 17 03:14:05 2018

@author: Ureridu
"""

import pyglet
from pyglet.window import key
import copy

#from pyglet.gl import *
#from pyglet import physicalobject

import os
import pandas as pd
import traceback
import sys

#glClearColor(  0, 100,   0, 255)  # background color
#glEnable(GL_LINE_SMOOTH)
#glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
#glEnable(GL_BLEND)                                  # transparency
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # transparency

mapBase = pd.read_csv('map2.csv')
del mapBase[mapBase.columns[0]]
mapBaseTerrain = pd.read_csv('mapTerrain.csv')

with open('resources/objects.txt', 'r') as infile:
    objects = eval(infile.read())

mediaPath = os.path.join(os.getcwd(), 'resources/test.jpg')

window = pyglet.window.Window(vsync=False)



boatLeft = pyglet.image.load('resources/boat.png')
boatRight = pyglet.image.load('resources/boatRight.png')
boatUp = pyglet.image.load('resources/boatUp.png')
boatDown = pyglet.image.load('resources/boatDown.png')
water = pyglet.image.load('resources/water beta2.png')
test = pyglet.image.load('resources/ground.png')
town1 = pyglet.image.load('resources/town1.png')


mapOffset = 2
xTiles = 20
yTiles = round((window.height / window.width) * xTiles)
baseTiles = (objects['player'][0]  + yTiles, objects['player'][1])

xxx = copy.deepcopy(mapBase)

rAdd = pd.DataFrame([[3] * (len(mapBase.columns))] * ((yTiles // 2) + mapOffset), columns=mapBase.columns)
mapBase = pd.concat([rAdd, mapBase, rAdd], axis=0, ignore_index=False)
mapBase.reset_index(drop=True, inplace=True)

cAdd = pd.DataFrame([[3] * ((xTiles // 2) + mapOffset)] * (len(mapBase.index)))
mapBase = pd.concat([cAdd, mapBase, cAdd], axis=1, ignore_index=True)
mapBase.columns = [x for x in range(len(mapBase.columns))]
mapBase.columns = [str(x) for x in mapBase.columns]

mapBase.reset_index(drop=True, inplace=True)





allSprite = {}
allSpriteList = []
waterSpriteList = []





class SubSprite(pyglet.sprite.Sprite):
    bufferTiles = 3
    xBaseTile = baseTiles[1]
    yBaseTile = baseTiles[0]

    def __init__(self, img, xLoc=0, yLoc=0):
        super().__init__(img)

#        baseX = xLoc - SubSprite.xBaseTile
#        baseY = yLoc - (SubSprite.yBaseTile - yTiles)
        self.xLoc = str(xLoc)
        self.yLoc = yLoc

        self.scale = window.width / (self.width * xTiles)
#        self.x = 0 + (xLoc - SubSprite.xBaseTile) * (self.width)
#        self.y = 0 + (yLoc - (SubSprite.yBaseTile - yTiles)) * (self.height)
        self.updateLoc()

        allSprite[yLoc, xLoc] = self
        allSpriteList.append(self)

    def updateLoc(self):
        self.x = gameMap.xMapRef.at[self.xLoc]
        self.y = gameMap.yMapRef.at[self.yLoc]

        ''' Update me to use base tiles instead of pixels. left corner issue '''
#        if self.x >= window.width + self.width * SubSprite.bufferTiles or self.x <= 0 - self.width * SubSprite.bufferTiles:
#            del self
#
#        if self.y >= window.height + self.height * SubSprite.bufferTiles or self.y <= 0 - self.height * SubSprite.bufferTiles:
#            del self

    def getTile(self):
        for i, col in enumerate(gameMap.xMapRef.index):
            if self.x + self.width / 2 >= gameMap.xMapRef.iloc[i] and self.x + self.width / 2 < gameMap.xMapRef.iloc[i+1]:
                xLoc = int(col)

        for i, row in enumerate(gameMap.yMapRef.index):
#            if self.y - self.height / 2 <= gameMap.yMapRef.iloc[i] and self.y - self.height / 2 > gameMap.yMapRef.iloc[i+1]:
            if self.y - self.height <= gameMap.yMapRef.iloc[i] and self.y - self.height > gameMap.yMapRef.iloc[i+1]:
                yLoc = row

        return yLoc, xLoc


class StaticSprite(SubSprite):
    def __init__(self, img, xLoc=0, yLoc=0):
        super().__init__(img, xLoc, yLoc)


class DynamicSprite(SubSprite):
    xMax = int((1 / xTiles) * window.width) * .3
    yMax = int((1 / yTiles) * window.height) * .3

    yVelocity = .03
    xVelocity = .03


    def __init__(self, img, xLoc=0, yLoc=0):
        super().__init__(img, xLoc, yLoc)
        self.evens = xLoc % 2

#        self.scale = self.scale * 1.2




class WaterSprite(DynamicSprite):
    waterSpriteList = []
    landType = 1 # water

    xOff = 0
    yOff = 0

    xIncr = 0
    yIncr = 0
#    offset = { 0: {'yOff': 0,
#                   'xOff': 0},
#               1: {'yOff': 0,
#                   'xOff': 0}
#               }
#
    def __init__(self, img, xLoc=0, yLoc=0):
        super().__init__(img, xLoc, yLoc)
        WaterSprite.waterSpriteList.append(self)
#
    def waveEmulation(self):
        if self.evens:
            self.y += WaterSprite.yOff
            self.x += WaterSprite.xOff
        else:
            self.y -= WaterSprite.yOff
            self.x -= WaterSprite.xOff
#        yIncr = (self.yVelocity * self.height) * dt
#        self.yOff += yIncr
#        if abs(self.yOff) >= (self.maxMove * self.height):
#            self.yVelocity = -self.yVelocity
#
#        self.y += yIncr
#
#        xIncr = (self.xVelocity * self.width) * dt
#        self.xOff += xIncr
#        if abs(self.xOff) >= (self.maxMove * self.width):
#            self.xVelocity = -self.xVelocity
#
#        self.x += xIncr

#        self.y = self.y +
#        if abs(self.y - self.yTrue)

    @classmethod
    def ClsWave(cls, dt):
        try:
            WaterSprite.yIncr = WaterSprite.yVelocity * WaterSprite.yMax * dt
            WaterSprite.yOff += WaterSprite.yIncr
            if abs(WaterSprite.yOff) >= WaterSprite.yMax:
                WaterSprite.yVelocity = -WaterSprite.yVelocity

            WaterSprite.xIncr = WaterSprite.xVelocity* WaterSprite.xMax  * dt
            WaterSprite.xOff += WaterSprite.xIncr
            if abs(WaterSprite.xOff) >= WaterSprite.xMax:
                WaterSprite.xVelocity = -WaterSprite.xVelocity

#            print(WaterSprite.yOff, WaterSprite.yIncr)
        except Exception as e:
            print(e)


class LandSprite(StaticSprite):
    landType = 2 # land

    def __init__(self, img, xLoc=0, yLoc=0):
        super().__init__(img, xLoc, yLoc)
        self.scale = self.scale * 1.3


class Object():

    def __init__(self):
        self.hitpoints = 10
        self.landSpeed = .5
        self.waterSpeed = .5
        self.impassSpeed = 0

    def makeSpeeds(self):
        self.speeds = {
                1: self.waterSpeed,
                2: self.landSpeed,
                3: self.impassSpeed,
                }


class Town(SubSprite):
    def __init__(self, img, xLoc=xTiles//2, yLoc=yTiles//2):
#        Object.__init__(self)
        super().__init__(img, xLoc, yLoc)

        self.hitpoints = 1000
        self.landSpeed = 0
        self.waterSpeed = 0
        self.impassSpeed = 0

        self.scale = .1


class ship(Object):
    def __init__(self):
        super().__init__()
        self.landSpeed = 0

    def fish(self):
        pass


class singlePersonFishingVessel(ship):
        def __init__(self):
            super().__init__()
            self.waterSpeed = .05
#            self.imgs = [boatRight, boatLeft, boatUp, boatDown]
            self.imgs = imgs


class PlayerSprite(SubSprite, singlePersonFishingVessel):

    def __init__(self, imgs, xLoc=xTiles//2, yLoc=yTiles//2):
        singlePersonFishingVessel.__init__(self)

        super().__init__(self.imgs[0], xLoc, yLoc)

        self.scale = .05

        self.imgLock = 0
        self.imgLockOwner = 'none'
        self.imgAxis = 'yVelocity'

        self.imgAdjust('xVelocity')

#        self.x -= self.width//2
#        self.y -= self.height//2

        self.makeSpeeds()
        self.updateSpeed()

        self.moveTable = {
                        key.RIGHT: ('xVelocity', 1, self.imgs[0]),
                        key.LEFT: ('xVelocity', -1, self.imgs[1]),
                        key.UP: ('yVelocity', 1, self.imgs[2]),
                        key.DOWN: ('yVelocity', -1, self.imgs[3]),
                        'none': (0, 0, 0)
                        }

        self.revMoveTable = {
                            ('xVelocity', 1): (key.RIGHT, self.imgs[0]),
                            ('xVelocity', -1):(key.LEFT, self.imgs[1]),
                            ('yVelocity', 1): (key.UP, self.imgs[2]),
                            ('yVelocity', -1): (key.DOWN, self.imgs[3]),

                            }

        self.dirTable = {
                        'xVelocity': 0,
                        'yVelocity': 0,
                        }

        self.yTile, self.xTile = self.getTile()

    def move(self):
        ''' Deprecated '''
        self.x = self.x + (self.dirTable['xVelocity'] * (window.width / xTiles))
        self.y = self.y + (self.dirTable['yVelocity'] * (window.width / xTiles))

        if self.x > window.width:
            self.x = window.width
        elif self.x < 0:
            self.x = 0

        if self.y > window.height:
            self.y = window.height
        elif self.y < 0:
            self.y = 0

        self.screenShift()


    def updateVelocity(self, symbol, press):
        axis, sign, img = self.moveTable[symbol]
        if self.moveTable[self.imgLockOwner][0] != axis:
            if press:
                self.dirTable[axis] = sign * self.speed
                if not self.imgLock:
                    self.imgLock = 1
                    self.imgLockOwner = symbol
                    self.image = img
                    self.imgAdjust(axis)
            else:
                self.dirTable[axis] = 0

        elif symbol == self.imgLockOwner:
            self.dirTable[axis] = 0
            self.imgLock = 0
            self.imgLockOwner = 'none'

            for k, v in self.dirTable.items():
                if v != 0:
                    if v < 0:
                        vv = -1
                    else:
                        vv = 1
                    self.imgLockOwner, self.image = self.revMoveTable[(k, vv)]
                    self.imgLock = 1
                    self.imgAdjust(k)

        print(mapBase.iloc[player.getTile()], player.getTile())


    def imgAdjust(self, axis):
        if self.imgAxis != axis:
#            if self.imgAxis == 'xVelocity':
#                self.x += self.width/2
#                self.y -= self.height/2
#            else:
#                self.x -= self.width/2
#                self.y += self.height/2
            self.x = round(window.width/2 - self.width/2 + .0001)
            self.y = round(window.height/2 + self.height/2 + .0001)

            print(self.width, self.height)
            print(self.x, self.y)


        self.imgAxis = axis

    def screenShift(self):
        xMove = -(self.dirTable['xVelocity'] * (window.width / xTiles))
        yMove = -(self.dirTable['yVelocity'] * (window.width / xTiles))

        self.xOldTile = self.xTile
        self.yOldTile = self.yTile

        gameMap.xMapRef += xMove
        gameMap.yMapRef += yMove

#        for spr in gameMap.mapSprites.values.flatten():
#            spr.updateLoc()

        self.yTile, self.xTile = self.getTile()

        oldSpeed = self.speed
        self.updateSpeed()

#        if self.dirTable['xVelocity']:
#            self.dirTable['xVelocity'] = abs(1 / self.dirTable['xVelocity']) * self.dirTable['xVelocity'] *self.speed
#
#        if self.dirTable['yVelocity']:
#            self.dirTable['yVelocity'] = abs(1 / self.dirTable['yVelocity']) * self.dirTable['yVelocity'] *self.speed

        if not self.speed:
            gameMap.xMapRef -= (xMove) if xMove else 0
            gameMap.yMapRef -= (yMove) if yMove else 0


        self.yTile, self.xTile = self.getTile()


        xD = self.xTile - self.xOldTile
        yD = self.yTile - self.yOldTile

        if xD > 0:
            gameMap.update(axis=1, ins=-1)
        elif xD < 0:
            gameMap.update(axis=1, ins=0)

        if yD > 0:
            gameMap.update(axis=0, ins=-1)
        elif yD < 0:
            gameMap.update(axis=0, ins=0)


    def updateLoc(self):
        pass

    def updateSpeed(self):
        self.speed = self.speeds[mapBase.iat[self.getTile()]]


class critters(Object)




#winSpritesFlat = [WaterSprite(water, j, i) for j in range(xTiles) for i in range(yTiles)]

class Map():
    w = 1
    l = 2
    n = 3

    ref = {
            w: WaterSprite,
            l: LandSprite,
            n: LandSprite
            }

    imgRef = {
                w: water,
                l: test,
                n: test,
                }

    def __init__(self, mapBase):
            self.mapTypes = mapBase.iloc[baseTiles[0] - yTiles:baseTiles[0] + mapOffset * 2, baseTiles[1]: xTiles + baseTiles[1] + mapOffset * 2]
            self.mapSprites = copy.deepcopy(self.mapTypes)
            self.xMapRef = copy.deepcopy(self.mapTypes.iloc[0, :])
            self.yMapRef = copy.deepcopy(self.mapTypes.iloc[:, 0])

            self.Frames = []

    def mapInit(self):
        xOffset = -mapOffset * int((1 / xTiles) * window.width)
        yOffset = -mapOffset * int((1 / yTiles) * window.height)

        for j, row in enumerate(self.yMapRef):
            rev = len(self.yMapRef) - j
            self.yMapRef.iloc[j] = int(rev * (1 / yTiles) * window.height) + yOffset

        for i, col in enumerate(self.xMapRef):
            self.xMapRef.iloc[i] = int(i * (1 / xTiles) * window.width) + xOffset

        for i, col in enumerate(self.mapTypes):
            for j, row in enumerate(self.mapTypes.loc[:, col].index):
                if mapBase.at[row, col] == Map.w:
                    self.mapSprites.loc[row, col] = WaterSprite(water, int(col), int(row))
                elif mapBase.at[row, col] == Map.l:
                    self.mapSprites.loc[row, col] = LandSprite(test, int(col), int(row))
                elif mapBase.at[row, col] == Map.n:
                    self.mapSprites.loc[row, col] = LandSprite(test, int(col), int(row))

    def update(self, axis, ins):
        if axis == 1:
            dif = self.xMapRef.iat[1] - self.xMapRef.iat[0]

            if ins == 0:
                d = self.xMapRef.iat[0] - dif
                self.mapSprites.drop(labels=self.mapSprites.columns[-1], axis=axis, inplace=True)
#                mapBase.drop(labels=mapBase.columns[-1], axis=axis, inplace=True)
                col = str(int(self.xMapRef.index[ins]) - 1)
                self.xMapRef = pd.concat([pd.Series(d, [col]), self.xMapRef.iloc[:-1]])
#                mapBase[col] = mapBase[col]
                self.mapSprites.insert(ins, col,
                                   [Map.ref[mapBase.at[y, col]](Map.imgRef[mapBase.at[y, col]], int(col), int(y))
                                    for y in self.yMapRef.index])
            else:
                d = self.xMapRef.iat[-1] + dif
                self.mapSprites.drop(labels=self.mapSprites.columns[0], axis=axis, inplace=True)
                col = str(int(self.xMapRef.index[ins]) + 1)
                self.xMapRef = pd.concat([self.xMapRef.iloc[1:], pd.Series(d, [col])])
#                mapBase[col] = mapBase[col]
                self.mapSprites[col] = [Map.ref[mapBase.at[y, col]](Map.imgRef[mapBase.at[y, col]], int(col), int(y))
                                        for y in self.yMapRef.index]


        else:
            dif = self.yMapRef.iat[1] - self.yMapRef.iat[0]

            if ins == 0:
                d = self.yMapRef.iat[0] - dif
                self.mapSprites.drop(labels=self.mapSprites.index[-1], axis=axis, inplace=True)
                row = int(self.yMapRef.index[ins]) - 1
                self.yMapRef = pd.concat([pd.Series(d, [row]), self.yMapRef.iloc[:-1]])
#                mapBase = pd.concat([mapBase.loc[row, :], mapBase])
            else:
                d = self.yMapRef.iat[-1] + dif
                self.mapSprites.drop(labels=self.mapSprites.index[0], axis=axis, inplace=True)
                row = int(self.yMapRef.index[ins]) + 1
                self.yMapRef = pd.concat([self.yMapRef.iloc[1:], pd.Series(d,  [row])])
#                mapBase = pd.concat([mapBase, mapBase.loc[row, :]])

            new = pd.DataFrame([Map.ref[mapBase.at[row, x]](Map.imgRef[mapBase.at[row, x]], int(x), int(row))
                    for x in self.xMapRef.index], columns=[row])
            new = new.T
            new.columns = self.xMapRef.index

            if ins == 0:
                self.mapSprites = pd.concat([new, self.mapSprites])
            else:
                self.mapSprites = pd.concat([self.mapSprites, new])



#mapSpritesFlat = [WaterSprite(water, j, i) if mapBase[j, i][0] == 1 else WaterSprite(test, j, i) for j in mapDisplay.loc[i, :] for i in mapDisplay]
#
gameMap = Map(mapBase)
gameMap.mapInit()
#imgs = [boatRight, boatLeft, boatUp, boatDown]
imgs = [boatRight, boatLeft, boatRight, boatLeft]
player = PlayerSprite(imgs, xLoc=baseTiles[1] + xTiles // 2, yLoc=baseTiles[0] + yTiles // 2)
#homeTown = Town(town1,  xLoc=str(objects['town1'][0] + yTiles), yLoc=objects['town1'][1] + xTiles//2)
homeTown = Town(town1,  yLoc=objects['town1'][0] + yTiles//2 + mapOffset, xLoc=objects['town1'][1] + xTiles//2 + mapOffset)

otherObjs = [homeTown]
#player.scale = .05

#afdgdfg




def update(dt):
    try:
        player.screenShift()
        WaterSprite.ClsWave(1)
        for spr in gameMap.mapSprites.values.flatten():
            spr.updateLoc()
            if spr.landType == 1:
#                print(spr)
                spr.waveEmulation()
#                pass
#                spr.draw()

#        print(allSpriteList[127].y)
#        for spr in allSpriteList:
#            spr.updateLoc(0, 0)

#        for spr in WaterSprite.waterSpriteList:
#            spr.waveEmulation(dt)
    except Exception as e:
        print(e)
        traceback.print_exception(*sys.exc_info())





@window.event
def on_key_press(symbol, modifiers):
    if symbol in player.moveTable:
        player.updateVelocity(symbol, 1)

@window.event
def on_key_release(symbol, modifiers):
    if symbol in player.moveTable:
        player.updateVelocity(symbol, 0)

@window.event
def on_draw():
    try:
#        dt = pyglet.clock.tick()
        window.clear()
        pyglet.gl.glClearColor(204/255, 224/255, 255/255, 1)
    #    update(dt)
#        player.screenShift()

#        WaterSprite.ClsWave(1)
#        gameMap.mapSprites.values.flatten().apply(lambda x: x.waveEmulation() if x.landType == 1)
#        print(allSpriteList[127].y, WaterSprite.yIncr)
#        sprites = gameMap.mapSprites.values.flatten()
        waters = []
        lands = []
        for spr in gameMap.mapSprites.values.flatten():
            if spr.landType == 1:
                waters.append(spr)
            else:
                lands.append(spr)
#                spr.waveEmulation()
#                spr.y = spr.y + WaterSprite.yOff
        for spr in lands:
            spr.draw()
        for spr in waters:
            spr.draw()

#        for spr in gameMap.mapSprites.values.flatten():
#            spr.draw()
#        print(allSpriteList[127].y)
        player.draw()
        for obj in otherObjs:
            if obj.xLoc in gameMap.xMapRef and obj.yLoc in gameMap.yMapRef:
                obj.updateLoc()
                obj.draw()

        fps_display.draw()
    #    image.blit(0, 0)
    except Exception as e:
        print(e)
        traceback.print_exception(*sys.exc_info())

fps_display = pyglet.clock.ClockDisplay()
pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.set_fps_limit(60)
pyglet.app.run()


'''
python -m cProfile -o sample_data.pyprof awesome_game.py
pyprof2calltree -i sample_data.pyprof -k
'''