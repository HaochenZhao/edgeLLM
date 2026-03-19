from gpiozero import RGBLED, Buzzer
from time import sleep

class HardwareController:
    def __init__(self, red_pin=17, green_pin=27, blue_pin=22, buzzer_pin=23):
        try:
            self.led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)
            self.buzzer = Buzzer(buzzer_pin)
            print(f"Hardware initialized: RGB LED (R:{red_pin}, G:{green_pin}, B:{blue_pin}), Buzzer ({buzzer_pin})")
        except Exception as e:
            print(f"Warning: Hardware initialization failed: {e}. Running in mock mode.")
            self.led = None
            self.buzzer = None

    def set_led(self, color=(0, 0, 0), brightness=1.0):
        print(f"Action: Setting LED color to {color} at {brightness*100}% brightness")
        if self.led:
            # color is expected to be (r, g, b) where each is 0-1
            self.led.value = tuple(c * brightness for c in color)

    def beep(self, duration=0.1):
        print(f"Action: Beeping for {duration}s")
        if self.buzzer:
            self.buzzer.on()
            sleep(duration)
            self.buzzer.off()

    def turn_off(self):
        print("Action: Turning off all hardware")
        if self.led:
            self.led.off()
        if self.buzzer:
            self.buzzer.off()

if __name__ == "__main__":
    # Test
    hw = HardwareController()
    hw.set_led((1,0,0), 0.5)
    hw.beep()
    sleep(1)
    hw.turn_off()
