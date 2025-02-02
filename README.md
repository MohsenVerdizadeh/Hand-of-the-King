# 🏆 Hand of the King AI 🤖

## 📌 Overview
My AI course's final project implements an AI agent for the **Hand of the King** board game using **Minimax with Alpha-Beta Pruning** and an **adaptive depth**. A **Genetic Algorithm** is also used to optimize heuristic weights for better decision-making.

## ✨ Features
✅ **AI Agent:** Implements Minimax with Alpha-Beta Pruning for optimal move selection.  
✅ **Adaptive Depth:** Dynamically adjusts search depth based on game complexity.  
✅ **Genetic Algorithm:** Optimizes heuristic weights for better AI performance.  
✅ **Threading Support:** Uses Python's `ThreadPoolExecutor` for efficient parallel execution.  
✅ **Companion Card Strategy:** AI intelligently selects and uses companion cards.  
✅ **File I/O:** Reads, updates, and writes JSON-formatted game states.  

## 🚀 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/MohsenVerdizadeh/Hand-of-the-King.git
   cd Hand-of-the-King
   ```
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Run
Run the main game file with:
```bash
python main.py
```
To use the AI agent:
```bash
python main.py --player1 ai --player2 human
```

## 📂 File Structure
```
📁 Hand-of-the-King/
├── 🏠 main.py              # Main game script
├── 🤖 eslash_agent.py      # AI agent with Minimax & trained with genetic algorithm
├── 🤖 opponent.py          # AI agent with Minimax & opponent agent for eslash_agent training
├── 🤖 random_agent.py      # AI agent with random move 
├── 🧬 train.py             # Training file with Genetic Algorithm for optimizing heuristics
├── 🏠 train_main.py        # Main game script for training
├── 📜 requirements.txt     # Project documentation
├── 📜 README.md            # Project documentation
```

## 🧠 How the AI Works
1️⃣ **Minimax with Alpha-Beta Pruning** evaluates possible moves and selects the best one.  
2️⃣ **Adaptive Depth Control** adjusts search depth based on the number of valid moves.  
3️⃣ **Heuristic Functions** evaluate game states based on card control, banners, and strategic positioning.  
4️⃣ **Genetic Algorithm** fine-tunes heuristic weights to improve AI decision-making over multiple iterations.  

## 🤝 Contributions
Feel free to contribute! Open an issue or submit a pull request.  

## 📜 License
This project is licensed under the **MIT License**.  

## 📬 Contact
For any questions, contact 📧 Mohsenverdizadehkohi@gmail.com.

