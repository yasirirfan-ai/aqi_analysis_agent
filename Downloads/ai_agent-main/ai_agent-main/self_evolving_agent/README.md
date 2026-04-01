
<!-- Project Logo -->
<div align="center">
  <a href="https://github.com/Hazyasir3/ai_agent">
    <img src="./assets/EAXLoGo.svg" alt="Self-Evolving Workflow Agent" width="50%">
  </a>
</div>

<h2 align="center">
  Building a Self-Evolving Ecosystem of AI Agents
</h2>

<div align="center">

[![Author](https://img.shields.io/badge/Author-Hazyasir3-blue.svg)](https://github.com/Hazyasir3)
[![Docs](https://img.shields.io/badge/-Documentation-0A66C2?logo=readthedocs&logoColor=white&color=7289DA&labelColor=grey)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Hazyasir3/ai_agent?style=social)](https://github.com/Hazyasir3/ai_agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Hazyasir3/ai_agent?style=social)](https://github.com/Hazyasir3/ai_agent/fork)

</div>

<h4 align="center">
  <i>An automated framework for generating, evaluating, and evolving agentic workflows.</i>
</h4>

<p align="center">
  <img src="./assets/framework_en.jpg">
</p>

---

## 🔥 Latest News
- **[2025]** 🎉 Self-Evolving Workflow Agent added to the `ai_agent` repository

---

## ⚡ Get Started
- [Installation](#installation)
- [LLM Configuration](#llm-configuration)
- [Automatic Workflow Generation](#automatic-workflow-generation)
- [Demo](#demo)
- [Evolution Algorithms](#evolution-algorithms)
- [Applications](#applications)
- [Tutorials & Use Cases](#tutorials--use-cases)
- [Roadmap](#-roadmap)
- [Support](#-support)
- [Contributing](#-contributing)
- [License](#-license)

---

## Installation

Install dependencies locally:

```bash
git clone https://github.com/Hazyasir3/ai_agent.git
cd ai_agent/self_evolving_workflow_agent
pip install -r requirements.txt
````

Optional: create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## LLM Configuration

### API Key Configuration

#### Option 1: Environment Variable

**Linux / macOS**

```bash
export OPENAI_API_KEY=your_openai_api_key
```

**Windows PowerShell**

```powershell
setx OPENAI_API_KEY "your_openai_api_key"
```

#### Option 2: `.env` File

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

Load it in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

## Configure and Use the LLM

```python
import os
from evoagentx.models import OpenAILLMConfig, OpenAILLM

config = OpenAILLMConfig(
    model="gpt-4o-mini",
    openai_key=os.getenv("OPENAI_API_KEY"),
    stream=True,
    output_response=True
)

llm = OpenAILLM(config=config)
response = llm.generate("Explain agentic workflows")
```

---

## Automatic Workflow Generation

### Core Steps

1. Define a natural language goal
2. Auto-generate workflow
3. Spawn agents
4. Execute workflow

### Minimal Example

```python
from evoagentx.workflow import WorkFlowGenerator, WorkFlow
from evoagentx.agents import AgentManager

goal = "Generate HTML code for a Tetris game"

workflow_graph = WorkFlowGenerator(llm=llm).generate_workflow(goal)

agent_manager = AgentManager()
agent_manager.add_agents_from_workflow(workflow_graph, llm_config=config)

workflow = WorkFlow(
    graph=workflow_graph,
    agent_manager=agent_manager,
    llm=llm
)

result = workflow.execute()
print(result)
```

---

## Demo

🎥 Demo showcases:

* Automatic workflow generation
* Multi-agent execution
* Self-evolving optimization

Assets available in `/assets`.

---

## Evolution Algorithms

Integrated optimization strategies include:

* **TextGrad**
* **AFlow**
* **MIPRO**

Benchmarks tested on:

* HotPotQA
* MBPP
* MATH

| Method   | HotPotQA | MBPP | MATH |
| -------- | -------- | ---- | ---- |
| Original | 63.5     | 69.0 | 66.0 |
| TextGrad | 71.0     | 71.0 | 76.0 |
| AFlow    | 65.0     | 79.0 | 71.0 |
| MIPRO    | 69.1     | 68.0 | 72.3 |

---

## Applications

Optimized multi-agent systems for:

* Deep Research Agents
* Code Generation Agents
* Financial & Reasoning Agents

GAIA-style benchmark improvements demonstrated.

---

## Tutorials & Use Cases

* Build Your First Agent
* Build Multi-Agent Workflow
* Workflow Auto-Generation
* Benchmarking & Evaluation
* Prompt & Structure Optimization

---

## 🎯 Roadmap

* [ ] Plug-and-play evolution algorithms
* [ ] Visual workflow editor
* [ ] Agent memory optimization
* [ ] Multi-objective evolution
* [ ] Persistent workflow storage

---

## 🙋 Support

For questions or feedback:

* GitHub Issues
* Discussions tab

---

## 🙌 Contributing

Contributions are welcome.
Please follow repository contribution guidelines.

---

## 📄 License

This project is licensed under the **MIT License**.

Maintained and adapted for the **ai_agent** repository by **Hazyasir3**
