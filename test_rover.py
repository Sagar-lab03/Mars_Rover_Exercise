"""
Unit tests for Mars Rover Simulation - Phase 1
Run with: pytest test_rover.py -v
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rover import (
    North, East, South, West,
    Grid, Rover,
    MoveForward, TurnLeft, TurnRight
)


class TestDirections:
    """Test direction classes."""
    
    def test_north_movement(self):
        """Test North direction moves correctly."""
        north = North()
        x, y = north.move_forward(5, 5)
        assert (x, y) == (5, 6)
    
    def test_east_movement(self):
        """Test East direction moves correctly."""
        east = East()
        x, y = east.move_forward(5, 5)
        assert (x, y) == (6, 5)
    
    def test_south_movement(self):
        """Test South direction moves correctly."""
        south = South()
        x, y = south.move_forward(5, 5)
        assert (x, y) == (5, 4)
    
    def test_west_movement(self):
        """Test West direction moves correctly."""
        west = West()
        x, y = west.move_forward(5, 5)
        assert (x, y) == (4, 5)
    
    def test_turn_left_from_north(self):
        """Test turning left from North goes to West."""
        north = North()
        new_dir = north.turn_left()
        assert isinstance(new_dir, West)
    
    def test_turn_right_from_north(self):
        """Test turning right from North goes to East."""
        north = North()
        new_dir = north.turn_right()
        assert isinstance(new_dir, East)
    
    def test_full_rotation_left(self):
        """Test full 360-degree rotation left."""
        direction = North()
        direction = direction.turn_left()  # West
        direction = direction.turn_left()  # South
        direction = direction.turn_left()  # East
        direction = direction.turn_left()  # North
        assert isinstance(direction, North)
    
    def test_full_rotation_right(self):
        """Test full 360-degree rotation right."""
        direction = North()
        direction = direction.turn_right()  # East
        direction = direction.turn_right()  # South
        direction = direction.turn_right()  # West
        direction = direction.turn_right()  # North
        assert isinstance(direction, North)


class TestGrid:
    """Test grid functionality."""
    
    def test_grid_creation(self):
        """Test grid is created with correct dimensions."""
        grid = Grid(10, 10)
        assert grid.width == 10
        assert grid.height == 10
    
    def test_obstacle_detection(self):
        """Test obstacle detection works."""
        grid = Grid(10, 10, obstacles=[(2, 2), (5, 5)])
        assert grid.has_obstacle(2, 2) is True
        assert grid.has_obstacle(5, 5) is True
        assert grid.has_obstacle(3, 3) is False
    
    def test_valid_position(self):
        """Test position validation."""
        grid = Grid(10, 10)
        assert grid.is_valid_position(5, 5) is True
        assert grid.is_valid_position(0, 0) is True
        assert grid.is_valid_position(9, 9) is True
        assert grid.is_valid_position(-1, 5) is False
        assert grid.is_valid_position(5, -1) is False
        assert grid.is_valid_position(10, 5) is False
        assert grid.is_valid_position(5, 10) is False


class TestRover:
    """Test rover functionality."""
    
    def test_rover_initialization(self):
        """Test rover is initialized correctly."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        assert rover.x == 5
        assert rover.y == 5
        assert isinstance(rover.direction, North)
    
    def test_rover_move_forward_success(self):
        """Test rover moves forward successfully."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        result = rover.move_forward()
        assert result is True
        assert rover.x == 5
        assert rover.y == 6
    
    def test_rover_blocked_by_obstacle(self):
        """Test rover is blocked by obstacles."""
        grid = Grid(10, 10, obstacles=[(5, 6)])
        rover = Rover(5, 5, North(), grid)
        result = rover.move_forward()
        assert result is False
        assert rover.x == 5
        assert rover.y == 5  # Should not move
    
    def test_rover_blocked_by_boundary(self):
        """Test rover is blocked by grid boundaries."""
        grid = Grid(10, 10)
        rover = Rover(0, 0, South(), grid)
        result = rover.move_forward()
        assert result is False
        assert rover.x == 0
        assert rover.y == 0  # Should not move
    
    def test_rover_turn_left(self):
        """Test rover turns left correctly."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        rover.turn_left()
        assert isinstance(rover.direction, West)
    
    def test_rover_turn_right(self):
        """Test rover turns right correctly."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        rover.turn_right()
        assert isinstance(rover.direction, East)
    
    def test_rover_path_tracking(self):
        """Test rover tracks its path."""
        grid = Grid(10, 10)
        rover = Rover(0, 0, North(), grid)
        rover.move_forward()
        rover.turn_right()
        rover.move_forward()
        assert len(rover.path_history) == 3
        assert (0, 0) in rover.path_history
        assert (0, 1) in rover.path_history
        assert (1, 1) in rover.path_history
    
    def test_rover_command_counting(self):
        """Test rover counts commands correctly."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        rover.move_forward()
        rover.turn_left()
        rover.turn_right()
        assert rover.command_count == 3


class TestCommands:
    """Test command pattern implementation."""
    
    def test_move_forward_command(self):
        """Test MoveForward command."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        cmd = MoveForward()
        cmd.execute(rover)
        assert rover.y == 6
    
    def test_turn_left_command(self):
        """Test TurnLeft command."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        cmd = TurnLeft()
        cmd.execute(rover)
        assert isinstance(rover.direction, West)
    
    def test_turn_right_command(self):
        """Test TurnRight command."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        cmd = TurnRight()
        cmd.execute(rover)
        assert isinstance(rover.direction, East)


class TestIntegration:
    """Integration tests for complete scenarios."""
    
    def test_square_path(self):
        """Test rover can complete a square path."""
        grid = Grid(10, 10)
        rover = Rover(5, 5, North(), grid)
        
        # Move in a square: North, East, South, West
        rover.move_forward()  # (5, 6)
        rover.turn_right()
        rover.move_forward()  # (6, 6)
        rover.turn_right()
        rover.move_forward()  # (6, 5)
        rover.turn_right()
        rover.move_forward()  # (5, 5)
        
        assert rover.x == 5
        assert rover.y == 5
        assert isinstance(rover.direction, West)
    
    def test_obstacle_navigation(self):
        """Test rover navigates around obstacles."""
        grid = Grid(10, 10, obstacles=[(5, 6)])
        rover = Rover(5, 5, North(), grid)
        
        # Try to move forward (blocked by obstacle at 5,6)
        rover.move_forward()
        assert rover.y == 5  # Blocked, still at (5, 5)
        
        # Go around the obstacle
        rover.turn_right()    # Now facing East
        rover.move_forward()  # Move to (6, 5)
        rover.turn_left()     # Now facing North
        rover.move_forward()  # Move to (6, 6)
        rover.turn_left()     # Now facing West
        rover.move_forward()  # Try to move to (5, 6) - blocked by obstacle!
        
        # Should still be at (6, 6) facing West (couldn't move to obstacle)
        assert rover.x == 6
        assert rover.y == 6
        assert isinstance(rover.direction, West)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
