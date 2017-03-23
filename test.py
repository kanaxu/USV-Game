#coding:utf-8

from Game import BasicGame
from Map import BasicMap
from USV import OneStepUSV


class MyUSV(OneStepUSV):
  '''一个策略简单的USV,派生自OneStepUSV'''
  def __init__(self, uid, x, y, env):
    super(MyUSV, self).__init__(uid, x, y, env)

  def decisionAlgrithm(self):
    if(self.isEnemy):
      return self.attackDecisionAlgrithm()
    else:
      return self.protectionDecisionAlgrithm()

  def attackDecisionAlgrithm(self):
    '''进攻方策略:在上下左右四个格子中,选择离目标最近的那个格子,如果出现相等就随机选一个;
    如果发现目标格子被其它舰艇占用,选择次近的格子;如果全部被占用,保持不动
    (这不见得是什么高明的策略,即是是防守方保持静止,也很有可能使进攻方进入死循环)'''
    targetX, targetY = self.env.targetCoordinate()
    distanceUp = ((targetX - self.x) ** 2 + (targetY - (self.y - 1)) ** 2) ** 0.5
    distanceDown = ((targetX - self.x) ** 2 + (targetY - (self.y + 1)) ** 2) ** 0.5
    distanceLeft = ((targetX - (self.x - 1)) ** 2 + (targetY - self.y) ** 2) ** 0.5
    distanceRight = ((targetX - (self.x + 1)) ** 2 + (targetY - self.y) ** 2) ** 0.5
    decisions = [distanceUp, distanceDown, distanceLeft, distanceRight]
    decisions.sort()

    finalDecision = {"stay":True}

    for decision in decisions:
      if decision==distanceUp:
        decisionX, decisionY = self.x, self.y - 1
        angularToBe = 90.0
      elif decision==distanceDown:
        decisionX, decisionY = self.x, self.y + 1
        angularToBe = 270.0
      elif decision==distanceLeft:
        decisionX, decisionY = self.x - 1, self.y
        angularToBe = 0.0
      elif decision==distanceRight:
        decisionX, decisionY = self.x + 1, self.y
        angularToBe = 180.0

      if(self.isDecisionLegal(decisionX, decisionY)):
          finalDecision["stay"] = False
          finalDecision["clockwise"] = angularToBe - self.direction > 0
          finalDecision["angularSpeed"] = abs(angularToBe - self.direction)
          break

    return finalDecision

  def protectionDecisionAlgrithm(self):
    '''试图出现在进攻方想要出现的那一个格子上,更具体的说,以进攻方的目标格子为"目标",实行进攻方的策略.
    这个测试游戏里面敌舰只有一艘,所以敌人想要去的位置是确定的,如果敌人选择不动,以敌人的位置为目标位置'''

    '''得到敌人的目标位置'''
    enemy = self.env.enemyShips[0]
    enemyAction = enemy.attackDecisionAlgrithm()
    if(enemyAction["stay"]):
      targetX, targetY = enemy.coordinate()
    else:
      if(enemyAction["clockwise"]):
        enemyDirection = enemy.direction + enemyAction["angularSpeed"]
        if(enemyDirection >= 360):
          enemyDirection -= 360
      else:
        enemyDirection = enemy.direction - enemyAction["angularSpeed"]
        if(enemyDirection < 0):
          enemyDirection += 360

      enemyX, enemyY = enemy.coordinate()
      if(enemyDirection==0.0):
        targetX, targetY = enemyX - 1, enemyY
      if(enemyDirection==90.0):
        targetX, targetY = enemyX, enemyY - 1
      if(enemyDirection==180.0):
        targetX, targetY = enemyX + 1, enemyY
      if(enemyDirection==270):
        targetX, targetY = enemyX, enemyY + 1

    '''下面套用attackDecisionAlgrithm'''
    distanceUp = ((targetX - self.x) ** 2 + (targetY - (self.y - 1)) ** 2) ** 0.5
    distanceDown = ((targetX - self.x) ** 2 + (targetY - (self.y + 1)) ** 2) ** 0.5
    distanceLeft = ((targetX - (self.x - 1)) ** 2 + (targetY - self.y) ** 2) ** 0.5
    distanceRight = ((targetX - (self.x + 1)) ** 2 + (targetY - self.y) ** 2) ** 0.5
    decisions = [distanceUp, distanceDown, distanceLeft, distanceRight]
    decisions.sort()

    finalDecision = {"stay":True}

    for decision in decisions:
      if decision==distanceUp:
        decisionX, decisionY = self.x, self.y - 1
        angularToBe = 90.0
      elif decision==distanceDown:
        decisionX, decisionY = self.x, self.y + 1
        angularToBe = 270.0
      elif decision==distanceLeft:
        decisionX, decisionY = self.x - 1, self.y
        angularToBe = 0.0
      elif decision==distanceRight:
        decisionX, decisionY = self.x + 1, self.y
        angularToBe = 180.0

      if(self.isDecisionLegal(decisionX, decisionY)):
          finalDecision["stay"] = False
          finalDecision["clockwise"] = angularToBe - self.direction > 0
          finalDecision["angularSpeed"] = abs(angularToBe - self.direction)
          break

    return finalDecision



'''开始游戏'''

testMap = BasicMap(20,15)
testMap.setTarget(4,4)
# print testMap

testFriendlyShip = MyUSV(uid=0,x=5,y=5,env=testMap)
testFriendlyShip.setAsFriendly()
testMap.addShip(testFriendlyShip)
testFriendlyShip1 = MyUSV(uid=1,x=4,y=5,env=testMap)
testFriendlyShip1.setAsFriendly()
testMap.addShip(testFriendlyShip1)
testFriendlyShip2 = MyUSV(uid=2,x=5,y=4,env=testMap)
testFriendlyShip2.setAsFriendly()
testMap.addShip(testFriendlyShip2)
testFriendlyShip3 = MyUSV(uid=3,x=6,y=4,env=testMap)
testFriendlyShip3.setAsFriendly()
testMap.addShip(testFriendlyShip3)
testFriendlyShip4 = MyUSV(uid=4,x=5,y=6,env=testMap)
testFriendlyShip4.setAsFriendly()
testMap.addShip(testFriendlyShip4)
testFriendlyShip5 = MyUSV(uid=5,x=7,y=4,env=testMap)
testFriendlyShip5.setAsFriendly()
testMap.addShip(testFriendlyShip5)
testFriendlyShip6 = MyUSV(uid=6,x=7,y=5,env=testMap)
testFriendlyShip6.setAsFriendly()
testMap.addShip(testFriendlyShip6)
testFriendlyShip7 = MyUSV(uid=7,x=7,y=6,env=testMap)
testFriendlyShip7.setAsFriendly()
testMap.addShip(testFriendlyShip7)

testEnemyShip = MyUSV(uid=8,x=10,y=10,env=testMap)
testEnemyShip.setAsEnemy()
testMap.addShip(testEnemyShip)
# print testMap

game = BasicGame()
game.setMap(testMap)
game.start()