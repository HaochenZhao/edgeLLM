import time
import json
import urllib.request
import psutil
import os
import re
import subprocess

class EdgeLLMBenchmark:
    def __init__(self, api_url="http://localhost:8080/completion"):
        self.api_url = api_url
        self.system_prompt = (
            "You are a hardware controller for a Raspberry Pi. "
            "You control an RGB LED and a buzzer. "
            "Respond ONLY with a JSON object. "
            "Actions: 'set_led' (color [r,g,b], brightness 0-1), 'beep' (duration in seconds). "
            "Examples:\n"
            'User: "Turn red"\n'
            'Assistant: {"action": "set_led", "params": {"color": [1,0,0], "brightness": 1.0}, "explanation": "Setting LED to red."}\n'
            'User: "Beep"\n'
            'Assistant: {"action": "beep", "params": {"duration": 0.2}, "explanation": "Beeping buzzer."}'
        )
        self.test_commands = [
            # Lighting Commands
            "Turn on the living room light", "Dim the bedroom lights to 50%", "Make the kitchen light red",
            "Set the hallway light to blue", "Turn off all lights in the house", "Set the study light to bright white",
            "Change the lounge light to a warm orange", "Make the nursery light a soft pink", "Increase the bathroom light brightness",
            "Set the dining room to a romantic purple", "Make the garage light green", "Turn the porch light on",
            "Set the balcony light to a cool cyan", "Make the basement light yellow", "Turn off the kitchen lights",
            "Set the intensity of the living room lamp to low", "Make the bedroom light dark blue", "Switch the attic light to green",
            "Set the entrance light to maximum brightness", "Turn on the stairs light",
            
            # Security & Alert Commands (Beep)
            "Sound the security alarm", "Someone is at the front door, chime please", "Alert: smoke detected in the kitchen",
            "Set a timer for 5 minutes and beep when done", "Activate the panic button", "Sound the siren for a second",
            "High priority alert: water leak in basement", "Low battery warning beep", "Double beep for confirmation",
            "System arming notification sound", "Doorbell ringing", "Emergency broadcast signal",
            "Wake up alarm for 7 AM (beep)", "Reminder to take medicine (chirp)", "Intruder detected in the garden!",
            
            # Scenario & Mood Commands
            "Party mode: set lights to colorful and beep once", "Movie time: dim the lights to 10%", "Good morning: turn on the lights moderately",
            "Good night: turn off all hardware", "Gaming mode: set lights to neon blue", "Relaxing session: soft green light",
            "Reading mode: neutral white light", "Romantic dinner: dim red lighting", "Study time: focused bright light",
            "Christmas theme: alternate red and green light", "Ocean vibes: set light to deep sea blue",
            "Fireplace simulation: orange and red flickering lights", "Forest escape: deep forest green", "Flash the lights for an incoming call",
            "Signal a SOS using red lights and short beeps"
        ]
        self.results = []

    def get_system_metrics(self):
        # CPU Temperature
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read()) / 1000.0
        except:
            temp = None

        # Throttling status
        try:
            throttled = subprocess.check_output(["vcgencmd", "get_throttled"]).decode().strip()
        except:
            throttled = "N/A"

        # RAM usage
        ram = psutil.virtual_memory().percent
        
        return {"temp": temp, "throttled": throttled, "ram_percent": ram}

    def get_accuracy_metrics(self, command, intent):
        if not intent:
            return False, "Invalid JSON"
        
        action = intent.get("action")
        params = intent.get("params", {})
        
        # 1. Legality Check
        is_legal = True
        legality_msg = "OK"
        if action == "set_led":
            color = params.get("color")
            brightness = params.get("brightness")
            if not isinstance(color, list) or len(color) != 3:
                is_legal = False; legality_msg = "Invalid color format"
            elif not all(0 <= c <= 1 for c in color):
                is_legal = False; legality_msg = "Color values out of range"
            elif not isinstance(brightness, (int, float)) or not (0 <= brightness <= 1):
                is_legal = False; legality_msg = "Invalid brightness"
        elif action == "beep":
            duration = params.get("duration")
            if not isinstance(duration, (int, float)) or duration <= 0:
                is_legal = False; legality_msg = "Invalid duration"
        else:
            is_legal = False; legality_msg = f"Unknown action: {action}"

        # 2. Semantic Accuracy (Keyword based Ground Truth)
        is_accurate = False
        cmd_lower = command.lower()
        if action == "set_led":
            # Keyword matching for LEDs
            if any(k in cmd_lower for k in ["light", "dim", "red", "green", "blue", "orange", "pink", "purple", "cyan", "yellow", "white", "off", "night", "morning", "party", "movie", "gaming", "relaxing", "reading", "study", "christmas", "ocean", "fire", "forest", "flash", "sos"]):
                is_accurate = True
        elif action == "beep":
            # Keyword matching for Beeps
            if any(k in cmd_lower for k in ["beep", "buzz", "alarm", "chime", "siren", "doorbell", "timer", "panic", "warning", "notification", "signal", "sos", "intruder", "smoke", "leak"]):
                is_accurate = True
        
        return is_legal and is_accurate, f"Legal: {legality_msg} | Accurate: {is_accurate}"

    def query_llm(self, user_input):
        prompt = f"<|im_start|>system\n{self.system_prompt}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        data = json.dumps({
            "prompt": prompt,
            "n_predict": 128,
            "temperature": 0.0,
            "stop": ["<|im_end|>", "User:"]
        }).encode('utf-8')

        req = urllib.request.Request(self.api_url, data=data, method='POST', 
                                  headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error calling LLM Server: {e}")
            return None

    def parse_intent(self, text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return None
        return None

    def run(self):
        print(f"--- Starting Edge LLM Benchmark ({len(self.test_commands)} samples) ---")
        accuracy_count = 0
        total_samples = len(self.test_commands)

        for i, cmd in enumerate(self.test_commands, 1):
            print(f"[{i}/{total_samples}] Command: {cmd}")
            
            m_before = self.get_system_metrics()
            t_start = time.time()
            
            resp = self.query_llm(cmd)
            
            t_end = time.time()
            m_after = self.get_system_metrics()
            
            if resp:
                content = resp.get("content", "")
                intent = self.parse_intent(content)
                timings = resp.get("timings", {})
                
                is_valid, validation_msg = self.get_accuracy_metrics(cmd, intent)
                if is_valid:
                    accuracy_count += 1
                
                res = {
                    "index": i,
                    "command": cmd,
                    "intent": intent,
                    "latency_total": t_end - t_start,
                    "prompt_ms": timings.get("prompt_ms"),
                    "predicted_per_second": timings.get("predicted_per_second"),
                    "temp_range": (m_before["temp"], m_after["temp"]),
                    "ram_peak": max(m_before["ram_percent"], m_after["ram_percent"]),
                    "throttled": m_after["throttled"],
                    "accuracy_check": validation_msg,
                    "passed": is_valid
                }
                self.results.append(res)
                print(f"  Latency: {res['latency_total']:.2f}s | Valid: {'YES' if is_valid else 'NO'} | Info: {validation_msg}")
            else:
                print(f"  FAILED to get response for: {cmd}")

        avg_acc = (accuracy_count / total_samples) * 100
        print(f"\n--- Benchmark Summary ---")
        print(f"Overall Accuracy: {avg_acc:.2f}%")
        self.save()

    def save(self):
        with open("benchmark_log.json", "w") as f:
            json.dump(self.results, f, indent=4)
        print("\nBenchmark complete. Results saved to benchmark_log.json")

if __name__ == "__main__":
    bench = EdgeLLMBenchmark()
    bench.run() # User said do not run yet
    print("Benchmark tool initialized. Ready to execute.")
