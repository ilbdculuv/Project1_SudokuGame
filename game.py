import pygame
import os
import ctypes
from generateGrid import Grid
import time

# Lấy độ phân giải màn hình
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Tính toán vị trí giữa màn hình
window_width, window_height = 1015, 725
pos_x = (screen_width - window_width) // 2
pos_y = (screen_height - window_height) // 2

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x}, {pos_y}"

# Tạo cửa sổ
pygame.init()
surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Sudoku")

pygame.font.init()
game_font = pygame.font.SysFont('Lobster', 70)
game_font2 = pygame.font.SysFont('Lobster', 30)
clock_font = pygame.font.SysFont(' Comic Sans MS', 25)  # Font cho đồng hồ bấm giờ

grid = Grid(pygame, game_font)

# Lấy thời gian bắt đầu game
start_time = time.time()
game_over = False
stop_timer = False
final_remaining_time = 0

countdown_time = 60

# Vòng lặp chính
running = True
while running:
    # Tính toán thời gian đã trôi qua
    if not stop_timer:
        elapsed_time = time.time() - start_time
        remaining_time = countdown_time - int(elapsed_time)
    else:
        remaining_time = final_remaining_time

    # Khi thời gian còn lại bằng 0, dừng lại
    if remaining_time <= 0 and not game_over:
        grid.lock_grid()  # Khóa bảng không cho nhập sau khi hết giờ
        game_over = True


    minutes, seconds = divmod(remaining_time, 60)
    formatted_time = f"{minutes:02}:{seconds:02}"


    time_text = f"Time: {formatted_time}" if remaining_time > 0 else "Time's up!"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Kiểm tra sự kiện nếu chưa hết giờ và game chưa thắng
        if not game_over:  # Nếu chưa hết giờ, xử lý sự kiện tương tác với bảng
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    grid.get_mouse_click(pos[0], pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and grid.win:
                    grid.restart()
                    start_time = time.time()
                    stop_timer = False
                    final_remaining_time = 0
                if event.key == pygame.K_SPACE and not grid.win:
                    grid.restart()
                    start_time = time.time()
                    stop_timer = False
                    final_remaining_time = 0


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
            grid.restart()
            start_time = time.time()
            game_over = False
            stop_timer = False
            final_remaining_time = 0

    # Thay đổi màu nền
    surface.fill((251, 251, 247))

    # Vẽ bảng
    grid.draw_all(pygame, surface)

    # Nếu thắng, chỉ hiển thị "You Won!" và dừng đồng hồ
    if grid.win:
        won_surface = game_font.render("You Won!", True, (214, 15, 15))
        surface.blit(won_surface, (755, 415))

        if not stop_timer:
            stop_timer = True
            final_remaining_time = remaining_time  # Store the final remaining time when the player wins

        press_enter_surf = game_font2.render("Press ENTER for new game!", True, (0, 0, 0))
        surface.blit(press_enter_surf, (731, 485))


    if game_over and not grid.win:
        time_out_surface = game_font.render("You Lose!", True, (214, 15, 15))
        surface.blit(time_out_surface, (755, 415))

        press_enter_surf = game_font2.render("Press ENTER for new game!", True, (0, 0, 0))
        surface.blit(press_enter_surf, (731, 485))

    else:
        if not grid.win and not game_over:
            press_1_surf = game_font2.render("Press SPACE to restart!", True, (214, 15, 15))
            surface.blit(press_1_surf, (755, 360))

    # Hiển thị đồng hồ bấm giờ
    if not grid.win:
        timer_surface = clock_font.render(time_text, True, (0, 0, 0))
    else:
        minutes, seconds = divmod(final_remaining_time, 60)
        formatted_final_time = f"{minutes:02}:{seconds:02}"
        timer_surface = clock_font.render(f"Time: {formatted_final_time}", True, (0, 0, 0))

    surface.blit(timer_surface, (800, 30))


    # Cập nhật cửa sổ
    pygame.display.flip()
