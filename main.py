#!/usr/bin/env python3
"""
Ghost Catching Game - Main Game Engine
A turn-based puzzle game where players place talismans to catch ghosts
"""

import pygame
import sys
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
GRID_SIZE = 40
GRID_COLS = SCREEN_WIDTH // GRID_SIZE
GRID_ROWS = (SCREEN_HEIGHT - 100) // GRID_SIZE
FPS = 60

# Colors
COLOR_BG = (20, 20, 30)
COLOR_GRID = (50, 50, 70)
COLOR_EMPTY = (30, 30, 45)
COLOR_GHOST = (100, 200, 255)
COLOR_TALISMAN = (255, 200, 50)
COLOR_POT = (200, 100, 50)
COLOR_OBSTACLE = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_SUCCESS = (100, 255, 100)
COLOR_FAILURE = (255, 100, 100)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    LEVEL_FAILED = 4
    GAME_OVER = 5

class CellType(Enum):
    EMPTY = 0
    TALISMAN = 1
    OBSTACLE = 2
    POT = 3
    GHOST = 4

@dataclass
class Position:
    x: int
    y: int
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def distance_to(self, other: 'Position') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

class Ghost:
    def __init__(self, start_pos: Position):
        self.pos = start_pos
        self.start_pos = start_pos
    
    def reset(self):
        self.pos = self.start_pos
    
    def get_valid_moves(self, grid: 'GameGrid') -> List[Position]:
        """Get all valid adjacent positions the ghost can move to"""
        valid_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = self.pos.x + dx
            new_y = self.pos.y + dy
            
            # Check bounds
            if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:
                new_pos = Position(new_x, new_y)
                # Check if cell is not blocked
                if grid.get_cell(new_pos) not in [CellType.TALISMAN, CellType.OBSTACLE]:
                    valid_moves.append(new_pos)
        
        return valid_moves
    
    def move_ai(self, grid: 'GameGrid', pot_positions: List[Position]):
        """AI logic: Ghost tries to escape from pots and reach the edge"""
        valid_moves = self.get_valid_moves(grid)
        
        if not valid_moves:
            return  # Ghost is trapped (shouldn't happen in normal gameplay)
        
        # Calculate score for each move
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            # Score 1: Distance from pots (want to maximize)
            min_pot_distance = min([move.distance_to(pot) for pot in pot_positions])
            
            # Score 2: Distance from center (want to maximize to reach edge)
            center = Position(GRID_COLS // 2, GRID_ROWS // 2)
            distance_from_center = move.distance_to(center)
            
            # Score 3: Distance from edges (want to minimize to escape)
            distance_from_edge = min(
                move.x,
                move.y,
                GRID_COLS - 1 - move.x,
                GRID_ROWS - 1 - move.y
            )
            
            # Combined score
            score = (
                min_pot_distance * 2 +  # Avoid pots
                distance_from_edge * -1  # Move towards edge
            )
            
            if score > best_score:
                best_score = score
                best_move = move
        
        if best_move:
            self.pos = best_move

class GameGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]
    
    def set_cell(self, pos: Position, cell_type: CellType):
        if 0 <= pos.y < self.height and 0 <= pos.x < self.width:
            self.grid[pos.y][pos.x] = cell_type
    
    def get_cell(self, pos: Position) -> CellType:
        if 0 <= pos.y < self.height and 0 <= pos.x < self.width:
            return self.grid[pos.y][pos.x]
        return CellType.EMPTY
    
    def reset(self):
        self.grid = [[CellType.EMPTY for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_placement(self, pos: Position) -> bool:
        """Check if a talisman can be placed at this position"""
        if not (0 <= pos.x < self.width and 0 <= pos.y < self.height):
            return False
        return self.get_cell(pos) == CellType.EMPTY

class Level:
    def __init__(self, level_num: int):
        self.level_num = level_num
        self.grid = GameGrid(GRID_COLS, GRID_ROWS)
        self.ghost = None
        self.pots: List[Position] = []
        self.obstacles: List[Position] = []
        self.talisman_count = 0
        self.max_talismans = 0
        self.generate_level()
    
    def generate_level(self):
        """Generate level based on difficulty"""
        # Clear grid
        self.grid.reset()
        self.obstacles.clear()
        self.pots.clear()
        
        # Difficulty progression
        if self.level_num <= 20:  # Easy
            num_pots = max(3, 5 - (self.level_num // 5))
            num_obstacles = 8 - (self.level_num // 3)
            self.max_talismans = 20 + (self.level_num * 2)
        elif self.level_num <= 60:  # Medium
            num_pots = max(2, 4 - ((self.level_num - 20) // 10))
            num_obstacles = 5 - ((self.level_num - 20) // 15)
            self.max_talismans = 25 + ((self.level_num - 20) * 1.5)
        else:  # Hard
            num_pots = 1
            num_obstacles = 2 - ((self.level_num - 60) // 20)
            self.max_talismans = 30 + ((self.level_num - 60) * 1.2)
        
        # Place pots
        for _ in range(num_pots):
            while True:
                x = random.randint(0, GRID_COLS - 1)
                y = random.randint(0, GRID_ROWS - 1)
                pos = Position(x, y)
                if pos not in self.pots:
                    self.pots.append(pos)
                    self.grid.set_cell(pos, CellType.POT)
                    break
        
        # Place obstacles
        for _ in range(num_obstacles):
            while True:
                x = random.randint(1, GRID_COLS - 2)
                y = random.randint(1, GRID_ROWS - 2)
                pos = Position(x, y)
                if pos not in self.obstacles and pos not in self.pots:
                    self.obstacles.append(pos)
                    self.grid.set_cell(pos, CellType.OBSTACLE)
                    break
        
        # Place ghost at a random position away from pots
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)
            ghost_pos = Position(x, y)
            if ghost_pos not in self.pots and ghost_pos not in self.obstacles:
                self.ghost = Ghost(ghost_pos)
                self.grid.set_cell(ghost_pos, CellType.GHOST)
                break
        
        self.talisman_count = 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ghost Catching Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = GameState.MENU
        self.current_level = 1
        self.level = None
        self.total_levels = 99
        
        self.load_level(self.current_level)
    
    def load_level(self, level_num: int):
        """Load a specific level"""
        self.current_level = level_num
        self.level = Level(level_num)
        self.state = GameState.PLAYING
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.PLAYING:
                    self.handle_game_click(event.pos)
                elif self.state == GameState.LEVEL_COMPLETE:
                    self.load_level(self.current_level + 1)
                elif self.state == GameState.LEVEL_FAILED:
                    self.load_level(self.current_level)
                elif self.state == GameState.MENU:
                    self.load_level(1)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                if event.key == pygame.K_r:
                    self.load_level(self.current_level)
        
        return True
    
    def handle_game_click(self, pos: Tuple[int, int]):
        """Handle click on game grid"""
        mouse_x, mouse_y = pos
        
        # Convert pixel position to grid position
        grid_x = mouse_x // GRID_SIZE
        grid_y = (mouse_y - 50) // GRID_SIZE  # Offset for UI
        
        # Check bounds
        if not (0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS):
            return
        
        click_pos = Position(grid_x, grid_y)
        
        # Try to place talisman
        if self.level.grid.is_valid_placement(click_pos):
            self.level.grid.set_cell(click_pos, CellType.TALISMAN)
            self.level.talisman_count += 1
            
            # Ghost moves after talisman placement
            self.level.ghost.move_ai(self.level.grid, self.level.pots)
            
            # Check win/lose conditions
            self.check_game_state()
    
    def check_game_state(self):
        """Check if level is won or lost"""
        ghost_pos = self.level.ghost.pos
        
        # Check if ghost is in a pot (win)
        if ghost_pos in self.level.pots:
            self.state = GameState.LEVEL_COMPLETE
            return
        
        # Check if ghost escaped (lose)
        if (ghost_pos.x < 0 or ghost_pos.x >= GRID_COLS or
            ghost_pos.y < 0 or ghost_pos.y >= GRID_ROWS):
            self.state = GameState.LEVEL_FAILED
            return
        
        # Check if talisman limit exceeded
        if self.level.talisman_count >= self.level.max_talismans:
            self.state = GameState.LEVEL_FAILED
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(COLOR_BG)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.state == GameState.LEVEL_FAILED:
            self.draw_level_failed()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw main menu"""
        title = self.font_large.render("Ghost Catching Game", True, COLOR_TEXT)
        subtitle = self.font_medium.render("Click to Start", True, COLOR_TEXT)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
    
    def draw_game(self):
        """Draw game screen"""
        # Draw UI bar
        ui_text = self.font_small.render(
            f"Level: {self.current_level}/99 | Talismans: {self.level.talisman_count}/{self.level.max_talismans}",
            True,
            COLOR_TEXT
        )
        self.screen.blit(ui_text, (10, 10))
        
        # Draw grid
        grid_start_y = 50
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                rect = pygame.Rect(x * GRID_SIZE, grid_start_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)
                
                pos = Position(x, y)
                cell = self.level.grid.get_cell(pos)
                
                if cell == CellType.TALISMAN:
                    pygame.draw.rect(self.screen, COLOR_TALISMAN, rect)
                elif cell == CellType.OBSTACLE:
                    pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
                elif cell == CellType.POT:
                    pygame.draw.circle(self.screen, COLOR_POT, rect.center, GRID_SIZE // 3)
                elif pos == self.level.ghost.pos:
                    pygame.draw.circle(self.screen, COLOR_GHOST, rect.center, GRID_SIZE // 3)
    
    def draw_level_complete(self):
        """Draw level complete screen"""
        self.draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Text
        text = self.font_large.render("Level Complete!", True, COLOR_SUCCESS)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        if self.current_level < self.total_levels:
            next_text = self.font_small.render("Click to continue...", True, COLOR_TEXT)
        else:
            next_text = self.font_small.render("Game Complete! Click to restart...", True, COLOR_SUCCESS)
        
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(next_text, next_rect)
    
    def draw_level_failed(self):
        """Draw level failed screen"""
        self.draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Text
        text = self.font_large.render("Ghost Escaped!", True, COLOR_FAILURE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        retry_text = self.font_small.render("Click to retry... (R to reset)", True, COLOR_TEXT)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(retry_text, retry_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
