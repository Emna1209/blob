import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def rollDice():
    roll = random.randint(1,100)
    if roll == 100:
        return False
    elif roll <=50:
        return False
    elif 100 > roll > 50:
        return True    

def simple_bettor(funds, initial_wager, wager_count):

    value = funds
    wager = initial_wager
    wX = []
    vY = []
    currentWager = 1
    while(currentWager <= wager_count):
        if rollDice():
            value += wager
        else:
            value -= wager
        wX.append(currentWager)
        vY.append(value)
        currentWager += 1
    if value < 0:
        value = 'broke'
    plt.plot(wX,vY)

x = 0
while x<1000:
    simple_bettor(10000, 100, 100000)
    x += 1

plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.show()