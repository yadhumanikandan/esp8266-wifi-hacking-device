import machine
import ssd1306
import time
import FakeAP_main


# Initialize I2C for the OLED display
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
global oled
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Menu options
menu_items = ["Option 1", "Option 2", "Option 3", "FAKE_AP", "Option 5", "Option 6", "Option 7", "hari", "yadhu", "", ""]
current_selection = 0

# Button setup
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)


button_press_count = 0

# Define a variable to track the last button press time
last_button_press_time = 0

# Define the double-click interval (in milliseconds)
double_click_interval = 500

#def button_click(pin):
#    global n
#    if n == len(menu_items)-3:
#        n=0
#    else:
#        n=n+1

def fakeAP():
    FakeAP_main.cap()
        
def button_click(pin):
    global n
    global button_press_count, last_button_press_time
    current_time = time.ticks_ms()

    # Check if it's a double click
    if (current_time - last_button_press_time) < double_click_interval and (button_press_count == 1):
        button_press_count += 1
        
        time.sleep_ms(double_click_interval)
        if button_press_count == 2:
            # This is a double click
            print("Double click detected")
            if n == 4:
                oled.fill(0)
                oled.text("Starting Fake-AP...", 0, 20)
                oled.show()
                fakeAP()
            # Add your double-click action here
            button_press_count = 0
    else:
        #global n
        if n == len(menu_items)-3:
            n=0
        else:
            n=n+1
        button_press_count = 1

    last_button_press_time = current_time


button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_click)

n=0

while True:
    oled.fill(0)
    oled.fill_rect(0, 0, 128, 17, 1)
    oled.text(">> "+menu_items[n], 0,5, 0)
    oled.text(menu_items[n+1], 0,25)
    oled.text(menu_items[n+2], 0,50)
    oled.show()

