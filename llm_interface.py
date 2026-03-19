import urllib.request
import json
import re

class LLMInterface:
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

    def query(self, user_input):
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
                result = json.loads(response.read().decode('utf-8'))
                content = result.get('content', '')
                return self._parse_json(content)
        except Exception as e:
            print(f"Error calling LLM Server: {e}")
            return None

    def _parse_json(self, text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                # Basic cleanup in case of extra trailings
                if json_str.count('{') == json_str.count('}'):
                    return json.loads(json_str)
                else:
                    # Try to find the first complete object
                    open_count = 0
                    for i, char in enumerate(json_str):
                        if char == '{': open_count += 1
                        elif char == '}': open_count -= 1
                        if open_count == 0:
                            return json.loads(json_str[:i+1])
            except Exception:
                return None
        return None

if __name__ == "__main__":
    llm = LLMInterface()
    for cmd in ["red", "beep"]:
        resp = llm.query(cmd)
        print(f"Input: {cmd} -> Response: {resp}")
