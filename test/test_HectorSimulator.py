import pytest
from src.HectorSimulator import HectorSimulator as Hector
from src.conf.HectorConfig import config


class Test_Hectorsimulator():
    hector = Hector(config)

    def test_scale_readout(self):
        scale = self.hector.scale_readout()
        assert scale == 0

    def test_Scale_Tare(self):
        tar = self.hector.scale_tare()
        assert tar == 0

    def test_Pump(self):
        pump = self.hector.pump_start()
        assert pump == 1
        pump = self.hector.pump_stop()
        assert pump == 0

    def test_Arm(self):
        self.hector.arm_out()
        armpos = False
        armpos = self.hector.arm_isInOutPos()
        assert armpos
        self.hector.arm_in()
        armpos = self.hector.arm_isInOutPos()
        assert not armpos

    def test_light_off(self):
        light = self.hector.light_off()
        assert light == 0

    def test_light_on(self):
        light = self.hector.light_on()
        assert light == 1

    def test_getConfig(self):
        conf = self.hector.getConfig()
        assert conf is not None
