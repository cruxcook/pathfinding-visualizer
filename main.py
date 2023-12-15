import pygame, sys, os
from states.state_manager import *

def main():
    sm = StateManager()
    sm.run()
    
if __name__ == '__main__':
    main()