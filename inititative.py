import random
from operator import attrgetter


def roll(x):
    return random.randint(1, x)


class Character(object):  # Character class to be used in init list
    def __init__(self, name="NoName", initiative=0, dexscore=0, party=False):
        self.__name = name  # Character Name
        self.initiative = initiative  # Character init value (with mods)
        self.dexscore = dexscore  # Character dex score (for tie breakers)
        self.__party = party  # Determines if the character is a party member to save them between encounters

    def getname(self):
        return self.__name

    def setname(self, newname):
        self.__name = newname

    def getinit(self):
        return self.initiative

    def setinit(self, newinit):
        self.initiative = newinit

    def getdex(self):
        return self.dexscore

    def setdex(self, newdex):
        self.dexscore = newdex

    def getparty(self):
        return self.__party

    def setparty(self, newparty):
        self.__party = newparty

    def __repr__(self):
        return repr((self.__name, self.initiative, self.dexscore, self.__party))


def partyimport(initlist):
    party_file = open("party.csv")
    party_contents = party_file.readlines()[1:]
    party_file.close()
    for i in party_contents:
        charconts = i.split(",")
        initlist.append(Character(charconts[0], dexscore=int(charconts[1]), party=True))
    partystring = ""
    for i in range(len(initlist)):
        if i != len(initlist) - 1:
            partystring += initlist[i].getname() + ", "
        else:
            partystring += initlist[i].getname()
    print("\nSuccessfully imported party: " + partystring)


def setinits(initlist):
    print("Setting all initiatives:")
    for i in initlist:
        print(i.getname() + " Current init: " + str(i.getinit()))
        newinit = input("New init: ")
        if newinit[0:4].lower() == "roll":
            intnewinit = roll(int(newinit[4:])) + int(input("Roll Modifier: "))
        else:
            intnewinit = int(newinit)
        i.setinit(intnewinit)
    print("All inits set!\n")


def turnorder(initlist):
    initlist = sorted(initlist, key=attrgetter('initiative', 'dexscore'), reverse=True)
    useinp = ""
    print("=============================================\n\tTurn order has begun!"
          "\n=============================================")
    while useinp != "exit":
        i = 0
        while i != len(initlist):
            strcurrent = "Turn: " + initlist[i].getname() + "\nWhat would you like to do?\n\t(N)ext\n\t(" \
                                                            "P)revious\n\t(R)emove this character\n\t(D)elay this " \
                                                            "character\n\t(exit) "
            useinp = input(strcurrent)
            if useinp.lower() == "n":
                i += 1
            elif useinp.lower() == "p":
                i -= 1
            elif useinp.lower() == "r":
                initlist.pop(i)
            elif useinp.lower() == "exit":
                break
            elif useinp.lower() == "d":
                newinit = int(input("Enter this characters new init: "))
                initlist[i].setinit(newinit)
                initlist = sorted(initlist, key=attrgetter('initiative', 'dexscore'), reverse=True)
                if newinit > initlist[i].getinit():
                    i += 1
    print("")


def addcharacter(initlist):
    newname = input("What is this character's name? ")
    newinit = int(input("What is this character's init? "))
    newdex = int(input("What is this character's dex score? "))
    partymem = input("Is this a party member? (Y or N): ")
    if partymem.lower() == "y":
        newparty = True
        print("(Remember to add this character to the party.csv file later on!)")
    else:
        newparty = False
    initlist.append(Character(newname, newinit, newdex, newparty))
    print("New character added!\n")


def removenonparty(initlist):
    for i in range(len(initlist)-1, -1, -1):
        if not initlist[i].getparty():
            initlist.pop(i)


def main():
    print("=============================================\n\tWelcome to the Inititative System!"
          "\n=============================================")
    initlist = []
    partyimport(initlist)
    useinp = ""
    while useinp != "exit":
        useinp = input("What would you like to do?\n\t(S)et inits\n\t(A)dd a new character to the init list\n\t"
                       "(C)lear the init list to the default party members\n\t(B)egin the turn order\n\t(exit)\n")

        if useinp.lower() == "s":
            setinits(initlist)
        elif useinp.lower() == "b":
            turnorder(initlist)
        elif useinp.lower() == "a":
            addcharacter(initlist)
        elif useinp.lower() == "c":
            removenonparty(initlist)


if __name__ == '__main__':
    main()
