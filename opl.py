
class RWPin:
    """
    Single pin controller to manage R/W
    :param microcontroller.pin pin_name: The board pin to read and write from

    """

    def __init__(self, pin_name):
        self._pin_obj = digitalio.DigitalInOut(pin_name)
        self._pin_obj.direction = digitalio.Direction.OUTPUT

    def __get__(self, obj, objtype=None):
        self._pin_obj.direction = digitalio.Direction.INPUT
        return self._pin_obj.value

    def _init_pin(self, pin_name):

    def __set__(self, obj, value):
        self._pin_obj.direction = digitalio.Direction.OUTPUT
        self._pin_obj.value = value

class Bus8Bit:
    """
    A class to manage an 8-bit R/W bus
    :param microcontroller.pin pin_name: The board pin to read and write from

    """

    def __init__(self, bus_pin_names):
        self._init_bus(bus_pin_names)

    def __get__(self, obj, objtype=None):
        bus_value = 0
        mask = 0x0
        for i in range(8):
            bus_value |= (self._bus[i].value) << (7-i)
        return bus_value

    def _init_pin(self, pin_name):

    def __set__(self, obj, value):
        if value < 0 or value > 255:
            raise AttributeError("value must be one byte")
        for i in range(8):
            self._bus[i].value = (value >> i) & 0x1

    def _init_bus(self, bus_pin_names):
        for i in range(8):
            pin_obj = digitalio.DigitalInOut(bus_pin_names[i])
            pin_obj.direction = digitalio.Direction.OUTPUT
            self._bus.append(pin_obj)
            self._bus[i].value = LOW

    # def __str__(self):
    #     val = self.__get__(self)
    #     for i in range(7, -1, -1):
    #         pin_level = -1
    #         pin_val =self._bus[i].value
    #         if pin_val is True:
    #             pin_level = 1
    #         else:
    #             pin_level = 0
    #         print(pin_level, end="")
    #     print("")

    def set_bus(self, value):


import time
import board
import digitalio
HIGH = True
LOW = False
class OPL3:
    def __init__(self, bus_pin_names, cs, a0, a1, ic, wr, rd):
        self._bus = []
        self._ic = RWPin(ic)
        self._cs = RWPin(cs)
        self._wr = RWPin(wr)
        self._rd = RWPin(rd)
        self._data_write = RWPin(a0)
        self._bank_select = RWPin(a1)
        self._wr = RWPin(wr)

        self.bus = Bus8Bit(bus_pin_names)


    # def _init_pin(self, pin_name):
    #     pin_obj = digitalio.DigitalInOut(pin_name)
    #     pin_obj.direction = digitalio.Direction.OUTPUT
    #     return pin_obj

    def read_status(self):
        # set control pins
        # A0=L
        self._data_write = LOW
        # - Tas -10 ns
        # CS=L
        self._cs= LOW
        # RD=L
        self._rd = LOW
        # - Tacc - 150ns max(most you'll have to wait for data to be ready)
        return self.bus
        # read bus

    def toggle_clock(self):
        start = time.monotonic_ns()
        self._wr_cs.value = True
        while True:
            time.sleep(0.001)
            #1 000 000 000
            if (time.monotonic_ns()-start) > 10000000:
                self._wr_cs.value = False
                return



if __name__ == "__main__":
    data_bus = [
        board.RX,
        board.TX,
        board.D7,
        board.D9,
        board.D10,
        board.D11,
        board.D13,
        board.D12
    ]

    
    IC = board.D2
    A0 = board.MISO
    A1 = board.MOSI
    WR = board.SCK
    RD = board.A5
    CS = board.A4

    opl = OPL3(data_bus, CS, A0, A1, IC, WR, RD)
    BIT_TIME = 0.01
    LOOP_TIME = 0.5
    print("made opl")
    while True:
        opl.bus = 0xFF
        opl.toggle_clock()
        time.sleep(BIT_TIME)
        opl.bus = 0x1
        opl.toggle_clock()
        time.sleep(BIT_TIME)
        # opl.set_bus(0x20)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x10)
        # opl.toggle_clock()

        # opl.set_bus(0x01)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x02)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x04)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x08)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)

        # opl.set_bus(0xF0)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x0F)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0xF0)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        # opl.set_bus(0x0F)
        # opl.toggle_clock()
        # time.sleep(BIT_TIME)
        time.sleep(LOOP_TIME)
        print("--loop---")

