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
- **Benchmarking Suite**: Specialized `benchmark.py` to evaluate performance, accuracy, and resource usage.

### Benchmarking (Evaluation)
The benchmarking suite evaluates:
- **TTFT (Time To First Token)**: Prompt processing latency.
- **Throughput**: Generation speed (Tokens Per Second).
- **Resource Usage**: RAM utilization and CPU Thermal range.
- **Accuracy**: Capability to map various commands to valid hardware actions.

To run the benchmark:
1. Ensure `llama-server` is running.
2. Run the script:
   ```bash
   python3 ~/edgeLLM/benchmark.py
   ```
   *Note: Results will be saved to `benchmark_log.json`.*

### Breadboard Wiring Diagram
| Component | Device Pin | Pi GPIO | Physical Pin | Resistor |
| :--- | :--- | :--- | :--- | :--- |
| **RGB LED** | Red (Anode/Cathode) | GPIO 17 | Pin 11 | 220Ω |
| **RGB LED** | Green (Anode/Cathode) | GPIO 27 | Pin 13 | 220Ω |
| **RGB LED** | Blue (Anode/Cathode) | GPIO 22 | Pin 15 | 220Ω |
| **RGB LED** | Common | GND | Pin 6/9 | None |
| **Buzzer** | Positive (+) | GPIO 23 | Pin 16 | None |
| **Buzzer** | Negative (-) | GND | Pin 14/20 | None |

### Usage
1. **Verify Wiring**: `python3 ~/edgeLLM/test_hardware.py`
2. **Start LLM Server**:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
3. **Run Controller**: `python3 ~/edgeLLM/main.py`

---

<a name="chinese"></a>
## 中文

### 项目简介
基于树莓派 5 的中间件，可通过本地大语言模型 (**Qwen2.5-0.5B-Instruct**) 实现对物理硬件（RGB LED、蜂鸣器）的自然语言控制。

### 功能特性
- **本地推理**: 使用 `llama.cpp` 和 `llama-server` 完全在设备端运行。
- **自然语言意图解析**: 将人类指令映射为结构化的 JSON 动作。
- **硬件控制**: 通过 `gpiozero` 直接进行 GPIO 交互。
- **调试工具**: 包含 `test_hardware.py` 脚本，用于验证面包板线路连接。
- **基准测试**: 提供 `benchmark.py` 脚本，用于评估性能、准确率和资源占用。

### 基准测试 (性能评估)
测试指标包括:
- **TTFT (首字延迟)**: Prompt 处理延迟。
- **吞吐量**: 生成速度 (每秒 Token 数)。
- **资源占用**: RAM 使用情况及 CPU 温度范围。
- **准确率**: 将各种指令转换为有效硬件动作的能力。

运行测试:
1. 确保 `llama-server` 已启动。
2. 运行脚本:
   ```bash
   python3 ~/edgeLLM/benchmark.py
   ```
   *注: 测试结果将保存至 `benchmark_log.json`。*

### 面包板接线图
| 元件 | 引脚类型 | 树莓派 GPIO | 物理引脚 | 电阻 |
| :--- | :--- | :--- | :--- | :--- |
| **RGB LED** | 红灯 (R) | GPIO 17 | Pin 11 | 220Ω |
| **RGB LED** | 绿灯 (G) | GPIO 27 | Pin 13 | 220Ω |
| **RGB LED** | 蓝灯 (B) | GPIO 22 | Pin 15 | 220Ω |
| **RGB LED** | 公共端 | GND | Pin 6/9 | 无 |
| **蜂鸣器** | 正极 (+) | GPIO 23 | Pin 16 | 无 |
| **蜂鸣器** | 负极 (-) | GND | Pin 14/20 | 无 |

### 使用方法
1. **验证线路**: `python3 ~/edgeLLM/test_hardware.py`
2. **启动 LLM 服务器**:
   ```bash
   ~/llama.cpp/build/bin/llama-server -m ~/llama.cpp/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080 &
   ```
3. **运行控制器**: `python3 ~/edgeLLM/main.py`
