from machine import Pin
import time
import random


"""
26 GPIO pins total on pico
20 GPIO Pins for columns, 6 pins for shift registers(3 each), one shift register for remaining 5 columns and one for all layers
The columns in the front face are controlled via shift register
layerShift[5] is white 4 red, etc
"""

grid = [[4, 3, 2, 1, 0],[9, 8, 7, 6, 5],[14,13,12,11,10],[22,21,17,16,15],[1001, 1002, 1003, 1004, 1005]] #GPIO pins, shift register pins will have there shift register sequence

#Shift register pins for extra columns
columnDataPin = machine.Pin(26, machine.Pin.OUT)
columnLatchPin = machine.Pin(27, machine.Pin.OUT)
columnClockPin = machine.Pin(28, machine.Pin.OUT)

#Shift register pins for layers
layerDataPin = machine.Pin(19, machine.Pin.OUT)
layerLatchPin = machine.Pin(20, machine.Pin.OUT)
layerClockPin = machine.Pin(18, machine.Pin.OUT)

spiralDelay = 0.1

columnShift = list("00000000")#string to hold instructions for column shift register

layerShift = list("0000000000")#string to hold instructions for layer shift register



def updateColumn():#Activating a column via shift register and columnSHift sequence
    columnLatchPin.value(0)
    #print (columnShift)
    for i in range(0, 8):
        columnDataPin.value(int(columnShift[i-1]))
        columnClockPin.value(1)
        columnClockPin.value(0)
    columnLatchPin.value(1)
    
def updateLayer():#Activating layer via shift register
    layerLatchPin.value(0)
    #print(layerShift)
    for i in range(8): #8 GP pins in shift register
        #print(int(layerShift[i-1]))
        layerDataPin.value(int(layerShift[i-1]))
        layerClockPin.value(1)
        layerClockPin.value(0)
    layerLatchPin.value(1)
    #print("end\n")
def resetAll():
    resetColumns()
    resetLayers()

def columnOff():
    pass
def layerOff():
    pass

def allColumns(): #Activate all columns including shift register columns
    for i in range(0, 23): 
        if i < 18 or i > 20: #Pins 18,19,20 are shift register pins
            machine.Pin(i, machine.Pin.OUT).value(1)
    for i in range(8):
       columnShift[i] = "1"
    updateColumn()

def bgwLayers(): #Turn on blue, green, white layers
    layerShift[1] = "1"
    layerShift[3] = "1"
    layerShift[5] = "1"
    updateLayer()
            
def resetColumns(): #Turn off all columns including shift register columns
    for i in range(0, 23): #Turn off output for all non shift register GPIO pins
        if i < 18 or i > 20:    
            machine.Pin(i, machine.Pin.OUT).value(0)
    for i in range(5, -1, -1):
       columnShift[i+1] = "0"
    updateColumn()
    print("Restting columns")
    
def resetLayers(): #Turn off all layers 
    for i in range(0, 8):
        layerShift[i] = "0"
    updateLayer()
    print("resetting layers")

def bottomToTop(t): #Turn on layers from bottom to top with given time delay
    for i in range(1, 6):
        layerShift[i] = "1"
        updateLayer()
        time.sleep(t)
        layerShift[i] = "0"
        updateLayer()
    
def pattern1(): #Light up layers one by one, top to bottom, inverse of pattern3
    allColumns()
    for i in range(6, -3, -1):
        layerShift[i+1] = "1"
        updateLayer()
        time.sleep(0.3)
        layerShift[i+1] = "0"
        updateLayer()

def pattern3(): #Light up one by one bottom to top, inverse of pattern1
    allColumns()
    for i in range(2, 7):
        layerShift[i-1] = "1"
        updateLayer()
        time.sleep(0.3)
        layerShift[i-1] = "0"
        updateLayer()
        
        
def pattern2(): #bottom to top left to right, inverse of pattern4
    '''layerShift[2] = "1"
    layerShift[4] = "1"'''
    for i in range(0, 5):
        layerShift[i+1] = "1"
        updateLayer()
        for i in range(0, 5):
            columnShift[i+1] = "1"
            updateColumn()
            for j in range(0, 5):
                if grid[j][i] < 1000:
                    machine.Pin(grid[j][i], machine.Pin.OUT).value(1)
            time.sleep(0.1)
            columnShift[i+1] = "0"
            for j in range(0, 5):
                if grid[j][i] < 1000:
                    machine.Pin(grid[j][i], machine.Pin.OUT).value(0)
            updateColumn()
        resetLayers()
#97 11 26
def pattern4(): #Top to bottom, right to left, inverse of pattern2
    for i in range(5, 0, -1):
        layerShift[i] = "1"
        updateLayer()
        for i in range(4, -1, -1):
            columnShift[i+1] = "1"
            updateColumn()
            for j in range(0, 5):
                if grid[j][i] < 1000:
                    machine.Pin(grid[j][i], machine.Pin.OUT).value(1)
            time.sleep(0.1)
            columnShift[i+1] = "0"
            for j in range(4, -1, -1):
                if grid[j][i] < 1000:
                    machine.Pin(grid[j][i], machine.Pin.OUT).value(0)
            updateColumn()
        resetLayers()
    
def pattern5(): #Random Raindrops
    
    for i in range(0, 15):
        col = random.randint(0, 4)
        row = random.randint(0, 4)
        if grid[col][row] < 1000:
            machine.Pin(grid[col][row], machine.Pin.OUT).value(1)
        else:
            columnShift[col] = "1" 
            updateColumn()
        for i in range(4, -1, -1):
            layerShift[i+1] = "1"
            updateLayer()
            time.sleep(0.1)
            layerShift[i+1] = "0"
            updateLayer()
        resetAll()
        
        
def pattern6(): #Spiral
    for i in range(5, 0, -1):
        layerShift[i] = "1"
        updateLayer()
        for j in range(0, 5):
            machine.Pin(grid[0][j], machine.Pin.OUT).value(1)
            columnShift[5-j] = "1"
            updateColumn()
            time.sleep(spiralDelay)
            machine.Pin(grid[0][j], machine.Pin.OUT).value(0)
            columnShift[5-j] = "0"
            updateColumn()
            
        for j in range(1, 5):
            machine.Pin(grid[4-j][0], machine.Pin.OUT).value(1)
            if grid[j][4] < 1000:
                machine.Pin(grid[j][4], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
                machine.Pin(grid[j][4], machine.Pin.OUT).value(0)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                columnShift[j+1] = "0"
                updateColumn()
            machine.Pin(grid[4-j][0], machine.Pin.OUT).value(0)
        for j in range(3, -1, -1):
            machine.Pin(grid[0][4-j], machine.Pin.OUT).value(1)
            if grid[4][j] < 1000:
                machine.Pin(grid[4][j], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
                machine.Pin(grid[4][j], machine.Pin.OUT).value(0)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                columnShift[j+1] = "0"
                updateColumn()
            machine.Pin(grid[0][4-j], machine.Pin.OUT).value(0)
        for j in range(3, 0, -1):
            machine.Pin(grid[4-j][4], machine.Pin.OUT).value(1)
            if grid[j][0] < 1000:
                machine.Pin(grid[j][0], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
                machine.Pin(grid[j][0], machine.Pin.OUT).value(0)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                columnShift[j+1] = "0"
                updateColumn()
            machine.Pin(grid[4-j][4], machine.Pin.OUT).value(0)
        resetAll()
        
                    
def patternName(): #My name
    letterDelay = 0.4
    #C
    updateLayer()
    for i in range(1, 5):
        machine.Pin(grid[0][i], machine.Pin.OUT).value(1)
        columnShift[i+1] = "1"
    
    for i in range(1, 4):
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
    updateColumn()
    bottomToTop(letterDelay)
    resetColumns()
    #A
    for i in range(1,4):
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
        machine.Pin(grid[i][4], machine.Pin.OUT).value(1)
    columnShift[1] = "1"
    columnShift[5] = "1"
    updateColumn()
    for i in range(1,4):
        machine.Pin(grid[0][i], machine.Pin.OUT).value(1)
        machine.Pin(grid[2][i], machine.Pin.OUT).value(1)
    bottomToTop(letterDelay)
    resetColumns()
    
    #M
    for i in range(0, 4):
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
        machine.Pin(grid[i][4], machine.Pin.OUT).value(1)
    columnShift[1] = "1"
    columnShift[5] = "1"
    updateColumn()
    machine.Pin(grid[1][1], machine.Pin.OUT).value(1)
    machine.Pin(grid[1][3], machine.Pin.OUT).value(1)
    machine.Pin(grid[2][2], machine.Pin.OUT).value(1)
    bottomToTop(letterDelay)
    resetColumns()

    #E
    for i in range(0, 5):
        machine.Pin(grid[0][i], machine.Pin.OUT).value(1)
        machine.Pin(grid[2][i], machine.Pin.OUT).value(1)
        columnShift[i+1] = "1"
    machine.Pin(grid[1][0], machine.Pin.OUT).value(1)
    machine.Pin(grid[3][0], machine.Pin.OUT).value(1)
    updateColumn()
    bottomToTop(letterDelay)
    resetColumns()
    
    #R
    for i in range(0, 4):
        machine.Pin(grid[0][i], machine.Pin.OUT).value(1)
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
        machine.Pin(grid[2][i], machine.Pin.OUT).value(1)
    columnShift[1] = "1"
    columnShift[5] = "1"
    machine.Pin(grid[1][4], machine.Pin.OUT).value(1)
    machine.Pin(grid[3][3], machine.Pin.OUT).value(1)
    updateColumn()
    bottomToTop(letterDelay)
    resetColumns()
    
    #O
    for i in range(0, 5):
        machine.Pin(grid[0][i], machine.Pin.OUT).value(1)
    for i in range(0, 4):
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
        machine.Pin(grid[i][4], machine.Pin.OUT).value(1)
    for i in range(1, 6):
        columnShift[i] = "1"
    updateColumn()
    bottomToTop(letterDelay)
    resetColumns()
    
    #N
    for i in range(0, 4):
        machine.Pin(grid[i][0], machine.Pin.OUT).value(1)
        machine.Pin(grid[i][4], machine.Pin.OUT).value(1)
    for i in range(1, 4):
        machine.Pin(grid[i][2], machine.Pin.OUT).value(1)
    machine.Pin(grid[0][1], machine.Pin.OUT).value(1)
    columnShift[1] = "1"
    columnShift[4] = "1"
    columnShift[5] = "1"
    updateColumn()
    bottomToTop(letterDelay)
    resetColumns()
        
def pattern7(): #Spiral2
    for i in range(5, 0, -1):
        layerShift[i] = "1"
        updateLayer()
        for j in range(0, 5):
            machine.Pin(grid[0][j], machine.Pin.OUT).value(1)
            updateColumn()
            time.sleep(spiralDelay)
            updateColumn()
            
        for j in range(1, 5):
            if grid[j][4] < 1000:
                machine.Pin(grid[j][4], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                updateColumn()
            
        for j in range(3, -1, -1):
            if grid[4][j] < 1000:
                machine.Pin(grid[4][j], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                updateColumn()
        for j in range(3, 0, -1):
            if grid[j][0] < 1000:
                machine.Pin(grid[j][0], machine.Pin.OUT).value(1)
                time.sleep(spiralDelay)
            else:
                columnShift[j+1] = "1"
                updateColumn()
                time.sleep(spiralDelay)
                updateColumn()
            
        resetAll()
        
def pattern8():#Wave pattern
    wave = [2, 1, 0, 1, 2]
    direction = ['L', 'L', 'R', 'R', 'R'] #Stores which direction the wave is going at this index
    bgwLayers()
    for i in range(0, 150):
        for i in range(0, 4):
            machine.Pin(grid[i][wave[i]]).value(1)
            if direction[i] == 'L':
                wave[i]-=1
            else:
                wave[i]+=1
            if wave[i] == 0:
                direction[i] = 'R'
            elif wave[i] == 4:
                direction[i] = 'L'
        #Shift register column
        columnShift[wave[4]+1] = "1"
        updateColumn()
        if direction[4] == 'L':
                wave[4]-=1
        else:
            wave[4]+=1
        if wave[4] == 0:
            direction[4] = 'R'
        elif wave[4] == 4:
            direction[4] = 'L'
                
        time.sleep(0.1)
        resetColumns()
        
def main():
    
    resetAll()
    pattern1()
    
    resetAll()
    pattern2()
    
    resetAll()
    pattern3()
    
    resetAll()
    pattern4()
    
    resetAll()
    pattern5()
    
    resetAll()
    pattern6()
    
    resetAll()
    pattern7()
    
    resetAll()
    pattern8()
    
    resetAll()
    patternName()
    
    resetAll()
    
if __name__ == "__main__":
    main()











