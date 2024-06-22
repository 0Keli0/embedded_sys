# ds3231.py

from machine import I2C
import utime

DS3231_I2C_ADDR = 0x68

class DS3231:
    def __init__(self, i2c, addr=DS3231_I2C_ADDR):
        self.i2c = i2c
        self.addr = addr

    def _bcd_to_dec(self, bcd):
        return (bcd // 16) * 10 + (bcd % 16)

    def _dec_to_bcd(self, dec):
        return (dec // 10) * 16 + (dec % 10)

    def datetime(self, dt=None):
        if dt is None:
            buf = self.i2c.readfrom_mem(self.addr, 0x00, 7)
            return (
                self._bcd_to_dec(buf[6]) + 2000,
                self._bcd_to_dec(buf[5]),
                self._bcd_to_dec(buf[4]),
                self._bcd_to_dec(buf[3]),
                self._bcd_to_dec(buf[2]),
                self._bcd_to_dec(buf[1]),
                self._bcd_to_dec(buf[0]),
                0
            )
        else:
            self.i2c.writeto_mem(self.addr, 0x00, bytes([
                self._dec_to_bcd(dt[6]),  # Second
                self._dec_to_bcd(dt[5]),  # Minute
                self._dec_to_bcd(dt[4]),  # Hour
                self._dec_to_bcd(dt[3]),  # Weekday
                self._dec_to_bcd(dt[2]),  # Day
                self._dec_to_bcd(dt[1]),  # Month
                self._dec_to_bcd(dt[0] - 2000)  # Year
            ]))

    def set_time(self, year, month, day, weekday, hour, minute, second):
        self.datetime((year, month, day, weekday, hour, minute, second, 0))

    def get_time(self):
        return self.datetime()
