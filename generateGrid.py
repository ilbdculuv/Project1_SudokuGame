import pygame
from random import sample
from selectNumer import SelectNumber
from copy import deepcopy
import time

def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    """ Tạo tọa độ cho các đường kẻ ngang và dọc của lưới Sudoku """
    points = []
    for y in range(1, 9):
        temp = []
        #Đường ngang
        temp.append((0, y*cell_size)) # x, y points [(0,100), (0,200)....]
        temp.append((720, y *cell_size)) # x, y point [(900,100), (900, 200), ....]
        points.append(temp)

    for x in range(1, 10):
        #Đường doc
        temp = []
        temp.append((x * cell_size, 0)) # x, y points [(100, 0), (200, 0)....]
        temp.append((x * cell_size, 720)) # x, y point [(100, 900), (200, 900), ....]
        points.append(temp)
    print(points)
    return points

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

#Xác định giá trị của một ô trong bảng Sudoku
def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

#Xáo trộn một danh sách các phần tử.
def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    row_base = range(sub_grid)
    rows = [g* sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)] #tron hang
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)] #tron cot
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_numbers(grid: list[list]) -> None:
    """ Tao khoang trong trong bang 9x9"""
    num_of_cells = GRID_SIZE * GRID_SIZE

    """Dieu chinh do kho"""
    empties = num_of_cells * 3 // 15
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


class Grid:
    def __init__(self, pygame, font):
        self.cell_size = 80
        self.num_x_offset = 26 #Điều chỉnh chiều ngang
        self.num_y_offset = 20 #Điều chỉnh chiều dọc
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid) #Tao mot ban sao truoc khi xoa mot so
        print(self.__test_grid)
        self.win = False

        remove_numbers(self.grid)

        self.pre_occupied_cells_coordinates = self.pre_occupied_cells()

        print(self.pre_occupied_cells_coordinates)

        self.game_font = font

        self.selection = SelectNumber(pygame, self. game_font)

        # Thêm biến start_time để theo dõi thời gian bắt đầu
        self.start_time = time.time()


    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.pre_occupied_cells_coordinates = self.pre_occupied_cells()
        self.win = False
        self.start_time = time.time()  # Cập nhật lại thời gian khi restart

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        """Check for none-playable cells: preoccupied/ initialized cells """
        for cell in self.pre_occupied_cells_coordinates: #Truy cap phuong thuc pre_occupied_cells()
            if x == cell[1] and y == cell[0]: # x is col, y is row
                return True
        return False

    def get_remaining_time(self) -> int:
        """Trả về thời gian còn lại trong 3 giây"""
        elapsed_time = time.time() - self.start_time
        remaining_time = 60 - int(elapsed_time)
        return remaining_time if remaining_time >= 0 else 0  # Không cho phép thời gian dưới 0

    def lock_grid(self) -> None:
        """Khóa bảng khi hết giờ"""
        if self.get_remaining_time() == 0:
            self.win = False  # Không set win = True khi hết giờ (thua)
            # Thêm thông báo "You Lose!" khi hết giờ
            time_out_surface = self.game_font.render("You Lose!", True, (214, 15, 15))
            return time_out_surface


    #Kiem tra so voi bang ban dau
    def check_grids(self):
        for y in range (len(self.grid)):
            for x in range (len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    #Kiem tra xem mot o co dien duoc so hay khong
    def get_mouse_click(self, x : int, y: int) -> None:
        if self.get_remaining_time() > 0:  # Chỉ cho phép người chơi chọn ô khi còn thời gian
            if x <= 720:
                grid_x, grid_y = x // 80, y // 80
                if not self.is_cell_preoccupied(grid_x, grid_y):
                    self.set_cell(grid_x, grid_y, self.selection.selected_number)
            self.selection.button_clicked(x, y)
            if self.check_grids():
                self.win = True
        self.lock_grid()  # Kiểm tra và khóa bảng khi hết thời gian

    #Tra ve danh sach toa do cac o bi chiem trong bang
    def pre_occupied_cells(self) -> list[tuple]:
        """Tap hop tat ca cac toa do cho cac diem da chiem trong bang"""

        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range (len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    occupied_cell_coordinates.append((y,x))
        return occupied_cell_coordinates

    def __draw_lines(self, pg, surface) -> None:
        # Vẽ các đường phụ (đường màu trắng mỏng) trước
        for index, point in enumerate(self.line_coordinates):
            if index != 2 and index != 5 and index != 10 and index != 13 and index != 16:

                pg.draw.line(surface, (231,233,233), point[0], point[1], 1)  # Đường trắng mỏng

        # Vẽ các đường chính (đường màu đen dày hơn) sau
        for index, point in enumerate(self.line_coordinates):

            # Các đường chính khác (đường đen dày hơn)
            if  index == 2 or index == 5 or index == 10 or index == 13 or index == 16:
                # Điều chỉnh các điểm đầu và điểm cuối của đường
                start_point = point[0]
                end_point = point[1]

                # Giới hạn các đường kẻ đen đậm để chúng không vượt quá bảng
                if start_point[0] < 0: start_point = (0, start_point[1])  # Bắt đầu từ x = 0 nếu x < 0
                if end_point[0] > 715: end_point = (720, end_point[1])  # Dừng tại x = 720 nếu x > 720

                if start_point[1] < 0: start_point = (start_point[0], 0)  # Bắt đầu từ y = 0 nếu y < 0
                if end_point[1] > 700: end_point = (end_point[0], 700)  # Dừng tại y = 720 nếu y > 720

                pg.draw.line(surface, (0, 0, 0), point[0], point[1], 3)  # Đường đen dày
    # Vẽ thêm đường viền bao quanh bảng
            offset = 2 # Dịch xuống và sang phải

            pg.draw.line(surface, (0, 0, 0), (offset, offset), (720, offset), 3)  # Đường viền trên
            # Đường viền phải
            pg.draw.line(surface, (0, 0, 0), (720, offset), (720, 720), 3)  # Đường viền phải
            # Đường viền dưới
            pg.draw.line(surface, (0, 0, 0), (720, 720), (offset, 720), 3)  # Đường viền dưới
            # Đường viền trái
            pg.draw.line(surface, (0, 0, 0), (offset, 720), (offset, offset), 3)  # Đường viền t
    def __draw_numbers(self, surface) -> None:
        """Draw the grid numbers """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0: #Kiem tra xem mot o co trong khong
                    if (y, x) in self.pre_occupied_cells_coordinates:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), True, (108,214,236)) #xanh duong
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), True, (0, 255, 0))

                    if self.get_cell(x, y) != self.__test_grid[y][x]: #check xem co trung voi ket qua chinh xac khong
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), True, (255, 0, 0)) # mau do

                    surface.blit(text_surface,
                                (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))

    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

    def get_cell(self, x: int, y: int) -> int:
        """Get a cell value at y, x coordinate """
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
         """Set a cell value at y, x coordinate """
         self.grid[y][x] = value


    def show(self):
        for row in self.grid:
            print(row)




if __name__ == "__main__":
    pygame.init()
    font = pygame.font.SysFont('Lobster', 50)
    grid = Grid(pygame, font)
    grid.show()