# Demo script to test the rover without manual input
# This simulates a simple mission

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from rover import Grid, Rover, North, MoveForward, TurnRight, TurnLeft, GridVisualizer
from rich.console import Console

console = Console()

def demo():
    """Run a simple automated demo."""
    console.print("\n[bold cyan]=== AUTOMATED DEMO ===[/bold cyan]\n")
    
    # Create grid with obstacles
    grid = Grid(10, 10, obstacles=[(2, 2), (3, 5), (7, 8)])
    
    # Create rover
    rover = Rover(0, 0, North(), grid)
    
    console.print("[yellow]Initial State:[/yellow]")
    GridVisualizer.display_grid(rover)
    
    # Execute commands
    commands = [
        ("Move Forward", MoveForward()),
        ("Move Forward", MoveForward()),
        ("Turn Right", TurnRight()),
        ("Move Forward", MoveForward()),
        ("Move Forward", MoveForward()),
        ("Turn Left", TurnLeft()),
        ("Move Forward", MoveForward()),
    ]
    
    for desc, cmd in commands:
        console.print(f"\n[cyan]Executing: {desc}[/cyan]")
        cmd.execute(rover)
        GridVisualizer.display_grid(rover)
    
    # Final status
    status = rover.get_status()
    console.print(f"\n[bold green]Demo Complete![/bold green]")
    console.print(f"Final Position: ({status['position']['x']}, {status['position']['y']})")
    console.print(f"Final Direction: {status['direction']}")
    console.print(f"Commands Executed: {status['commands_executed']}")
    console.print(f"Cells Visited: {status['cells_visited']}\n")

if __name__ == "__main__":
    demo()
