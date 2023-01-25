import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Hector9000",
    version="0.1.0rc2",
    author="DevTown",
    author_email="Hector@dev-town.de",
    description="Fancy barbot with lots of needless features and ...of course... WiFi and a bunch of blinky LEDs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/H3c702/Hector9000",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
         "Natural Language :: English",
        "Natural Language :: German",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    'Adafruit-GPIO==1.0.3',
    'Adafruit-PCA9685==1.0.1',
    'Adafruit-PureIO>=1.1.5',
    'atomicwrites==1.3.0',
    'adafruit-circuitpython-neopixel==6.0.0',
    'attrs==19.1.0',
    'board==0.0.0.post0',
    'certifi==2022.12.7',
    'console-menu==0.7.1',
    'chardet==3.0.4',
    'docutils==0.14',
    'idna==2.8',
    'more-itertools==7.0.0',
    'packaging==19.0',
    'paho-mqtt==1.6.1',
    'pluggy==0.12.0',
    'py==1.10.0',
    'Pygments==2.7.4',
    'pyparsing==2.4.0',
    'requests==2.27.1',
    'six==1.12.0',
    'urllib3==1.26.5',
    'wcwidth==0.1.7',
    'webcolors==1.3',
    'zipp==3.1.0',
    ],
    extras_require={
        'dev': ['pytest', 'flake8', 'autopep8'],
        "pi": ['RPi.GPIO==0.7.0', 'spidev==3.5'],
    }
    ,
    entry_points={"console_scripts": ["HectorServer = Hector9000.HectorServer:main",
                                      "HectorController = Hector9000.HectorController:main",
                                      "LEDStripServer = Hector9000.LEDStripServer:main"]},
)
