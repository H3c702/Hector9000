from conf.database import Database as hdb

db = hdb()

def get_IngLists():
    inglist = db.get_AllIngredients()
    counter = 0
    print("Select a ing")

    for x in inglist:
        print(str(counter) + ": " + x[0])
        counter = counter + 1

    ing: int = int(input("Chose a ingredient(exit with -1):"))

    if ing == -1:
        return ""

    return inglist[ing]


while True:
    ing = get_IngLists()
    valve: int = int(input("Chose a valve (1-12):"))

    print(ing[1] +" goes into " + str(valve))
