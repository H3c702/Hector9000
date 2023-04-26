 Chat:  Join the Chat at [Discord](https://discord.gg/MHJh4bBddY)
 
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=H3c702_Hector9000&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=H3c702_Hector9000)

| Branch  | Status |
| ------------- | ------------- |
| Master | [![Build Status(Master)](https://travis-ci.com/H3c702/Hector9000.svg?branch=master&label=master)](https://travis-ci.com/H3c702/Hector9000/branches) |
| Development  | [![Build Status](https://travis-ci.com/H3c702/Hector9000.svg?branch=development)](https://travis-ci.com/H3c702/Hector9000/branches)  |
 

HECTOR 9000
======================

Minimal Requirements 
---

	- RaspberryPi 3
	- Debian bases Linux (to use installscript)
    - Python 3.8

Prepare Raspberry
---
Activate I2C:

    sudo raspi-config 

Here go to "Interfacing Options" and Activate/Enable I2C 

Install on RaspberryPi
----
First you have to clone the github repo of Hector

	git clone https://github.com/H3c702/Hector9000.git

This repository doesn't contain a frontent. To get the original Hector9000 frontend see: 

	https://github.com/H3c702/Hector9000WebUI

To start the Hector software first move into the directory:

	cd Hector9000

Then run this command to setup all necessary tools:

	./setup.sh

Or run it with the option "-c" to preset the mqtt preconfigure for the WebUI

	./setup.sh -c

To start the software run:

	./start.sh


Add Drinks
---

To add a new Drink you have to modify the `drinks.py` file and add a new item into the `drink_list` array formatted as followed:

	{
        "name": "NAME OF DRINK",
        "recipe": [
            ("ingr", "INGREDIENT1", AMOUNT1),
            ("ingr", "INGREDIENT2", AMOUNT2)
        ]	
    }

All strings in `UPPERCASE` are placeholders, all lowercase strings have to be used literally in the definition. The `INGREDIENTx` names are not cleartext but are identifiers referencing into the `ingredients` list below in the same file. The `AMOUNTx` values are numerical values of the corresponding ingredient's amount in grams.

At the moment there are only some ingredients but feel free to put in some new. You can add them in src/Hector/conf/database.py .
Or you can use the WebUI when it is implemented.

A future extension might allow multi-language UIs.

Add Ingredients
---
To edit the Ingredients that can be used you can edit the 
database.py or use the tool in the tools folder.

    python3 Hector9000/tools/Editingredients.py


Assigning valves
---
The available ingredients are also moved to the db and can initial be edited in the databas.py 
or over the WEB UI in the future.

For the meantime you can use the script "SetValveIng.py".

    python3 Hector9000/tools/SetValveIng.py



Calibration of Loadcell 
---

HOW TO CALCULATE THE REFFERENCE UNIT
To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.

After you have calculate your reference then go to Hector9000/conf/HectorConfig.py
and set the 
    
    "hx711": {
        "ref": 2145  # REFERENCE VALUE
        }

Development on non-Hector hardware :
---

In the `HectorServer.py` you have to comment line :
	
	#from HectorHardware import HectorHardware as Hector

and uncomment:

	from HectorSimulator import HectorSimulator as Hector



## Info 

If you have some ideas or a fix or something else to make 
Hector better, don't be afraid to send us a pullrequest ;-)

---
Special thanks to
<div>

  <a href="https://www.jetbrains.com/pycharm/">
    <img alt="PyCharm" width="128" heigth="128" hspace="40" src="./images/PyCharm_logo.png">
  </a>

</div>

