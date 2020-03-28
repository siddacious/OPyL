# An official method of Adlib (OPL2) detection is:

#Reset Timer 1 and Timer 2: 
# write 60h to register 4
# Reset the IRQ: 
# write 80h to register 4.
#    Note: Steps 1 and 2 can't be combined together.
 #.Read status
#  read port base+0 (388h) and save the result
# .Set Timer 1 to FFh: 
# write FFh to register 2  
#  -- Unmask and start Timer 1
# write 21h to register 4.
# Wait in a delay loop for at least 80 usec.
#Read status Save the result. 
# read port base+0 (388h). 
# Reset Timer 1, Timer 2 and IRQ as in steps 1 and 2.
# Test the results of the two reads:
#  the first should be 0, the second should be C0h. If either is incorrect, then the OPL2 is not present.

# Notes:

# You should AND the result bytes with E0h because the unused bits are undefined.
# This testing method doesn't work in some SoundBlaster compatible cards.
# OPL3 Detection
# Detect OPL2. If present, continue.
# Read status register: read port base+0.
# AND the result with 06h.
# If the result is zero, you have OPL3, otherwise OPL2.
# Note: This is NOT an official method. I have dug it out of a sound driver. I haven't tested it, because I haven't an OPL2 card (Adlib, SB Pro I). Nevertheless it "detects" my SB Pro II properly. ;-)
# Another possible detection method for distinguishing between SB Pro I and SB Pro II would be to try to detect OPL2 at I/O port base+0 and then at port base+2. The first test should succeed and the second should fail if OPL3 is present. (Remember: SB Pro I contains twin OPL2 chips at addresses base+0 and base+2, while SB Pro II contains one OPL3 chip at I/O address base+0 thru base+3).



# set up pin aliases for data bus, address pins, cs/wr, and IC#
    #   A0 -- microcontroller.pin.A0
    #   A1 -- microcontroller.pin.A1
    #   A2 -- microcontroller.pin.A2
    #   A3 -- microcontroller.pin.A3
    #   A4 -- microcontroller.pin.A4
    #   A5 -- microcontroller.pin.A5
    #   D0 -- microcontroller.pin.D0
    #   RX -- microcontroller.pin.D0
    #   D1 -- microcontroller.pin.D1
    #   TX -- microcontroller.pin.D1
    #   D2 -- microcontroller.pin.D2
    #   D3 -- microcontroller.pin.D3
    #   D4 -- microcontroller.pin.D4
    #   D5 -- microcontroller.pin.D5
    #   D7 -- microcontroller.pin.D7
    #   D9 -- microcontroller.pin.D9
    #   D10 -- microcontroller.pin.D10
    #   D11 -- microcontroller.pin.D11
    #   D12 -- microcontroller.pin.D12
    #   D13 -- microcontroller.pin.D13
    #   SDA -- microcontroller.pin.SDA
    #   SCL -- microcontroller.pin.SCL
    #   SCK -- microcontroller.pin.SCK
    #   MOSI -- microcontroller.pin.MOSI
#   MISO -- microcontroller.pin.MISO
import time
import board
import digitalio
class OPL3:
    def __init__(self, bus_pin_names, ic, wr_cs, a0, a1):
        self._bus = []
        self._ic = ic
        self._wr_cs = wr_cs
        self._addr=[a0, a1]
        self._init_bus(bus_pin_names)

    def _init_bus(self, bus_pin_names):
        for i in range(8):
            # pin_obj = digitalio.DigitalInOut(bus_pin_names[i])
            # pin_obj.direction = digitalio.Direction.OUTPUT
            self._bus.append(self._init_pin(bus_pin_names[i]))

    def _init_pin(pin_name):
        pin_obj = digitalio.DigitalInOut(pin_name)
        pin_obj.direction = digitalio.Direction.OUTPUT
        return pin_obj


    def print_bus(self):
        print("0x", end="")
        for i in range(7, -1, -1):
            pin_level = -1
            pin_val =self._bus[i].value
            if pin_val is True:
                pin_level = 1
            else:
                pin_level = 0
            print(pin_level, end="")
        print("")
    def set_bus(self, value):
        if value < 0 or value > 255:
            raise AttributeError("value must be one byte")
        for i in range(8):
            self._bus[i].value = (value >> i) & 0x1
        self.print_bus()

    def toggle_clock(self):
        self._wr_cs


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
    WR_CS = board.MISO
    A0 = board.SCK
    A1 = board.MOSI
    opl = OPL3(data_bus, IC, WR_CS, A0, A1)
    BIT_TIME = 0.10
    LOOP_TIME = 0.5
    print("made opl")
    while True:
        opl.set_bus(0x80)
        time.sleep(BIT_TIME)
        opl.set_bus(0x40)
        time.sleep(BIT_TIME)
        opl.set_bus(0x20)
        time.sleep(BIT_TIME)
        opl.set_bus(0x10)
        time.sleep(BIT_TIME)
        opl.set_bus(0xF0)
        time.sleep(BIT_TIME)
        opl.set_bus(0x0F)
        time.sleep(BIT_TIME)
        time.sleep(LOOP_TIME)
        print("--loop---")

