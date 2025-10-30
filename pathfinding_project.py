# Nama File: diamond_heist_final_v5.0.py
# Proyek 1: "The Diamond Heist: AI vs. Human"
# Versi 5.0: Pixel Art 16x16 + Spawn Kuadran + Peta DENGAN TEMBOK + Validasi Konektivitas

import pygame
import queue
import math
import time
import random
import sys

# --- KONFIGURASI TAMPILAN (PYGAME) ---
WIDTH = 800
ROWS = 40
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Proyek 1 AI: The Diamond Heist (BFS vs A*)")
pygame.font.init()
GAME_FONT = pygame.font.SysFont('Arial', 30, bold=True)
INFO_FONT = pygame.font.SysFont('Arial', 24)

# --- DEFINISI WARNA ---
WARNA_PUTIH = (255, 255, 255)
WARNA_HITAM = (0, 0, 0)
WARNA_BIRU = (0, 100, 255)
WARNA_HIJAU = (0, 200, 0)
WARNA_DIAMOND = (0, 255, 255)
WARNA_ABU_ABU = (128, 128, 128)
WARNA_AI_BFS = (255, 0, 0)
WARNA_AI_ASTAR = (255, 100, 0)
WARNA_KARPET = (139, 69, 19)


def create_sprite(base_surface, scale_size):
    """Helper untuk mengatur transparansi dan menskalakan surface."""
    base_surface.set_colorkey(WARNA_HITAM) # Warna Hitam (0,0,0) akan transparan
    return pygame.transform.scale(base_surface, (scale_size, scale_size))

def create_player_sprite(size):
    """Membuat sprite pixel art 16x16 untuk Pemain dengan detail dan shading."""
    surf = pygame.Surface((16, 16))
    
    # Palet Warna Pemain
    skin = (255, 219, 172)
    skin_shadow = (234, 192, 144)
    hair = (80, 48, 32)
    hair_highlight = (110, 78, 62)
    shirt = (0, 100, 255)
    shirt_shadow = (0, 70, 205)
    pants = (50, 50, 100)
    pants_shadow = (30, 30, 70)
    shoes = (100, 50, 20)
    shoes_highlight = (130, 80, 50)
    
    # Gambar dari belakang ke depan (bayangan dulu)
    # Rambut
    pygame.draw.rect(surf, hair, (4, 2, 8, 5))
    pygame.draw.rect(surf, hair_highlight, (5, 2, 6, 1))
    # Wajah
    pygame.draw.rect(surf, skin_shadow, (4, 5, 8, 3)) # Leher
    pygame.draw.rect(surf, skin, (4, 4, 8, 3))
    # Mata
    pygame.draw.rect(surf, (255, 255, 255), (5, 5, 2, 1)) # Putih mata
    pygame.draw.rect(surf, (255, 255, 255), (9, 5, 2, 1))
    pygame.draw.rect(surf, (0, 0, 0), (6, 5, 1, 1)) # Pupil
    pygame.draw.rect(surf, (0, 0, 0), (9, 5, 1, 1))
    # Baju
    pygame.draw.rect(surf, shirt_shadow, (3, 7, 10, 5))
    pygame.draw.rect(surf, shirt, (4, 7, 8, 4))
    # Lengan
    pygame.draw.rect(surf, skin_shadow, (1, 8, 2, 3))
    pygame.draw.rect(surf, skin, (1, 7, 2, 2))
    pygame.draw.rect(surf, skin_shadow, (13, 8, 2, 3))
    pygame.draw.rect(surf, skin, (13, 7, 2, 2))
    # Celana
    pygame.draw.rect(surf, pants_shadow, (4, 12, 8, 2))
    pygame.draw.rect(surf, pants, (5, 12, 2, 2))
    pygame.draw.rect(surf, pants, (9, 12, 2, 2))
    # Sepatu
    pygame.draw.rect(surf, shoes, (4, 14, 3, 2))
    pygame.draw.rect(surf, shoes, (9, 14, 3, 2))
    pygame.draw.rect(surf, shoes_highlight, (4, 14, 2, 1))
    pygame.draw.rect(surf, shoes_highlight, (9, 14, 2, 1))
    
    return create_sprite(surf, size)

def create_guard_sprite(size, color):
    """Membuat sprite pixel art 16x16 untuk Penjaga dengan detail dan shading."""
    surf = pygame.Surface((16, 16))
    
    # Palet Warna Penjaga
    skin_shadow = (215, 160, 110) # Lebih gelap karena di bawah topi
    uniform = (80, 80, 90)
    uniform_shadow = (60, 60, 70)
    pants = (40, 40, 50)
    pants_shadow = (25, 25, 35)
    shoes = (20, 20, 20)
    badge = (255, 223, 0)
    badge_highlight = (255, 255, 100)
    
    # Topi
    pygame.draw.rect(surf, color, (3, 1, 10, 4))
    pygame.draw.rect(surf, (50, 50, 50), (2, 4, 12, 2)) # Brim
    # Wajah (dalam bayangan topi)
    pygame.draw.rect(surf, skin_shadow, (4, 5, 8, 4))
    # Mata
    pygame.draw.rect(surf, (0, 0, 0), (5, 6, 2, 1))
    pygame.draw.rect(surf, (0, 0, 0), (9, 6, 2, 1))
    # Seragam
    pygame.draw.rect(surf, uniform_shadow, (3, 9, 10, 4))
    pygame.draw.rect(surf, uniform, (4, 9, 8, 3))
    # Lencana
    pygame.draw.rect(surf, badge, (5, 10, 2, 2))
    pygame.draw.rect(surf, badge_highlight, (5, 10, 1, 1))
    # Sabuk
    pygame.draw.line(surf, (30, 30, 30), (3, 12), (12, 12))
    # Celana
    pygame.draw.rect(surf, pants_shadow, (4, 13, 8, 2))
    pygame.draw.rect(surf, pants, (5, 13, 2, 2))
    pygame.draw.rect(surf, pants, (9, 13, 2, 2))
    # Sepatu
    pygame.draw.rect(surf, shoes, (4, 15, 3, 1))
    pygame.draw.rect(surf, shoes, (9, 15, 3, 1))
    
    return create_sprite(surf, size)

def create_diamond_sprite(size):
    """Membuat sprite pixel art 16x16 untuk Berlian dengan segi dan kilau."""
    surf = pygame.Surface((16, 16))
    
    # Palet Warna Berlian
    dark = (0, 150, 170)
    medium = (0, 225, 255)
    light = (150, 255, 255)
    sparkle = (255, 255, 255)

    # Menggambar segi-segi sebagai poligon
    # Bagian bawah
    pygame.draw.polygon(surf, dark, [(8, 14), (2, 7), (14, 7)])
    # Bagian atas
    pygame.draw.polygon(surf, medium, [(8, 2), (2, 7), (14, 7)])
    # Facet tengah
    pygame.draw.polygon(surf, light, [(8, 2), (2, 7), (8, 7)])
    # Garis outline untuk kejelasan
    pygame.draw.line(surf, light, (8, 2), (8, 14), 1)
    pygame.draw.line(surf, light, (2, 7), (14, 7), 1)
    # Kilau
    pygame.draw.rect(surf, sparkle, (4, 5, 2, 2))
    pygame.draw.rect(surf, sparkle, (12, 8, 1, 1))
    
    return create_sprite(surf, size)

def create_exit_sprite(size):
    """Membuat sprite pixel art 16x16 untuk Pintu Keluar dengan shading."""
    surf = pygame.Surface((16, 16))
    
    # Palet Warna Pintu
    frame_dark = (60, 40, 20)
    frame_light = (100, 70, 40)
    door_dark = (0, 150, 0)
    door_light = (0, 200, 0)
    knob = (255, 223, 0)
    knob_highlight = (255, 255, 150)
    
    # Frame Pintu
    pygame.draw.rect(surf, frame_dark, (3, 1, 11, 15))
    pygame.draw.rect(surf, frame_light, (4, 2, 9, 13))
    # Pintu
    pygame.draw.rect(surf, door_dark, (5, 3, 7, 11))
    pygame.draw.rect(surf, door_light, (5, 3, 7, 5)) # Bagian atas lebih terang
    # Gagang Pintu
    pygame.draw.rect(surf, knob, (10, 7, 2, 2))
    pygame.draw.rect(surf, knob_highlight, (10, 7, 1, 1))
    
    return create_sprite(surf, size)
# --- ----------------------------- ---


# --- KELAS UTAMA: Node / Sel ---
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row; self.col = col; self.x = row * width; self.y = col * width
        self.width = width; self.total_rows = total_rows; self.color = WARNA_PUTIH
        self.neighbors = []; self.traversal_cost = 1; self.g = float("inf")
        self.f = float("inf"); self.parent = None
    def get_pos(self): return self.row, self.col
    def is_wall(self): return self.color == WARNA_HITAM
    def reset_path_vars(self): self.g = float("inf"); self.f = float("inf"); self.parent = None
    def make_wall(self): self.color = WARNA_HITAM; self.traversal_cost = float("inf")
    def make_floor(self): self.color = WARNA_PUTIH; self.traversal_cost = 1
    def make_carpet(self): self.color = WARNA_KARPET; self.traversal_cost = 5
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): self.neighbors.append(grid[self.row][self.col - 1])
    def __lt__(self, other): return self.f < other.f

# --- KELAS ENTITAS GAME ---
class Player:
    def __init__(self, row, col, sprite):
        self.row = row; self.col = col; self.sprite = sprite; self.has_diamond = False
    def move(self, dr, dc, grid):
        new_row, new_col = self.row + dr, self.col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            if not grid[new_row][new_col].is_wall():
                self.row = new_row; self.col = new_col; return True
        return False
    def draw(self, win, width): win.blit(self.sprite, (self.row * width, self.col * width))

class Guard:
    def __init__(self, row, col, sprite, algo_type):
        self.row = row; self.col = col; self.sprite = sprite; self.algo_type = algo_type
    def move(self, grid, player_node):
        start_node = grid[self.row][self.col]; end_node = player_node; path = None
        if self.algo_type == 'BFS': path = bfs(grid, start_node, end_node)
        elif self.algo_type == 'A*': path = a_star(grid, start_node, end_node)
        if path and len(path) > 1:
            next_node = path[1]; self.row = next_node.row; self.col = next_node.col
    def draw(self, win, width): win.blit(self.sprite, (self.row * width, self.col * width))

# --- FUNGSI PATHFINDING ---
def h(p1, p2):
    x1, y1 = p1; x2, y2 = p2; return abs(x1 - x2) + abs(y1 - y2)
def reset_pathfinding_vars(grid):
    for row in grid:
        for node in row: node.reset_path_vars()
def reconstruct_path(current_node):
    path = [];
    while current_node: path.append(current_node); current_node = current_node.parent
    return path[::-1]

def bfs(grid, start, end):
    reset_pathfinding_vars(grid); q = queue.Queue(); q.put(start)
    visited = {start}; start.g = 0
    while not q.empty():
        current = q.get()
        if current == end: return reconstruct_path(current)
        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.parent = current; neighbor.g = current.g + 1
                visited.add(neighbor); q.put(neighbor)
    return None

def a_star(grid, start, end):
    reset_pathfinding_vars(grid); count = 0; open_set = queue.PriorityQueue()
    open_set.put((0, count, start)); open_set_hash = {start}
    start.g = 0; start.f = h(start.get_pos(), end.get_pos())
    while not open_set.empty():
        current = open_set.get()[2]; open_set_hash.remove(current)
        if current == end: return reconstruct_path(current)
        for neighbor in current.neighbors:
            temp_g_score = current.g + neighbor.traversal_cost
            if temp_g_score < neighbor.g:
                neighbor.parent = current; neighbor.g = temp_g_score
                neighbor.f = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1; open_set.put((neighbor.f, count, neighbor)); open_set_hash.add(neighbor)
    return None

# --- FUNGSI SETUP & DRAWING GAME ---
def make_grid(rows, width):
    grid = []; gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows); grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows): pygame.draw.line(win, WARNA_ABU_ABU, (0, i * gap), (width, i * gap))
    for j in range(rows): pygame.draw.line(win, WARNA_ABU_ABU, (j * gap, 0), (j * gap, width))

def draw_game(win, grid, rows, width, player, guards, diamond_pos, exit_pos, difficulty, sprites):
    win.fill(WARNA_PUTIH)
    for row in grid:
        for node in row: node.draw(win)
    draw_grid_lines(win, rows, width)
    
    gap = width // rows
    win.blit(sprites["exit"], (exit_pos[0] * gap, exit_pos[1] * gap))
    if not player.has_diamond: win.blit(sprites["diamond"], (diamond_pos[0] * gap, diamond_pos[1] * gap))
    
    player.draw(win, gap)
    for guard in guards: guard.draw(win, gap)
        
    if difficulty == "EASY":
        info_text_bfs = INFO_FONT.render("Merah = BFS (Lambat)", True, WARNA_AI_BFS); win.blit(info_text_bfs, (10, 10))
    else:
        info_text_bfs = INFO_FONT.render("Merah = BFS (Bodoh)", True, WARNA_AI_BFS); win.blit(info_text_bfs, (10, 10))
        if difficulty == "HARD": info_text_astar = INFO_FONT.render("Oranye = A* (SANGAT CEPAT)", True, WARNA_AI_ASTAR)
        else: info_text_astar = INFO_FONT.render("Oranye = A* (Pintar)", True, WARNA_AI_ASTAR)
        win.blit(info_text_astar, (10, 35))
    pygame.display.update()

# --- PETA ACAK (DIKEMBALIKAN DENGAN TEMBOK) ---
def create_random_map_with_walls(grid, safe_zones, difficulty):
    """
    Membuat peta acak 'cluster' DENGAN TEMBOK dan KARPET.
    """
    if difficulty == "EASY":
        NUM_WALL_CLUSTERS = 10; MAX_WALL_LENGTH = 30
        NUM_CARPET_PATCHES = 5; MAX_CARPET_SIZE = 20
        print_msg = "Peta acak 'Mudah' telah dibuat."
    elif difficulty == "HARD":
        NUM_WALL_CLUSTERS = 15; MAX_WALL_LENGTH = 40
        NUM_CARPET_PATCHES = 10; MAX_CARPET_SIZE = 30
        print_msg = "Peta acak 'Sulit' telah dibuat."
    else: # Medium (Normal)
        NUM_WALL_CLUSTERS = 12; MAX_WALL_LENGTH = 35
        NUM_CARPET_PATCHES = 8; MAX_CARPET_SIZE = 25
        print_msg = "Peta acak 'Normal' telah dibuat."

    # 1. Mulai dengan peta bersih
    for i in range(ROWS):
        for j in range(ROWS):
            if i == 0 or i == ROWS - 1 or j == 0 or j == ROWS - 1:
                grid[i][j].make_wall()
            else:
                grid[i][j].make_floor()

    # 2. "Tumbuhkan" gugus Tembok
    for _ in range(NUM_WALL_CLUSTERS):
        row = random.randint(1, ROWS - 2); col = random.randint(1, ROWS - 2)
        current_length = 0
        while current_length < MAX_WALL_LENGTH:
            pos = (row, col)
            if pos in safe_zones: break 
            if not grid[row][col].is_wall():
                grid[row][col].make_wall(); current_length += 1
            move = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]); row += move[0]; col += move[1]
            if not (1 <= row < ROWS - 2 and 1 <= col < ROWS - 2): break

    # 3. "Tumbuhkan" area Karpet
    for _ in range(NUM_CARPET_PATCHES):
        row = random.randint(1, ROWS - 2); col = random.randint(1, ROWS - 2)
        current_size = 0
        while current_size < MAX_CARPET_SIZE:
            pos = (row, col)
            if pos in safe_zones: break
            if (not grid[row][col].is_wall()) and (pos not in safe_zones):
                grid[row][col].make_carpet(); current_size += 1
            move = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]); row += move[0]; col += move[1]
            if not (1 <= row < ROWS - 2 and 1 <= col < ROWS - 2): break
                
    # 4. Pembersihan Terakhir
    for pos in safe_zones:
        grid[pos[0]][pos[1]].make_floor()
    print(print_msg)


# --- FUNGSI BARU: VALIDASI PETA ---
def is_map_connected(grid, all_spawn_points):
    """
    Memeriksa apakah semua titik spawn dapat dijangkau dari titik pertama
    menggunakan BFS (flood-fill).
    """
    if not all_spawn_points:
        return True # Peta kosong secara teknis terhubung
        
    start_node = grid[all_spawn_points[0][0]][all_spawn_points[0][1]]
    goal_nodes = {grid[pos[0]][pos[1]] for pos in all_spawn_points[1:]}
    
    q = queue.Queue()
    q.put(start_node)
    visited = {start_node}
    
    while not q.empty():
        current = q.get()
        
        # Cek apakah kita menemukan salah satu tujuan
        if current in goal_nodes:
            goal_nodes.remove(current) # Hapus dari daftar yg belum ditemukan
            
        # Lanjutkan pencarian
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                q.put(neighbor)
                
    # Jika 'goal_nodes' kosong, berarti semua telah ditemukan/terhubung
    return len(goal_nodes) == 0

# --- -------------------------- ---


# --- FUNGSI TAMPILAN PESAN ---
def show_message(win, text, title_font, regular_font):
    win.fill(WARNA_HITAM)
    lines = text.split('\n')
    start_y = (WIDTH // 2) - (len(lines) * 30) 
    for i, line in enumerate(lines):
        if line.startswith("[") or line.islower() or line.startswith("("): font_to_use = regular_font
        else: font_to_use = title_font
        text_surface = font_to_use.render(line, True, WARNA_PUTIH)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, start_y + i * 45))
        win.blit(text_surface, text_rect)
    pygame.display.update()

# --- FUNGSI MENU UTAMA ---
def show_menu_screen(win):
    menu_text = (
        "THE DIAMOND HEIST\n\n"
        "PILIH TINGKAT KESULITAN\n\n"
        "[E] Mudah\n"
        "(1 Penjaga BFS, bergerak 1x tiap 2 langkahmu)\n\n"
        "[M] Normal\n"
        "(2 Penjaga, bergerak 1x tiap 1 langkahmu)\n\n"
        "[H] Sulit\n"
        "(2 Penjaga, A* bergerak 2x tiap 1 langkahmu)"
    )
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    option_font = pygame.font.SysFont('Arial', 24)
    while True:
        show_message(win, menu_text, title_font, option_font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: return "EASY"
                if event.key == pygame.K_m: return "MEDIUM"
                if event.key == pygame.K_h: return "HARD"
                if event.key == pygame.K_q: return None

# --- FUNGSI SESI GAME (DIUBAH DENGAN VALIDASI) ---
def run_game_session(win, width, difficulty, sprites):
    
    grid = make_grid(ROWS, width)
    player_move_count = 0 
    
    # --- LOOP VALIDASI PETA ---
    map_valid = False
    while not map_valid:
        # 1. Tentukan Posisi Spawn Kuadran
        mid_row = ROWS // 2; mid_col = ROWS // 2
        q1_spawns = [(r, c) for r in range(2, mid_row - 1) for c in range(2, mid_col - 1)]
        q2_spawns = [(r, c) for r in range(2, mid_row - 1) for c in range(mid_col + 1, ROWS - 2)]
        q3_spawns = [(r, c) for r in range(mid_row + 1, ROWS - 2) for c in range(2, mid_col - 1)]
        q4_spawns = [(r, c) for r in range(mid_row + 1, ROWS - 2) for c in range(mid_col + 1, ROWS - 2)]

        try:
            START_POS = random.choice(q1_spawns)        # Kiri Atas
            DIAMOND_POS = random.choice(q4_spawns)      # Kanan Bawah
            GUARD_BFS_POS = random.choice(q2_spawns)    # Kanan Atas
            GUARD_ASTAR_POS = random.choice(q3_spawns)  # Kiri Bawah
            EXIT_POS = START_POS
        except IndexError:
            print("Error: Grid terlalu kecil."); return "QUIT"
        
        # Tentukan zona aman
        all_spawn_points = [START_POS, DIAMOND_POS, GUARD_BFS_POS, GUARD_ASTAR_POS]
        safe_zones = set(all_spawn_points)

        # 2. Buat Peta (DENGAN TEMBOK)
        create_random_map_with_walls(grid, safe_zones, difficulty)
        
        # 3. Update neighbors SETELAH peta dibuat
        for row in grid:
            for node in row:
                node.update_neighbors(grid)
                
        # 4. JALANKAN VALIDASI
        map_valid = is_map_connected(grid, all_spawn_points)
        
        if not map_valid:
            print("Peta tidak valid (ada yang terjebak), membuat ulang...")
            # Loop akan otomatis berulang
            
    # --- PETA DIJAMIN VALID ---
    
    # 5. Buat Entitas
    player = Player(START_POS[0], START_POS[1], sprites["player"])
    guard_bfs = Guard(GUARD_BFS_POS[0], GUARD_BFS_POS[1], sprites["guard_bfs"], "BFS")
    guard_astar = Guard(GUARD_ASTAR_POS[0], GUARD_ASTAR_POS[1], sprites["guard_astar"], "A*")
    
    active_guards = []
    if difficulty == "EASY":
        active_guards.append(guard_bfs)
    else: 
        active_guards.append(guard_bfs); active_guards.append(guard_astar)

    run_game = True; game_over = False; win_message = ""; clock = pygame.time.Clock()
    
    print(f"\n--- PERMAINAN BARU DIMULAI (Tingkat: {difficulty}) ---")
    print(f"Pemain di: {START_POS}, Berlian di: {DIAMOND_POS}")
    print(f"Penjaga BFS di: {GUARD_BFS_POS}, Penjaga A* di: {GUARD_ASTAR_POS}")
    print("Kontrol: Panah (Atas, Bawah, Kiri, Kanan)")

    # --- LOOP GAME ---
    while run_game:
        clock.tick(10)
        draw_game(win, grid, ROWS, width, player, active_guards, DIAMOND_POS, EXIT_POS, difficulty, sprites)
        
        player_moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                dr, dc = 0, 0
                if event.key == pygame.K_LEFT: dr, dc = -1, 0
                elif event.key == pygame.K_RIGHT: dr, dc = 1, 0
                elif event.key == pygame.K_UP: dr, dc = 0, -1
                elif event.key == pygame.K_DOWN: dr, dc = 0, 1
                if (dr, dc) != (0, 0) and not game_over:
                    player_moved = player.move(dr, dc, grid)

        if player_moved and not game_over:
            player_move_count += 1
            run_ai_turn = False
            if difficulty == "EASY":
                if player_move_count % 2 == 0: run_ai_turn = True
            else: run_ai_turn = True
            
            if run_ai_turn:
                player_node = grid[player.row][player.col]
                for guard in active_guards:
                    guard.move(grid, player_node)
                    if difficulty == "HARD" and guard.algo_type == 'A*':
                        if not (guard.row == player.row and guard.col == player.col):
                            guard.move(grid, player_node) 

        if not game_over:
            for guard in active_guards:
                if guard.row == player.row and guard.col == player.col:
                    win_message = "ANDA KALAH!"; game_over = True; run_game = False; break
            if game_over: continue
            
            if not player.has_diamond:
                if player.row == DIAMOND_POS[0] and player.col == DIAMOND_POS[1]:
                    player.has_diamond = True; print("--- ANDA MENDAPATKAN BERLIAN! ---")
            
            if player.has_diamond:
                if player.row == EXIT_POS[0] and player.col == EXIT_POS[1]:
                    win_message = "ANDA MENANG!"; game_over = True; run_game = False
    
    if game_over:
        msg = f"{win_message}\n\nTekan 'R' untuk Mulai Ulang (Level Ini)\n\nTekan 'M' untuk kembali ke Menu\n\nTekan 'Q' untuk Keluar"
        show_message(win, msg, GAME_FONT, INFO_FONT)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: return "RESTART"
                    if event.key == pygame.K_m: return "MENU"
                    if event.key == pygame.K_q: return "QUIT"
    return "QUIT" 

# --- FUNGSI UTAMA (MAIN LOOP) ---
def main(win, width):
    run_app = True
    
    gap = WIDTH // ROWS
    sprites = {
        "player": create_player_sprite(gap),
        "guard_bfs": create_guard_sprite(gap, WARNA_AI_BFS),
        "guard_astar": create_guard_sprite(gap, WARNA_AI_ASTAR),
        "diamond": create_diamond_sprite(gap),
        "exit": create_exit_sprite(gap)
    }
    
    while run_app:
        difficulty = show_menu_screen(win)
        if difficulty is None: run_app = False; break
            
        while True: 
            game_result = run_game_session(win, width, difficulty, sprites) 
            if game_result == "QUIT": run_app = False; break
            elif game_result == "MENU": break 
            elif game_result == "RESTART": continue 
                
    pygame.quit()
    sys.exit()

# --- ENTRY POINT ---
if __name__ == "__main__":
    main(WIN, WIDTH)