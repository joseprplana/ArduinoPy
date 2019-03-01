import sys, time
from pyfirmata import Arduino, util

board = Arduino('/dev/cu.wchusbserialfa13240')
time.sleep(1.0)

while(True):
    board.digital[2].write(1)
    print(board.digital[2].read())
    time.sleep(1.0)
    board.digital[3].write(1)
    time.sleep(1.0)
    board.digital[2].write(0)
    time.sleep(1.0)
    board.digital[3].write(0)
    time.sleep(1.0)