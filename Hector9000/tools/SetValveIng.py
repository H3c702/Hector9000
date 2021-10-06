from Hector9000.conf.database import Database as hdb

db = hdb()


def get_IngLists():
    inglist = db.get_AllIngredients()
    counter = 0
    print("Select a ing")

    for x in inglist:
        print(str(counter) + ": " + x[0] + " | " + x[1])
        counter = counter + 1

    ing: int = -2

    while ing == -2:
        try:
            ing: int = int(input("Chose a ingredient(exit with -1):"))

            if ing == -1:
                quit()

            return inglist[ing]

        except ValueError:

            print("Oops!  That was no valid number.  Try again...")




def get_Valves():
    servs = db.get_Servos_asList()
    print("Vales | Ing")

    counter = 1

    for x in servs:
        print(str(counter) + ": " + x)
        counter += 1

    print("----------------------------------------------------")


while True:
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    get_Valves()

    ing = get_IngLists()
    try:
        valve: int = int(input("Chose a valve (1-12):"))

        if 0 < valve <= 12:
            print(ing[1] + " goes into " + str(valve))
            db.set_Servo(valve, ing[0])
        if valve == 13:
            print("------------------")
            print(db.get_AllIngredients_asJson())
            print("------------------")
        if valve == 14:
            print("------------------")
            print(db.get_Servos_asJson())
            print("------------------")

    except ValueError:
        print("Oops!  That was no valid number.  Try again...")


