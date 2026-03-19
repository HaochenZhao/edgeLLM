import sys
import os

# Add current directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hardware_control import HardwareController
from llm_interface import LLMInterface

def main():
    hw = HardwareController()
    llm = LLMInterface()

    print("\n" + "="*40)
    print("   Edge LLM Hardware Controller v1.0   ")
    print("="*40)
    print("Commands: 'red', 'happy', 'beep', etc.")
    print("Exit: 'quit' or 'q'")

    while True:
        try:
            user_input = input("\nUser > ")
            if user_input.lower() in ['exit', 'quit', 'q']:
                break

            if not user_input.strip():
                continue

            print("Thinking...")
            response = llm.query(user_input)

            if response and "action" in response:
                action = response["action"]
                params = response.get("params", {})
                explanation = response.get("explanation", "No explanation.")

                print(f"\n[LLM Decision] {explanation}")

                if action == "set_led":
                    color = params.get("color", [0, 0, 0])
                    brightness = params.get("brightness", 1.0)
                    hw.set_led(color=tuple(color), brightness=brightness)
                elif action == "beep":
                    duration = params.get("duration", 0.1)
                    hw.beep(duration=duration)
                else:
                    print(f"Unknown action: {action}")
            else:
                print("Error: Could not parse intent or invalid command.")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    hw.turn_off()
    print("\nSystem Halted. Goodbye!")

if __name__ == "__main__":
    main()
