# 🚀 Mars Rover Simulation - Phase 1

## Overview
A Python-based Mars Rover simulation that demonstrates object-oriented programming, design patterns, and software engineering best practices. This project simulates a rover navigating a grid-based Mars surface while avoiding obstacles.

## ✨ Phase 1 Features

### 1. **Type Hints & Documentation**
- Comprehensive type hints for all functions and methods
- Detailed docstrings following Python best practices
- Clear, maintainable code structure

### 2. **Rich Terminal UI**
- Beautiful colored terminal output using the `rich` library
- Real-time grid visualization showing:
  - Rover position with directional arrows (↑ → ↓ ←)
  - Obstacles marked in red
  - Path history shown as dots
  - Grid coordinates for easy navigation

### 3. **Configuration System**
- YAML-based configuration file (`config.yaml`)
- Easy customization without code changes:
  - Grid dimensions
  - Obstacle positions
  - Rover starting position and direction
  - Mission settings

### 4. **Telemetry Logging**
- Automatic mission data logging to JSON files
- Tracks:
  - All commands executed
  - Rover position history
  - Mission start/end times
  - Final statistics
- Saved in `telemetry/` folder for analysis

### 5. **Unit Testing**
- Comprehensive test suite using `pytest`
- Tests cover:
  - Direction logic
  - Grid functionality
  - Rover movement and turning
  - Command execution
  - Integration scenarios
- Easy to run: `pytest test_rover.py -v`

## 🏗️ Architecture & Design Patterns

### **Strategy Pattern**
The direction system uses the Strategy pattern, where each cardinal direction (North, East, South, West) is a separate class implementing the `Direction` interface. This makes it easy to add new behaviors without modifying existing code.

### **Command Pattern**
Commands (Move, Turn Left, Turn Right) are implemented as objects that can be executed on the rover. This allows for:
- Easy addition of new commands
- Command history tracking
- Potential undo/redo functionality (future enhancement)

### **Object-Oriented Design**
- Clear separation of concerns
- Abstract base classes for extensibility
- Encapsulation of rover state and grid logic

## 📁 Project Structure

```
Mars_Rover_Exercise/
├── rover.py             # Main application
├── config.yaml          # Mission configuration
├── test_rover.py        # Unit tests
├── requirements.txt     # Python dependencies
├── README_Phase1.md     # This file
└── telemetry/          # Mission logs (auto-created)
    └── mission_*.json
```

## 🚀 Getting Started

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Simulation

1. **Run the program:**
```bash
python rover.py
```

2. **Control the rover:**
   - `M` - Move forward
   - `L` - Turn left
   - `R` - Turn right
   - `Q` - Quit and show summary

3. **Customize your mission:**
   - Edit `config.yaml` to change grid size, obstacles, or starting position

### Running Tests

```bash
pytest test_rover.py -v
```

## 📊 Example Output

```
═══ MARS SURFACE GRID ═══

 9 │ · · · · · · · · · ·
 8 │ · · · · · · · ■ · ·
 7 │ · · · · · · · · · ·
 6 │ · · · · · · · · · ·
 5 │ · · · ■ · · · · · ·
 4 │ · · · · · · · · · ·
 3 │ · · · · · · · · · ·
 2 │ · · ■ · · · · · · ·
 1 │ · · · · · · · · · ·
 0 │ ↑ · · · · · · · · ·
   └────────────────────
     0 1 2 3 4 5 6 7 8 9

Legend: ↑→↓← Rover | ■ Obstacle | · Path
```

## 🎯 Key Learnings

### Technical Skills Demonstrated:
- **Python Best Practices**: Type hints, docstrings, PEP 8 compliance
- **Design Patterns**: Strategy and Command patterns
- **Testing**: Unit testing with pytest
- **Configuration Management**: YAML-based config
- **Data Logging**: JSON telemetry for analysis
- **User Experience**: Rich terminal UI for better visualization

### Software Engineering Principles:
- **SOLID Principles**: Single responsibility, Open/closed principle
- **Clean Code**: Readable, maintainable, well-documented
- **Separation of Concerns**: Clear module boundaries
- **Testability**: Comprehensive test coverage

## 🔮 What's Next?

**Phase 2** will include:
- A* pathfinding algorithm for autonomous navigation
- Battery/energy system with solar charging
- Mission objectives and waypoints
- Terrain types affecting movement
- Web-based visualization

## 🤝 Connect With Me

I'm passionate about combining **Astronomy** and **AI/ML** technologies. This project showcases my interest in space exploration and software engineering.

If you're working on similar projects or interested in collaboration, let's connect!

---

## 📝 Technical Notes

### Dependencies
- **rich**: Terminal formatting and visualization
- **pyyaml**: Configuration file parsing
- **pytest**: Testing framework

### Python Version
- Requires Python 3.7+

### License
Educational project - feel free to learn from and adapt!

---

*Phase 1 - Core Optimizations Complete ✅*
