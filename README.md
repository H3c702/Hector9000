HECTOR 9000 - Hardware
======================

Min requirements
---

	- Python 3
	- Kivy 
	- RaspberryPi 3

Install on RaspberryPi
----
First of all you have to install Python3 and Kivi on your RaspberryPi. 
For this there  is a HowTo on the Kivi Homepage : 		

	https://kivy.org/doc/stable/installation/installation-rpi.html

After you habe installed Python and Kivy you can get you the sources by using Git

	git clone https://github.com/H3c702/Hector9000.git

have to install all the requiremets listend in the requirement.txt by using pip

	pip3 install -r requirements.txt



Development on not Pi-Mashine :
--

	If you are on a not RaspberryPi you can set the Var in Hectorhardware.py 

	devenvirement = True

	If you are in Production or dev direct on a Pi you can set this var to False.
