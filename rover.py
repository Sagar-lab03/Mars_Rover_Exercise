"""
Mars Rover Simulation - Phase 1
A command-line simulation of a Mars rover navigating a grid with obstacles.

Features:
- Object-oriented design with Strategy and Command patterns
- Rich terminal visualization
- Configuration file support
- Telemetry logging
- Type hints and comprehensive documentation
"""

import logging
import json
import yaml
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Dict, Type
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rich console for beautiful output
console = Console()


# # # ----- DIRECTION CLASSES ----- # # #

class Direction(ABC):
    """Abstract base class for cardinal directions."""
    
    @abstractmethod
    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        """Calculate new position when moving forward.
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
            
        Returns:
            Tuple of new (x, y) coordinates
        """
        pass

    @abstractmethod
    def turn_left(self) -> 'Direction':
        """Return the direction after turning left."""
        pass

    @abstractmethod
    def turn_right(self) -> 'Direction':
        """Return the direction after turning right."""
        pass


class North(Direction):
    """North direction - moving forward increases Y."""
    
    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        return x, y + 1

    def turn_left(self) -> Direction:
        return West()

    def turn_right(self) -> Direction:
        return East()
    
    def __str__(self) -> str:
        return "North"


class East(Direction):
    """East direction - moving forward increases X."""
    
    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        return x + 1, y

    def turn_left(self) -> Direction:
        return North()

    def turn_right(self) -> Direction:
        return South()
    
    def __str__(self) -> str:
        return "East"


class South(Direction):
    """South direction - moving forward decreases Y."""
    
    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        return x, y - 1

    def turn_left(self) -> Direction:
        return East()

    def turn_right(self) -> Direction:
        return West()
    
    def __str__(self) -> str:
        return "South"


class West(Direction):
    """West direction - moving forward decreases X."""
    
    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        return x - 1, y

    def turn_left(self) -> Direction:
        return South()

    def turn_right(self) -> Direction:
        return North()
    
    def __str__(self) -> str:
        return "West"


# # # ----- COMMAND CLASSES ----- # # # 

class Command(ABC):
    """Abstract base class for rover commands."""
    
    @abstractmethod
    def execute(self, rover: 'Rover') -> None:
        """Execute the command on the rover.
        
        Args:
            rover: The rover to execute the command on
        """
        pass


class MoveForward(Command):
    """Command to move the rover forward one step."""
    
    def execute(self, rover: 'Rover') -> None:
        rover.move_forward()


class TurnLeft(Command):
    """Command to turn the rover 90 degrees left."""
    
    def execute(self, rover: 'Rover') -> None:
        rover.turn_left()


class TurnRight(Command):
    """Command to turn the rover 90 degrees right."""
    
    def execute(self, rover: 'Rover') -> None:
        rover.turn_right()


# # # ----- GRID AND ROVER CLASSES ----- # # #

class Grid:
    """Represents the Mars surface grid with obstacles."""
    
    def __init__(self, width: int, height: int, obstacles: List[Tuple[int, int]] = None):
        """Initialize the grid.
        
        Args:
            width: Grid width
            height: Grid height
            obstacles: List of (x, y) coordinates with obstacles
        """
        self.width = width
        self.height = height
        self.obstacles = obstacles or []

    def has_obstacle(self, x: int, y: int) -> bool:
        """Check if there's an obstacle at the given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if obstacle exists, False otherwise
        """
        return (x, y) in self.obstacles
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height


class Rover:
    """Mars rover that can navigate the grid."""
    
    def __init__(self, x: int, y: int, direction: Direction, grid: Grid):
        """Initialize the rover.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            direction: Starting direction
            grid: The grid the rover operates on
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.grid = grid
        self.path_history: List[Tuple[int, int]] = [(x, y)]
        self.command_count = 0

    def move_forward(self) -> bool:
        """Move the rover forward one step.
        
        Returns:
            True if move was successful, False if blocked
        """
        new_x, new_y = self.direction.move_forward(self.x, self.y)
        
        if not self.grid.is_valid_position(new_x, new_y):
            console.print("[yellow]! Warning: Cannot move - grid boundary![/yellow]")
            return False
            
        if self.grid.has_obstacle(new_x, new_y):
            console.print("[yellow]! Warning: Cannot move - obstacle detected![/yellow]")
            return False
        
        self.x, self.y = new_x, new_y
        self.path_history.append((self.x, self.y))
        self.command_count += 1
        return True

    def turn_left(self) -> None:
        """Turn the rover 90 degrees to the left."""
        self.direction = self.direction.turn_left()
        self.command_count += 1

    def turn_right(self) -> None:
        """Turn the rover 90 degrees to the right."""
        self.direction = self.direction.turn_right()
        self.command_count += 1

    def get_status(self) -> Dict[str, any]:
        """Get current rover status.
        
        Returns:
            Dictionary with rover status information
        """
        return {
            "position": {"x": self.x, "y": self.y},
            "direction": str(self.direction),
            "commands_executed": self.command_count,
            "cells_visited": len(set(self.path_history))
        }

    def report_status(self) -> str:
        """Generate a status report string.
        
        Returns:
            Formatted status string
        """
        return f"Rover is at ({self.x}, {self.y}) facing {self.direction}."


# # # ----- VISUALIZATION ----- # # #

class GridVisualizer:
    """Handles grid visualization in the terminal."""
    
    @staticmethod
    def display_grid(rover: Rover) -> None:
        """Display the grid with rover, obstacles, and path.
        
        Args:
            rover: The rover to display
        """
        grid = rover.grid
        
        # Create visual representation
        console.print("\n[bold cyan]=== MARS SURFACE GRID ===[/bold cyan]\n")
        
        # Direction symbols (ASCII-safe for Windows)
        direction_symbols = {
            "North": "^",
            "East": ">",
            "South": "v",
            "West": "<"
        }
        
        rover_symbol = direction_symbols.get(str(rover.direction), "R")
        
        # Build grid display
        for y in range(grid.height - 1, -1, -1):
            row = []
            for x in range(grid.width):
                if (x, y) == (rover.x, rover.y):
                    row.append(f"[bold green]{rover_symbol}[/bold green]")
                elif (x, y) in grid.obstacles:
                    row.append("[red]X[/red]")
                elif (x, y) in rover.path_history:
                    row.append("[dim cyan].[/dim cyan]")
                else:
                    row.append("[dim].[/dim]")
            
            # Add row with coordinates
            console.print(f"{y:2d} | " + " ".join(row))
        
        # Add x-axis
        console.print("   +" + "-" * (grid.width * 2))
        x_labels = "     " + " ".join(str(x) for x in range(grid.width))
        console.print(x_labels)
        
        # Legend
        console.print("\n[dim]Legend: [bold green]^>v<[/bold green] Rover | [red]X[/red] Obstacle | [cyan].[/cyan] Path[/dim]\n")


# # # ----- TELEMETRY ----- # # #

class TelemetryLogger:
    """Logs mission telemetry data to JSON files."""
    
    def __init__(self, mission_name: str, folder: str = "telemetry"):
        """Initialize telemetry logger.
        
        Args:
            mission_name: Name of the mission
            folder: Folder to store telemetry files
        """
        self.mission_name = mission_name
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)
        self.start_time = datetime.now()
        self.events: List[Dict] = []
    
    def log_event(self, event_type: str, data: Dict) -> None:
        """Log a mission event.
        
        Args:
            event_type: Type of event (e.g., 'command', 'status')
            data: Event data
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        self.events.append(event)
    
    def save(self, rover: Rover) -> str:
        """Save telemetry to file.
        
        Args:
            rover: The rover to save telemetry for
            
        Returns:
            Path to saved telemetry file
        """
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        filename = self.folder / f"mission_{timestamp}.json"
        
        telemetry = {
            "mission_name": self.mission_name,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "final_status": rover.get_status(),
            "path_history": rover.path_history,
            "events": self.events
        }
        
        with open(filename, 'w') as f:
            json.dump(telemetry, f, indent=2)
        
        return str(filename)


# # # ----- CONFIGURATION ----- # # #

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        console.print(f"[yellow]Config file not found. Using defaults.[/yellow]")
        return {
            "grid": {"width": 10, "height": 10, "obstacles": []},
            "rover": {"start_x": 0, "start_y": 0, "start_direction": "N"},
            "mission": {"name": "Mars Mission", "enable_telemetry": True}
        }


# # # ----- USER INTERFACE ---- # # #

def initialize_rover(config: Dict) -> Rover:
    """Initialize rover from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Initialized Rover instance
    """
    grid_config = config.get("grid", {})
    rover_config = config.get("rover", {})
    
    # Create grid
    obstacles = [tuple(obs) for obs in grid_config.get("obstacles", [])]
    grid = Grid(
        width=grid_config.get("width", 10),
        height=grid_config.get("height", 10),
        obstacles=obstacles
    )
    
    # Direction mapping
    direction_map = {
        'N': North(),
        'E': East(),
        'S': South(),
        'W': West()
    }
    
    # Create rover
    x = rover_config.get("start_x", 0)
    y = rover_config.get("start_y", 0)
    direction = direction_map[rover_config.get("start_direction", "N")]
    
    rover = Rover(x, y, direction, grid)
    logging.info(f"Rover initialized at ({x}, {y}) facing {direction}")
    
    return rover


def get_commands() -> List[str]:
    """Get commands from user input.
    
    Returns:
        List of command strings
    """
    command_strs = []
    
    while True:
        try:
            console.print("\n[bold]Available Commands:[/bold]")
            console.print("  [green]M[/green] - Move Forward")
            console.print("  [yellow]L[/yellow] - Turn Left")
            console.print("  [yellow]R[/yellow] - Turn Right")
            console.print("  [red]Q[/red] - Quit and show final status")

            command = console.input("\n[bold cyan]Enter command:[/bold cyan] ").upper()

            if command not in ['M', 'L', 'R', 'Q']:
                raise ValueError("Invalid command entered")

            if command == 'Q':
                break

            command_strs.append(command)
        except ValueError as e:
            logging.error(e)
            console.print("[red]Invalid command. Please try again.[/red]")
    
    return command_strs


def display_mission_summary(rover: Rover, telemetry_path: Optional[str] = None) -> None:
    """Display final mission summary.
    
    Args:
        rover: The rover to summarize
        telemetry_path: Path to telemetry file if saved
    """
    status = rover.get_status()
    
    # Create summary table
    table = Table(title="Mission Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Final Position", f"({status['position']['x']}, {status['position']['y']})")
    table.add_row("Final Direction", status['direction'])
    table.add_row("Commands Executed", str(status['commands_executed']))
    table.add_row("Unique Cells Visited", str(status['cells_visited']))
    
    if telemetry_path:
        table.add_row("Telemetry Saved", telemetry_path)
    
    console.print("\n")
    console.print(table)
    console.print("\n")


# # # ----- MAIN ----- # # #

def main():
    """Main entry point for the Mars Rover simulation."""
    
    # Display welcome banner
    console.print(Panel.fit(
        "MARS ROVER SIMULATION - Phase 1\n"
        "Navigate the Martian surface and avoid obstacles!",
        border_style="cyan"
    ))
    
    # Load configuration
    config = load_config()
    mission_name = config.get("mission", {}).get("name", "Mars Mission")
    enable_telemetry = config.get("mission", {}).get("enable_telemetry", True)
    
    console.print(f"\n[bold]Mission:[/bold] {mission_name}\n")
    
    # Initialize rover
    rover = initialize_rover(config)
    
    # Initialize telemetry
    telemetry = None
    if enable_telemetry:
        telemetry_folder = config.get("mission", {}).get("telemetry_folder", "telemetry")
        telemetry = TelemetryLogger(mission_name, telemetry_folder)
        telemetry.log_event("mission_start", rover.get_status())
    
    # Display initial grid
    GridVisualizer.display_grid(rover)
    
    # Command mapping
    command_map: Dict[str, Type[Command]] = {
        'M': MoveForward,
        'L': TurnLeft,
        'R': TurnRight
    }
    
    # Get and execute commands
    command_strs = get_commands()
    
    for cmd_str in command_strs:
        try:
            command = command_map[cmd_str]
            command().execute(rover)
            
            if telemetry:
                telemetry.log_event("command", {
                    "command": cmd_str,
                    "status": rover.get_status()
                })
            
            logging.info(f"Executed command: {cmd_str}")
            
            # Show updated grid
            GridVisualizer.display_grid(rover)
            
        except Exception as e:
            logging.error(f"Error executing command {cmd_str}: {e}")
    
    # Save telemetry
    telemetry_path = None
    if telemetry:
        telemetry.log_event("mission_end", rover.get_status())
        telemetry_path = telemetry.save(rover)
        console.print(f"[green]Telemetry saved to: {telemetry_path}[/green]")
    
    # Display final summary
    display_mission_summary(rover, telemetry_path)
    
    console.print("[bold green]Mission Complete![/bold green]\n")


if __name__ == "__main__":
    main()
