# 🚀 Quick Start Guide - Phase 1

## Installation & First Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Tests (Optional but Recommended)
```bash
pytest test_rover.py -v
```
You should see: **24 passed** ✅

### Step 3: Run the Simulation
```bash
python rover.py
```

### Step 4: Try These Commands
When the program starts, try this sequence:
1. Press `M` (Move forward)
2. Press `M` (Move forward again)
3. Press `R` (Turn right)
4. Press `M` (Move forward)
5. Press `Q` (Quit and see summary)

You'll see the grid update after each command showing your rover's position!

## Customizing Your Mission

Edit `config.yaml` to change:
- Grid size (default: 10x10)
- Obstacle positions
- Rover starting position
- Mission name

## What You'll See

- **Beautiful grid visualization** with your rover shown as directional arrows (↑ → ↓ ←)
- **Obstacles** shown in red (■)
- **Path history** shown as dots (·)
- **Mission summary** at the end with statistics
- **Telemetry files** saved in the `telemetry/` folder

## Tips

- The rover won't move into obstacles or outside the grid
- You'll get a warning if you try to move into an obstacle
- Your path is tracked and shown on the grid
- All mission data is logged to JSON for later analysis

Enjoy exploring Mars! 🌟
