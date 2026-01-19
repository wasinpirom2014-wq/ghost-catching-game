#!/usr/bin/env python3
"""
Ghost Catching Game - Enhanced Version
A turn-based puzzle game where players place talismans to catch ghosts
Version 2.0 with improved UI, animations, and features
"""

import pygame
import sys
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set
import random
import math

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
COLOR_UI_BG = (40, 40, 60)
COLOR_BUTTON = (100, 150, 200)
COLOR_BUTTON_HOVER = (120, 170, 220)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    LEVEL_FAILED = 4
    GAME_OVER = 5
    PAUSE = 6

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
        self.animation_progress = 0.0
        self.prev_pos = start_pos
    
    def reset(self):
        self.pos = self.start_pos
        self.prev_pos = self.start_pos
        self.animation_progress = 0.0
    
    def get_valid_moves(self, grid: 'GameGrid') -> List[Position]:
        """Get all valid adjacent positions the ghost can move to"""
        valid_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = self.pos.x + dx
            new_y = self.pos.y + dy
            
            if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:
                new_pos = Position(new_x, new_y)
                if grid.get_cell(new_pos) not in [CellType.TALISMAN, CellType.OBSTACLE]:
                    valid_moves.append(new_pos)
        
        return valid_moves
    
    def move_ai(self, grid: 'GameGrid', pot_positions: List[Position]):
        """AI logic: Ghost tries to escape from pots and reach the edge"""
        valid_moves = self.get_valid_moves(grid)
        
        if not valid_moves:
            return
        
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            min_pot_distance = min([move.distance_to(pot) for pot in pot_positions])
            center = Position(GRID_COLS // 2, GRID_ROWS // 2)
            distance_from_center = move.distance_to(center)
            distance_from_edge = min(
                move.x,
                move.y,
                GRID_COLS - 1 - move.x,
                GRID_ROWS - 1 - move.y
            )
            
            score = (
                min_pot_distance * 2 +
                distance_from_edge * -1
            )
            
            if score > best_score:
                best_score = score
                best_move = move
        
        if best_move:
            self.prev_pos = self.pos
            self.pos = best_move
            self.animation_progress = 0.0

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
        self.grid.reset()
        self.obstacles.clear()
        self.pots.clear()
        
        if self.level_num <= 20:
            num_pots = max(3, 5 - (self.level_num // 5))
            num_obstacles = 8 - (self.level_num // 3)
            self.max_talismans = 20 + (self.level_num * 2)
        elif self.level_num <= 60:
            num_pots = max(2, 4 - ((self.level_num - 20) // 10))
            num_obstacles = 5 - ((self.level_num - 20) // 15)
            self.max_talismans = 25 + ((self.level_num - 20) * 1.5)
        else:
            num_pots = 1
            num_obstacles = 2 - ((self.level_num - 60) // 20)
            self.max_talismans = 30 + ((self.level_num - 60) * 1.2)
        
        for _ in range(num_pots):
            while True:
                x = random.randint(0, GRID_COLS - 1)
                y = random.randint(0, GRID_ROWS - 1)
                pos = Position(x, y)
                if pos not in self.pots:
                    self.pots.append(pos)
                    self.grid.set_cell(pos, CellType.POT)
                    break
        
        for _ in range(num_obstacles):
            while True:
                x = random.randint(1, GRID_COLS - 2)
                y = random.randint(1, GRID_ROWS - 2)
                pos = Position(x, y)
                if pos not in self.obstacles and pos not in self.pots:
                    self.obstacles.append(pos)
                    self.grid.set_cell(pos, CellType.OBSTACLE)
                    break
        
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
        self.total_score = 0
        self.best_times = {}
        
        self.load_level(self.current_level)
    
    def load_level(self, level_num: int):
        """Load a specific level"""
        if level_num > self.total_levels:
            self.state = GameState.GAME_OVER
            return
        
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
                    if self.current_level < self.total_levels:
                        self.load_level(self.current_level + 1)
                    else:
                        self.state = GameState.GAME_OVER
                elif self.state == GameState.LEVEL_FAILED:
                    self.load_level(self.current_level)
                elif self.state == GameState.MENU:
                    self.load_level(1)
                elif self.state == GameState.GAME_OVER:
                    self.state = GameState.MENU
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                if event.key == pygame.K_r:
                    self.load_level(self.current_level)
                if event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSE
                    elif self.state == GameState.PAUSE:
                        self.state = GameState.PLAYING
        
        return True
    
    def handle_game_click(self, pos: Tuple[int, int]):
        """Handle click on game grid"""
        mouse_x, mouse_y = pos
        
        grid_x = mouse_x // GRID_SIZE
        grid_y = (mouse_y - 50) // GRID_SIZE
        
        if not (0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS):
            return
        
        click_pos = Position(grid_x, grid_y)
        
        if self.level.grid.is_valid_placement(click_pos):
            self.level.grid.set_cell(click_pos, CellType.TALISMAN)
            self.level.talisman_count += 1
            
            self.level.ghost.move_ai(self.level.grid, self.level.pots)
            
            self.check_game_state()
    
    def check_game_state(self):
        """Check if level is won or lost"""
        ghost_pos = self.level.ghost.pos
        
        if ghost_pos in self.level.pots:
            self.state = GameState.LEVEL_COMPLETE
            self.total_score += max(0, self.level.max_talismans - self.level.talisman_count)
            return
        
        if (ghost_pos.x < 0 or ghost_pos.x >= GRID_COLS or
            ghost_pos.y < 0 or ghost_pos.y >= GRID_ROWS):
            self.state = GameState.LEVEL_FAILED
            return
        
        if self.level.talisman_count >= self.level.max_talismans:
            self.state = GameState.LEVEL_FAILED
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(COLOR_BG)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSE:
            self.draw_game()
            self.draw_pause()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
        elif self.state == GameState.LEVEL_FAILED:
            self.draw_level_failed()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw main menu"""
        # Draw title
        title = self.font_large.render("Ghost Catching Game", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.font_medium.render("Turn-Based Puzzle Game", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw instructions
        instr1 = self.font_small.render("Place talismans to catch the ghost", True, COLOR_TEXT)
        instr1_rect = instr1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instr1, instr1_rect)
        
        instr2 = self.font_small.render("Guide it into the sacred pot", True, COLOR_TEXT)
        instr2_rect = instr2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(instr2, instr2_rect)
        
        # Draw start button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50)
        pygame.draw.rect(self.screen, COLOR_BUTTON, button_rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, button_rect, 2)
        
        start_text = self.font_medium.render("START", True, COLOR_TEXT)
        start_rect = start_text.get_rect(center=button_rect.center)
        self.screen.blit(start_text, start_rect)
    
    def draw_game(self):
        """Draw game screen"""
        # Draw UI bar
        pygame.draw.rect(self.screen, COLOR_UI_BG, (0, 0, SCREEN_WIDTH, 50))
        
        ui_text = self.font_small.render(
            f"Level: {self.current_level}/99 | Talismans: {self.level.talisman_count}/{self.level.max_talismans} | Score: {self.total_score}",
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
                    pygame.draw.rect(self.screen, COLOR_TEXT, rect, 1)
                elif cell == CellType.OBSTACLE:
                    pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
                elif cell == CellType.POT:
                    pygame.draw.circle(self.screen, COLOR_POT, rect.center, GRID_SIZE // 3)
                    pygame.draw.circle(self.screen, COLOR_TEXT, rect.center, GRID_SIZE // 3, 1)
                elif pos == self.level.ghost.pos:
                    pygame.draw.circle(self.screen, COLOR_GHOST, rect.center, GRID_SIZE // 3)
                    pygame.draw.circle(self.screen, COLOR_TEXT, rect.center, GRID_SIZE // 3, 1)
    
    def draw_pause(self):
        """Draw pause overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("PAUSED", True, COLOR_TEXT)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        resume_text = self.font_small.render("Press P to resume", True, COLOR_TEXT)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_level_complete(self):
        """Draw level complete screen"""
        self.draw_game()
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("Level Complete!", True, COLOR_SUCCESS)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text, text_rect)
        
        score_text = self.font_medium.render(f"Score: +{max(0, self.level.max_talismans - self.level.talisman_count)}", True, COLOR_SUCCESS)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        if self.current_level < self.total_levels:
            next_text = self.font_small.render("Click to continue to next level...", True, COLOR_TEXT)
        else:
            next_text = self.font_small.render("All levels complete! Click to restart...", True, COLOR_SUCCESS)
        
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(next_text, next_rect)
    
    def draw_level_failed(self):
        """Draw level failed screen"""
        self.draw_game()
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("Ghost Escaped!", True, COLOR_FAILURE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        retry_text = self.font_small.render("Click to retry... (R to reset, ESC for menu)", True, COLOR_TEXT)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(retry_text, retry_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        title = self.font_large.render("Game Complete!", True, COLOR_SUCCESS)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        
        score_text = self.font_medium.render(f"Final Score: {self.total_score}", True, COLOR_SUCCESS)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        congrats_text = self.font_small.render("Congratulations! You caught all 99 ghosts!", True, COLOR_TEXT)
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(congrats_text, congrats_rect)
        
        restart_text = self.font_small.render("Click to return to menu", True, COLOR_TEXT)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
        self.screen.blit(restart_text, restart_rect)
    
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
