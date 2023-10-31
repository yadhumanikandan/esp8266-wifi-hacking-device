import uos
import ssd1306
from machine import Pin, I2C

i2c = I2C(sda=Pin(4), scl=Pin(5))

display = ssd1306.SSD1306_I2C(128, 64, i2c)


class Creds:

    CRED_FILE = "./wifi.creds"

    def __init__(self, ssid=None, password=None):
        self.ssid = ssid
        self.password = password

    def write(self):
        """Write credentials to CRED_FILE if valid input found."""
        if self.is_valid():
            with open(self.CRED_FILE, "ab") as f:
                f.write("\nemail: " + str(self.ssid) + "\npassword: " + str(self.password) + "\n\n")
                # f.write(b",".join([self.ssid, self.password]))
            display.text(self.ssid, 0, 0)
            display.text(self.password, 0, 20)
            display.show()
            print("Wrote credentials to {:s}".format(self.CRED_FILE))

    def load(self):

        try:
            with open(self.CRED_FILE, "rb") as f:
                contents = f.read().split(b",")
            print("Loaded WiFi credentials from {:s}".format(self.CRED_FILE))
            if len(contents) == 2:
                self.ssid, self.password = contents

            if not self.is_valid():
                self.remove()
        except OSError:
            pass

        return self

    def remove(self):
        """
        1. Delete credentials file from disk.
        2. Set ssid and password to None
        """
        # print("Attempting to remove {}".format(self.CRED_FILE))
        try:
            pass
            #uos.remove(self.CRED_FILE)
        except OSError:
            pass

        self.ssid = self.password = None

    def is_valid(self):
        # Ensure the credentials are entered as bytes
        if not isinstance(self.ssid, bytes):
            return False
        if not isinstance(self.password, bytes):
            return False

        # Ensure credentials are not None or empty
        return all((self.ssid, self.password))
