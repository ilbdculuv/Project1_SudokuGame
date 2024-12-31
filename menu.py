import pygame
import time

class Menu:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.font = font
        self.btn_width = 300
        self.btn_height = 80
        self.color_normal = (123, 132, 124)
        self.color_hover = (37, 177, 24)

        # Các nút độ khó
        self.difficulty_btn_positions = [
            (250, 200),  # Easy
            (250, 300),  # Medium
            (250, 400),  # Hard
        ]

        self.difficulty_text = ['Easy', 'Medium', 'Hard']
        self.selected_difficulty = None

    def draw(self, surface):
        """ Vẽ menu và các nút chọn độ khó """
        for index, pos in enumerate(self.difficulty_btn_positions):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_width, self.btn_height], width=3, border_radius=15)

            # Kiểm tra nếu chuột hover
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_hover, [pos[0], pos[1], self.btn_width, self.btn_height], width=3, border_radius=15)
                text_surface = self.font.render(self.difficulty_text[index], True, (0, 255, 0))
            else:
                text_surface = self.font.render(self.difficulty_text[index], True, self.color_normal)

            # Vị trí chữ để căn giữa trong nút
            text_x = pos[0] + (self.btn_width - text_surface.get_width()) // 2
            text_y = pos[1] + (self.btn_height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))

    def button_clicked(self, mouse_x: int, mouse_y: int):
        """ Kiểm tra xem người chơi đã chọn độ khó chưa """
        for index, pos in enumerate(self.difficulty_btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_difficulty = index  # Lưu độ khó đã chọn
                return self.selected_difficulty  # Trả về độ khó đã chọn

    def button_hover(self, pos: tuple) -> bool:
        """ Kiểm tra nếu chuột đang hover qua nút """
        mouse_pos = self.pygame.mouse.get_pos()
        return self.on_button(mouse_pos[0], mouse_pos[1], pos)

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        """ Kiểm tra nếu chuột đang nằm trong vùng của nút """
        return pos[0] < mouse_x < pos[0] + self.btn_width and pos[1] < mouse_y < pos[1] + self.btn_height

    def get_selected_difficulty(self):
        """ Trả về độ khó đã chọn """
        return self.selected_difficulty
