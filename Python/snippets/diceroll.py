#diceroll.py
"""
Diceroll.py
Author: John Cooper Hopkin
22 November 2018
A script to roll groups of dice and determine the individual group total
and full total
"""
import sys
import re
import random

def isValid(inString):
    if re.search("^([\d]+)g([\d]+)d([\d]+)$", inString, re.IGNORECASE):
        return True
    elif re.search("([\d]+)g ([\d]+)d ([\d]+)", inString, re.IGNORECASE):
        return True
    else:
        #print("Input not valid.")
        return False

def groupParse(inString):
    if re.search("^([\d]+)g([\d]+)d([\d]+)$", inString, re.IGNORECASE):
        regex = re.search("^([\d]+)g([\d]+)d([\d]+)$", inString, re.IGNORECASE)
        return int(regex[1]), int(regex[2]), int(regex[3])
    elif re.search("([\d]+)g ([\d]+)d ([\d]+)", inString, re.IGNORECASE):
        regex = re.search("([\d]+)g ([\d]+)d ([\d]+)", inString, re.IGNORECASE)
        return int(regex[1]), int(regex[2]), int(regex[3])


def totalRoll(groups, number, die):
    #TODO Implement rolling function (print to console)
    #input("Inside the totalRoll func")
    groupTotals = []

    for i in range(groups):

        total = 0
        for j in range(number):
            total += random.randrange(1,die+1)
        groupTotals.append(total)


    #print out list of group totals, then total
    print("Group totals: ",end='')
    for i in range(len(groupTotals)-1):
        print(groupTotals[i], end=", ")
    print(groupTotals[-1])
    
    print()
    print("Final Total:", sum(groupTotals))


def dynamic():
    #TODO: Implement manual Input mode (0 to exit)
    try:
        while(True):
            # set groups to -1 for exception logic if user inputs 
            # invalid input
            groups = -1
            groups = int(input("Enter the number of dice groups or 0 to return to main menu: "))
            if (groups == 0):
                return
            elif (groups < 0):
                raise Exception("You can't have a negative group number!")

            #number of dice
            number = int(input("Enter the number of dice to roll: "))
            if (number < 1):
                raise Exception("You can't roll less than 1 die!")

            #type of die
            die = int(input("Enter the type of die: "))
            if (die < 2):
                raise Exception("Why would you want a die with less than two sides?")

            #roll the dice
            totalRoll(groups, number, die)
    
    except ValueError:
        print("Invalid Argument!")
        
    except Exception as inst:
        print(inst.args[0])
        
    finally:
        if groups == 0 or input("Press Enter to try again, or enter 0 to return to main menu: ") == "0":
            return
        else:
            main()

def main():
    try:
        choicetype = input("Enter your roll syntax (XgYdZ), press enter to specify your roll dynamically, or enter 0 to exit: ")
        if choicetype == '':
            dynamic()
        elif choicetype == "0":
            print("Goodbye!")
            return
        elif isValid(choicetype):
            totalRoll(*groupParse(choicetype))
        else:
            print("Invalid input!")
        main()
    except:
        print("Goodbye!")
        
    
if __name__ == "__main__":
    print("Rolls can be specified in two ways:")
    print("\tDynamically, where you enter the number of rolls, number of dice, and type of dice when it prompts you")
    print("\tSyntactically, where you enter your roll in the format XgYdZ, where:")
    print("\t\tX is the number of rolls")
    print("\t\tY is the number of dice") 
    print("\t\tand Z is the number of faces on the die.")
    print()
    main()
  
  