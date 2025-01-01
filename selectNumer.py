from typing import Optional
class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 72 #button width
        self.btn_h = 72 #button height
        self.my_font = font

        self.color_selected = (37,177,24)
        self.color_normal = (123,132,124)

        self.btn_positions = [(740, 80), (830, 80), (920, 80),
                              (740, 170), (830, 170), (920, 170),
                              (740, 260), (830, 260), (920, 260)]
        self.selected_number = 0


    def draw(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_w, self.btn_h], width = 3, border_radius = 15)

            #Kiểm tra sự kiện chọn
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width = 3 , border_radius = 15)
                text_surface = self.my_font.render(str(index + 1), True, (0, 255, 0))
            else:
                text_surface = self.my_font.render(str(index + 1), True, self.color_normal)

            #Kiem tra mot so da duoc chon chua, va danh dau mau xanh la
            if self.selected_number > 0:
                if self.selected_number - 1 == index:
                    pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width = 3, border_radius = 15)
                    text_surface = self.my_font.render(str(index + 1), True,
                                                       self.color_selected)
            # Adjust text position to center it within the button
            text_x = pos[0] + (self.btn_w - text_surface.get_width()) // 2
            text_y = pos[1] + (self.btn_h - text_surface.get_height()) // 2

            # Draw the number in the center of the button
            surface.blit(text_surface, (text_x, text_y))

    #Nhan vao nut de thay doi gia tri
    def button_clicked(self, mouse_x: int, mouse_y: int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = index + 1


    def button_hover(self, pos: tuple) -> bool|None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        return pos[0] < mouse_x < pos[0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h