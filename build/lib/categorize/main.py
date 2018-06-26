import os
import pygame

def main():
    response = 0

    while type(response) != str:
        print("We are currently in the directory " + os.getcwd())
        print("Would you like to turn this into a categorization directory? (y/N)")
        response = input()

        if type(response != str):
            print("Please only input a character")

    response = response.lower()[0]

    if response != 'y':
        print("Ending program")
        return

    os.system("mkdir .files")



if __name__ == "__main__":
    main()
