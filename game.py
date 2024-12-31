import pygame
import os
import ctypes
from generateGrid import Grid
import time  # Thêm thư viện time để quản lý đồng hồ bấm giờ

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
start_time = time.time()  # Ghi lại thời gian bắt đầu
game_over = False  # Biến flag để dừng đồng hồ khi hết thời gian
stop_timer = False  # Flag to stop the timer when the game is won
final_remaining_time = 0  # To store the final remaining time when the player wins

# Thời gian countdown (10 giây)
countdown_time = 60  # Thay đổi thời gian còn lại thành 10 giây

# Vòng lặp chính
running = True
while running:
    # Tính toán thời gian đã trôi qua
    if not stop_timer:
        elapsed_time = time.time() - start_time  # Thời gian trôi qua kể từ khi game bắt đầu
        remaining_time = countdown_time - int(elapsed_time)  # Tính thời gian còn lại
    else:
        remaining_time = final_remaining_time  # After winning, keep showing the final remaining time

    # Khi thời gian còn lại bằng 0, dừng lại
    if remaining_time <= 0 and not game_over:
        grid.lock_grid()  # Khóa bảng không cho nhập sau khi hết giờ
        game_over = True  # Đánh dấu là đã hết giờ

    # Convert remaining time into minutes and seconds
    minutes, seconds = divmod(remaining_time, 60)
    formatted_time = f"{minutes:02}:{seconds:02}"

    # Định dạng thời gian: Hiển thị thời gian còn lại khi chưa hết giờ, nếu đã hết giờ hiển thị "Time's up!"
    time_text = f"Time: {formatted_time}" if remaining_time > 0 else "Time's up!"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Kiểm tra sự kiện nếu chưa hết giờ và game chưa thắng
        if not game_over:  # Nếu chưa hết giờ, xử lý sự kiện tương tác với bảng
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # check for the left mouse button
                    pos = pygame.mouse.get_pos()
                    grid.get_mouse_click(pos[0], pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and grid.win:
                    grid.restart()
                    start_time = time.time()  # Reset thời gian khi khởi động lại
                    stop_timer = False  # Resuming the timer when starting a new game
                    final_remaining_time = 0  # Reset the final time when restarting the game
                if event.key == pygame.K_SPACE and not grid.win:  # Nhấn phím SPACE để khởi động lại bất kỳ lúc nào
                    grid.restart()
                    start_time = time.time()  # Reset thời gian khi khởi động lại
                    stop_timer = False  # Resuming the timer when starting a new game
                    final_remaining_time = 0  # Reset the final time when restarting the game

        # Dù hết giờ, nhấn phím ENTER vẫn có thể khởi động lại
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
            grid.restart()  # Khởi động lại game khi nhấn ENTER
            start_time = time.time()  # Reset thời gian khi khởi động lại
            game_over = False  # Reset trạng thái game_over
            stop_timer = False  # Resuming the timer after restarting
            final_remaining_time = 0  # Reset the final time when restarting

    # Thay đổi màu nền
    surface.fill((251, 251, 247))

    # Vẽ bảng
    grid.draw_all(pygame, surface)

    # Nếu thắng, chỉ hiển thị "You Won!" và dừng đồng hồ
    if grid.win:
        won_surface = game_font.render("You Won!", True, (214, 15, 15))
        surface.blit(won_surface, (755, 415))

        # Stop the timer when the game is won
        if not stop_timer:
            stop_timer = True
            final_remaining_time = remaining_time  # Store the final remaining time when the player wins

        # Thông điệp hướng dẫn khi game thắng
        press_enter_surf = game_font2.render("Press ENTER for new game!", True, (0, 0, 0))
        surface.blit(press_enter_surf, (731, 485))

    # Nếu hết giờ, chỉ hiển thị "You Lose!"
    if game_over and not grid.win:  # Only show "You Lose!" if the game is over and not won
        time_out_surface = game_font.render("You Lose!", True, (214, 15, 15))  # Hiển thị "You Lose!"
        surface.blit(time_out_surface, (755, 415))  # Vị trí hiển thị thông báo

        # Thêm dòng hướng dẫn khi nhấn phím ENTER
        press_enter_surf = game_font2.render("Press ENTER for new game!", True, (0, 0, 0))
        surface.blit(press_enter_surf, (731, 485))  # Hiển thị dòng hướng dẫn dưới "You Lose!"

    else:
        # Chỉ hiển thị dòng "Press SPACE to restart!" nếu chưa thắng và chưa hết giờ
        if not grid.win and not game_over:
            press_1_surf = game_font2.render("Press SPACE to restart!", True, (214, 15, 15))
            surface.blit(press_1_surf, (755, 360))

    # Hiển thị đồng hồ bấm giờ
    if not grid.win:
        timer_surface = clock_font.render(time_text, True, (0, 0, 0))
    else:
        # Display the final remaining time when the game is won
        minutes, seconds = divmod(final_remaining_time, 60)
        formatted_final_time = f"{minutes:02}:{seconds:02}"
        timer_surface = clock_font.render(f"Time: {formatted_final_time}", True, (0, 0, 0))

    surface.blit(timer_surface, (800, 30))  # Vị trí đồng hồ ở góc trên bên phải


    # Cập nhật cửa sổ
    pygame.display.flip()  # Cập nhật màn hình khi có sự thay đổi
