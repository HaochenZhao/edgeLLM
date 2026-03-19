# Edge LLM Hardware Controller / 边缘大模型硬件控制器

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### Project Overview
A Raspberry Pi 5 based middleware that enables natural language control of physical hardware (RGB LED, Buzzer) using a local Large Language Model (**Qwen2.5-0.5B-Instruct**).

### Features
- **Local Inference**: Runs entirely on-device using `llama.cpp` and `llama-server`.
- **Natural Language Intent**: Maps human commands (e.g., "Make the light red") to structured JSON actions.
- **Hardware Control**: Direct GPIO interaction via `gpiozero`.
- **Debugging Tool**: Includes `test_hardware.py` to verify your breadboard connections.

### Breadboard Wiring Diagram
| Component | Device Pin | Pi GPIO | Physical Pin | Resistor |
| :--- | :--- | :--- | :--- | :--- |
| **RGB LED** | Red (Anode/Cathode) | GPIO 17 | Pin 11 | 220Ω |
| **RGB LED** | Green (Anode/Cathode) | GPIO 27 | Pin 13 | 220Ω |
| **RGB LED** | Blue (Anode/Cathode) | GPIO 22 | Pin 15 | 220Ω |
| **RGB LED** | Common | GND | Pin 6/9 | None |
| **Buzzer** | Positive (+) | GPIO 23 | Pin 16 | None |
| **Buzzer** | Negative (-) | GND | Pin 14/20 | None |

> [!NOTE]
> For common cathode RGB LEDs, connect the common pin to GND. For common anode, connect it to 3.3V and ensure `active_high=False` in the code.

### Usage
1. **Verify Wiring**:
   ```bash
   python3 ~/edgeLLM/test_hardware.py
   ```
2. **Start LLM Server**:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
3. **Run Controller**:
   ```bash
   python3 ~/edgeLLM/main.py
   ```

---

<a name="chinese"></a>
## 中文

### 项目简介
基于树莓派 5 的中间件，可通过本地大语言模型 (**Qwen2.5-0.5B-Instruct**) 实现对物理硬件（RGB LED、蜂鸣器）的自然语言控制。

### 功能特性
- **本地推理**: 使用 `llama.cpp` 和 `llama-server` 完全在设备端运行。
- **自然语言意图解析**: 将人类指令（例如“把灯调成红色”）映射为结构化的 JSON 动作。
- **硬件控制**: 通过 `gpiozero` 直接进行 GPIO 交互。
- **调试工具**: 包含 `test_hardware.py` 脚本，用于验证面包板线路连接。

### 面包板接线图
| 元件 | 引脚类型 | 树莓派 GPIO | 物理引脚 | 电阻 |
| :--- | :--- | :--- | :--- | :--- |
| **RGB LED** | 红灯 (R) | GPIO 17 | Pin 11 | 220Ω |
| **RGB LED** | 绿灯 (G) | GPIO 27 | Pin 13 | 220Ω |
| **RGB LED** | 蓝灯 (B) | GPIO 22 | Pin 15 | 220Ω |
| **RGB LED** | 公共端 | GND | Pin 6/9 | 无 |
| **蜂鸣器** | 正极 (+) | GPIO 23 | Pin 16 | 无 |
| **蜂鸣器** | 负极 (-) | GND | Pin 14/20 | 无 |

> [!TIP]
> 如果您使用的是共阴极 LED，请将公共端接 GND；如果是共阳极，请接 3.3V，并在代码中确认 `active_high=False`。

### 使用方法
1. **验证线路**:
   ```bash
   python3 ~/edgeLLM/test_hardware.py
   ```
2. **启动 LLM 服务器**:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
3. **运行控制器**:
   ```bash
   python3 ~/edgeLLM/main.py
   ```
