 Chat:  [![Join the Chat at https://gitter.im/Hector9k/Hector9000](https://img.shields.io/gitter/room/Hector9k/Hector9000?style=plastic)](https://gitter.im/Hector9k/Hector9000?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)  
 
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

Or run it with the option "-c" to preset the mqtt preconfig for the WebUI

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


Assigning valves
---

The available ingreduents are also moved to the db and can initial be edited in the databas.py 
or over the WEB UI in the future.

For teh meantime you can use the script "SetValveIng.py".

    python3 Hector9000/tools/SetValveIng.py


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

