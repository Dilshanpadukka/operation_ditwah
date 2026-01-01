# Operation Ditwah – Crisis Intelligence Pipeline

**Scenario:** Post-Cyclone Ditwah Relief (Sri Lanka) – December 2025

---

## 📋 Project Overview

This project implements a **Crisis Intelligence Pipeline** designed to assist the **Disaster Management Center (DMC)** during a fictional cyclone crisis.

The system:

* Filters noise from social media
* Validates genuine rescue requests
* Optimizes logistics for limited resources
* Converts unstructured news feeds into actionable databases

The pipeline handles **five core tasks**:

* **Reliability (The Contract):** Distinguishes real SOS calls from news noise using *Few-Shot Prompting*.
* **Safety (Stability Experiment):** Tests system stability against hallucinations by varying model temperature (*Safe Mode vs. Chaos Mode*).
* **Strategic Planning (Logistics Commander):** Plans complex logistics for limited resources using *Chain of Thought (CoT)* and *Tree of Thoughts (ToT)* reasoning.
* **Efficiency (Budget Keeper):** Rejects or summarizes token-heavy spam to save API costs.
* **Scalability (News Feed Pipeline):** Processes a live news feed into a structured Excel database using *Pydantic* and *Pandas*.

---

## 🛠️ Prerequisites

* Python **3.8+**
* **Groq API Key** (Required for Llama 3 model integration)

---

## 📦 Installation & Setup

### Project Setup

Ensure your project folder follows the structure defined below.

### Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the root directory and add your Groq API key:

```ini
GROQ_API_KEY=gsk_your_api_key_here
```

---

## 📂 Project Structure

```plaintext
operation_ditwah/
│
├── data/                       # Input datasets
│   ├── sample_messages.txt     # Mixed SOS / News messages
│   ├── incidents.txt           # Critical incidents for logistics
│   ├── scenarios.txt           # Complex scenarios for stress testing
│   └── news_feed.txt           # Raw news ticker feed
│
├── output/                     # Generated results
│   ├── classified_messages.xlsx # Output from Part 1
│   └── flood_report.xlsx        # Output from Part 5
│
├── src/                        # Source code
│   ├── classifier.py     # Few-Shot Learning Classifier
│   ├── stability.py      # Temperature / Hallucination Test
│   ├── logistics.py      # CoT & ToT Logic Planner
│   ├── budget.py         # Token Limiter & Summarizer
│   └── newsfeed.py       # JSON Extraction Pipeline
│
├── utils/
│   └── token_utils.py          # Helper for counting tokens
│
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Usage Guide

### Part 1: The "Contract" (Classifier)

Classifies incoming messages into **Rescue**, **Supply**, **Info**, or **Other** categories.

```bash
python src/classifier.py
```

* **Goal:** Engineer a reliable classification prompt using few-shot examples
* **Output:** `output/classified_messages.xlsx`

---

### Part 2: The Stability Experiment

Runs a stress test on the AI model by comparing:

* **Safe Mode:** Temperature = 0.0
* **Chaos Mode:** Temperature = 1.0

```bash
python src/stability.py
```

* **Goal:** Observe how high temperature causes the model to drift or hallucinate resources

---

### Part 3: The Logistics Commander

Uses **Chain of Thought (CoT)** to score incident urgency and **Tree of Thoughts (ToT)** to determine the optimal rescue route for a single boat.

```bash
python src/logistics.py
```

* **Goal:** Maximize total priority score saved within the shortest time

---

### Part 4: The "Budget Keeper"

Implements token economics. Messages exceeding **150 tokens** are flagged and summarized before processing.

```bash
python src/budget.py
```

* **Goal:** Print `BLOCKED` / `TRUNCATED` for spam inputs

---

### Part 5: The "News Feed" Pipeline

Converts the unstructured `news_feed.txt` into a structured Excel database using **Pydantic** for strict schema validation.

```bash
python src/newsfeed.py
```

* **Extracted Fields:**

  * `district`
  * `flood_level_meters`
  * `victim_count`
  * `main_need`
  * `status`

* **Output:** `output/flood_report.xlsx`

---
