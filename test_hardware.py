import time
from gpiozero import RGBLED, Buzzer
from gpiozero.pins.lgpio import LPiFactory

# Use lgpio factory for Pi 5 compatibility
factory = LPiFactory()

def test_hardware():
    print("--- Edge LLM Hardware Debugging Tool ---")
    
    try:
        led = RGBLED(red=17, green=27, blue=22, active_high=True, pin_factory=factory)
        buzzer = Buzzer(23, pin_factory=factory)
        
        print("\n1. Testing LED: Red")
        led.color = (1, 0, 0)
        time.sleep(1)
        
        print("2. Testing LED: Green")
        led.color = (0, 1, 0)
        time.sleep(1)
        
        print("3. Testing LED: Blue")
        led.color = (0, 0, 1)
        time.sleep(1)
        
        print("4. Testing LED: White (All on)")
        led.color = (1, 1, 1)
        time.sleep(1)
        
        led.off()
        
        print("5. Testing Buzzer: Beep")
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        
        print("\nHardware Test Completed Successfully!")
        print("If you didn't see the colors or hear the beep, check your wiring and resistors.")
        
    except Exception as e:
        print(f"\nError initializing hardware: {e}")
        print("Ensure 'python3-lgpio' is installed and you have correct permissions.")

if __name__ == "__main__":
    test_hardware()
