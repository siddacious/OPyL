
import time
import board
import digitalio

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
BIT_TIME = 0.01
LOOP_TIME = .5
pv = {True : 1, False: 0}

class RWPin:
    """
    Single pin controller to manage R/W
    :param microcontroller.pin pin_name: The board pin to read and write from

    """

    def __init__(self, pin_name):
        self._pin_obj = digitalio.DigitalInOut(pin_name)
        self._pin_obj.direction = digitalio.Direction.OUTPUT

    def get(self):
        self._pin_obj.direction = digitalio.Direction.INPUT

        return pv[self._pin_obj.value]

    def set(self, value):
        self._pin_obj.direction = digitalio.Direction.OUTPUT
        if (value == 1) or (value == HIGH):
            self._pin_obj.value = True
        else:
            self._pin_obj.value = False

class Bus8Bit:
    """
    A class to manage an 8-bit R/W bus
    :param microcontroller.pin pin_name: The board pin to read and write from

    """

    def __init__(self, bus_pin_names):
        self._bus = []
        self._init_bus(bus_pin_names)

    def get(self):
        bus_value = 0
        for i in range(8):
            pin_val = (self._bus[i].get())
            bus_value |= pin_val << i
        return bus_value



    def set(self, value):
        if value < 0 or value > 255:
            raise AttributeError("value must be one byte")
        for i in range(8):
            self._bus[i].set((value >> i) & 0x1)

    def _init_bus(self, bus_pin_names):
        for i in range(8):
            self._bus.append(RWPin(bus_pin_names[i]))
            self._bus[i].set(LOW)

    def to_s(self):
        valstr = "0x"
        for i in range(7, -1, -1):
            valstr += str(self._bus[i].get())

        return valstr

HIGH = True
LOW = False
class OPL3:
    # _cs = RWPin(CS)
    def __init__(self, bus_pin_names, cs, a0, a1, ic, wr, rd):
        self._ic = RWPin(ic)
        self._cs = RWPin(cs)
        self._wr = RWPin(wr)
        self._rd = RWPin(rd)
        self.test = RWPin(board.A0)
        self._data_write = RWPin(a0)
        self._bank_select = RWPin(a1)

        self.bus = Bus8Bit(bus_pin_names)

    def read_status(self):
        # set control pins
        # A0=L
        self._data_write.set(LOW)
        # - Tas -10 ns
        # CS=L
        self._cs.set(LOW)
        # RD=L
        self._rd.set(LOW)
        # - Tacc - 150ns max(most you'll have to wait for data to be ready)
        value = self.bus.get()
        self._rd.set(HIGH)
        self._cs.set(HIGH)
        self._data_write.set(HIGH)
        return self.bus.get()
        # read bus

    def toggle_clock(self):
        start = time.monotonic_ns()
        self._cs.set(HIGH)
        while True:
            time.sleep(0.001)
            #1 000 000 000
            if (time.monotonic_ns()-start) > 10000000:
                self._cs.set(LOW)
                return
    
    def send(self, value):
        self.bus.set(value)
        self.toggle_clock()

if __name__ == "__main__":

    opl = OPL3(data_bus, CS, A0, A1, IC, WR, RD)

    print("made opl")
    while True:

        opl.send(0x01)
        opl.send(0x02)
        opl.send(0x04)
        opl.send(0x08)
        
        time.sleep(BIT_TIME)

        print("status:", bin(opl.read_status()))

        time.sleep(LOOP_TIME)
        print("--loop---")

