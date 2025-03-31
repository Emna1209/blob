import random
import matplotlib
import matplotlib.pyplot as plt
import time

def rollDice():
    roll = random.randint(1,100)
    if roll == 100:
        return False
    elif roll <=50:
        return False
    elif 100 > roll > 50:
        return True    
    
def doubler_bettor(funds, initial_wager, wager_count):
    value = funds
    wager = initial_wager
    global broke_count
    wX = []
    vY = []
    currentWager = 1
    previousWager = 'win'
    previousWagerAmount = initial_wager

    while currentWager < wager_count:
        if previousWager == 'win':
            print('we won the last wager')
            if rollDice():
                value += wager
            else:
                value -= wager
                previousWager = 'loss'
                previousWagerAmount = wager
                if value < 0:
                    broke_count += 1
                    break
            wX.append(currentWager)
            vY.append(value)
        elif previousWager == 'loss':
            if rollDice():
                wager = previousWagerAmount * 2
                value += wager
                wager = initial_wager
                previousWager = 'win'
            else:
                wager = previousWagerAmount * 2
                value -= wager
                if value < 0:
                    broke_count += 1
                    break
                previousWager = 'loss'
                previousWagerAmount = wager
            wX.append(currentWager)
            vY.append(value)
        currentWager += 1
    print(value)
    plt.plot(wX, vY)

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

xx = 0
broke_count = 0

while xx < 100000:
    doubler_bettor(10000,100,1000)
    xx += 1

plt.ylabel('Account Value')
plt.xlabel('Wager Count')

death_rate = (broke_count/float(xx)) * 100
print('death rate:', death_rate)
print('survival rate:', 100 - death_rate)

plt.axhline(0, color='r')
plt.show() 
time.sleep(5)