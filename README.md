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

### Requirements
- Raspberry Pi 5
- RGB LED (Common Cathode/Anode)
- Active Buzzer
- Python 3.11+

### Pin Configuration
- **Red LED**: GPIO 17
- **Green LED**: GPIO 27
- **Blue LED**: GPIO 22
- **Buzzer**: GPIO 23

### How to Run
1. Start the LLM server:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
2. Run the controller:
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

### 硬件要求
- 树莓派 5
- RGB LED (共阴/共阳)
- 有源蜂鸣器
- Python 3.11+

### 引脚配置
- **红灯**: GPIO 17
- **绿灯**: GPIO 27
- **蓝灯**: GPIO 22
- **蜂鸣器**: GPIO 23

### 运行指南
1. 启动 LLM 服务器:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
2. 启动控制器:
   ```bash
   python3 ~/edgeLLM/main.py
   ```
