from Hector9000.conf.database import Database as hdb

db = hdb()


def print_IngList():
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    inglist = db.get_AllIngredients()
    counter = 0
    print("Ing List:")

    for x in inglist:
        print(str(counter) + ": " + x[0] + " | " + x[1])
        counter = counter + 1

    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    pass


def add_Ing():
    shortname: str = str(input("Enter shortform:"))
    longname: str = str(input("Enter longname:"))
    isAlcoholic: int = int(input("Is Alcholic(1=yes 0=false):"))

    if isAlcoholic > 1:
        isAlcoholic = 1
    if isAlcoholic < 0:
        isAlcoholic = 0

    db.add_Ingredient(shortname, longname, isAlcoholic)

    print_IngList()
    pass


def dell_Ing():
    print_IngList()

    index: int = int(input("Please enter number:"))
    print("DELETE: " + db.get_AllIngredients()[index][0])
    db.delete_Ingredient(db.get_AllIngredients()[index][0])
    pass


while True:
    function: int = 0

    print("1 -> print Ing List")
    print("2 -> Add new Ing")
    print("3 -> Delte Ing")

    print("10 -> print Ing List")

    function = int(input("Chose function:"))

    try:
        if function == 1:
            print_IngList()
        if function == 2:
            add_Ing()
        if function == 3:
            dell_Ing()
        if function == 10:
            print("------------------")
            print(db.get_AllIngredients_asJson())
            print("------------------")
        if function == -4:
            print("------------------")
            print(db.get_Servos_asJson())
            print("------------------")

    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
