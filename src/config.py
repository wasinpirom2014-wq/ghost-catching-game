"""
Game Configuration
Central place for all game settings and constants
"""

# Screen Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
GRID_SIZE = 40
GRID_COLS = SCREEN_WIDTH // GRID_SIZE  # 20
GRID_ROWS = (SCREEN_HEIGHT - 100) // GRID_SIZE  # 22
FPS = 60

# Game Configuration
TOTAL_LEVELS = 99
GAME_VERSION = "1.0.0"
GAME_NAME = "Ghost Catching Game"

# Color Palette
COLORS = {
    'bg': (20, 20, 30),
    'grid': (50, 50, 70),
    'empty': (30, 30, 45),
    'ghost': (100, 200, 255),
    'talisman': (255, 200, 50),
    'pot': (200, 100, 50),
    'obstacle': (100, 100, 100),
    'text': (255, 255, 255),
    'success': (100, 255, 100),
    'failure': (255, 100, 100),
    'ui_bg': (40, 40, 60),
    'ui_text': (200, 200, 220),
}

# Level Configuration
LEVEL_CONFIG = {
    'easy': {
        'range': (1, 20),
        'min_pots': 3,
        'max_pots': 5,
        'min_obstacles': 5,
        'max_obstacles': 8,
        'base_talismans': 20,
        'talisman_per_level': 2,
    },
    'medium': {
        'range': (21, 60),
        'min_pots': 2,
        'max_pots': 4,
        'min_obstacles': 2,
        'max_obstacles': 5,
        'base_talismans': 25,
        'talisman_per_level': 1.5,
    },
    'hard': {
        'range': (61, 99),
        'min_pots': 1,
        'max_pots': 1,
        'min_obstacles': 0,
        'max_obstacles': 2,
        'base_talismans': 30,
        'talisman_per_level': 1.2,
    },
}

# AdMob Configuration
ADMOB_CONFIG = {
    'enabled': True,
    'test_mode': False,  # Set to True for testing
    'interstitial_ad_unit_id': 'ca-app-pub-xxxxxxxxxxxxxxxx/yyyyyyyyyyyyyy',
    'rewarded_ad_unit_id': 'ca-app-pub-xxxxxxxxxxxxxxxx/zzzzzzzzzzzzzz',
    'show_interstitial_after_level': True,
    'show_rewarded_on_failure': True,
    'rewarded_undo_moves': 3,
    'rewarded_skip_after_failures': 3,
}

# Audio Configuration
AUDIO_CONFIG = {
    'enabled': True,
    'music_volume': 0.7,
    'sfx_volume': 0.8,
    'background_music': 'assets/audio/background.mp3',
    'sound_effects': {
        'talisman_place': 'assets/audio/talisman.wav',
        'ghost_move': 'assets/audio/ghost_move.wav',
        'level_complete': 'assets/audio/level_complete.wav',
        'level_failed': 'assets/audio/level_failed.wav',
        'ui_click': 'assets/audio/ui_click.wav',
    }
}

# UI Configuration
UI_CONFIG = {
    'button_width': 200,
    'button_height': 50,
    'button_color': (100, 150, 200),
    'button_hover_color': (120, 170, 220),
    'button_text_color': (255, 255, 255),
    'font_size_large': 48,
    'font_size_medium': 36,
    'font_size_small': 24,
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'enabled': True,
    'track_level_completion': True,
    'track_ads_shown': True,
    'track_game_duration': True,
    'track_device_info': True,
}

# Difficulty Multipliers
DIFFICULTY_MULTIPLIERS = {
    1: 1.0,
    2: 1.1,
    3: 1.2,
    4: 1.3,
    5: 1.4,
}

# Ghost AI Configuration
GHOST_AI_CONFIG = {
    'pot_avoidance_weight': 2.0,
    'edge_attraction_weight': 1.0,
    'obstacle_awareness': True,
    'pathfinding_depth': 3,
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_vsync': True,
    'max_fps': 60,
    'enable_particle_effects': True,
    'enable_animations': True,
    'cache_level_data': True,
}

# Debug Configuration
DEBUG_CONFIG = {
    'enabled': False,
    'show_grid_numbers': False,
    'show_ghost_ai_debug': False,
    'show_fps': False,
    'show_memory_usage': False,
}

# Localization
LOCALES = {
    'en': 'English',
    'th': 'Thai',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese',
    'zh': 'Chinese',
}

DEFAULT_LOCALE = 'en'

# Strings (English)
STRINGS_EN = {
    'title': 'Ghost Catching Game',
    'level': 'Level',
    'talismans': 'Talismans',
    'level_complete': 'Level Complete!',
    'ghost_escaped': 'Ghost Escaped!',
    'click_to_continue': 'Click to continue...',
    'click_to_retry': 'Click to retry...',
    'game_complete': 'Game Complete!',
    'click_to_restart': 'Click to restart...',
    'start': 'Start Game',
    'menu': 'Menu',
    'settings': 'Settings',
    'about': 'About',
    'quit': 'Quit',
}

# Strings (Thai)
STRINGS_TH = {
    'title': 'เกมจับวิญญาณ',
    'level': 'ด่าน',
    'talismans': 'ยันต์',
    'level_complete': 'ผ่านด่านแล้ว!',
    'ghost_escaped': 'วิญญาณหนีไปแล้ว!',
    'click_to_continue': 'คลิกเพื่อดำเนินการต่อ...',
    'click_to_retry': 'คลิกเพื่อลองใหม่...',
    'game_complete': 'เล่นจบแล้ว!',
    'click_to_restart': 'คลิกเพื่อเริ่มใหม่...',
    'start': 'เริ่มเล่น',
    'menu': 'เมนู',
    'settings': 'ตั้งค่า',
    'about': 'เกี่ยวกับ',
    'quit': 'ออก',
}

def get_strings(locale=DEFAULT_LOCALE):
    """Get localized strings"""
    if locale == 'th':
        return STRINGS_TH
    return STRINGS_EN

def get_level_config(level_num):
    """Get configuration for a specific level"""
    for difficulty, config in LEVEL_CONFIG.items():
        if config['range'][0] <= level_num <= config['range'][1]:
            return config
    return LEVEL_CONFIG['hard']

def get_max_talismans(level_num):
    """Calculate maximum talismans allowed for a level"""
    config = get_level_config(level_num)
    offset = level_num - config['range'][0]
    return int(config['base_talismans'] + (offset * config['talisman_per_level']))
