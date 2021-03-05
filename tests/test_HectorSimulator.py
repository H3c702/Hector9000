from Hector9000.HectorSimulator import HectorSimulator as Hector
from Hector9000.conf import HectorConfig as config

hector = Hector(config.config)


def test_scale_readout():
    scale = hector.scale_readout()
    assert scale == 0


def test_Scale_Tare():
    tar = hector.scale_tare()
    assert tar == 0


def test_Pump():
    pump = hector.pump_start()
    assert pump == 1
    pump = hector.pump_stop()
    assert pump == 0


def test_Arm():
    hector.arm_out()
    armpos = False
    armpos = hector.arm_isInOutPos()
    assert armpos
    hector.arm_in()
    armpos = hector.arm_isInOutPos()
    assert not armpos


def test_light_off():
    light = hector.light_off()
    assert light == 0


def test_light_on():
    light = hector.light_on()
    assert light == 1


def test_getConfig():
    conf = hector.getConfig()
    assert conf is not None
