import itertools
import pygame
import random
from Engine.Engine import Engine
from Engine.Grid import Grid
from Engine.Config import get_screenrect, set_screensize
from Engine.Text import text_surface


class TetrisBlockOld:
    def __init__(self, name, color):
        self.name = name
        self.x = 144
        self.y = 16
        self.image = None
        self.width = None
        self.height = None
        self.blocks = []
        self.block_size = 16
        self.rotation = 0
        self.color = color
        self.setup(name)

    def setup(self, name):
        if name == "t":
            self.blocks.append([0, 1, 0])
            self.blocks.append([1, 1, 1])
        elif name == "straight":
            self.blocks.append([1])
            self.blocks.append([1])
            self.blocks.append([1])
            self.blocks.append([1])
        elif name == "normal_l":
            self.blocks.append([1, 0])
            self.blocks.append([1, 0])
            self.blocks.append([1, 1])
        elif name == "backwards_l":
            self.blocks.append([0, 1])
            self.blocks.append([0, 1])
            self.blocks.append([1, 1])
        elif name == "normal_zigzag":
            self.blocks.append([1, 0])
            self.blocks.append([1, 1])
            self.blocks.append([0, 1])
        elif name == "backwards_zigzag":
            self.blocks.append([0, 1])
            self.blocks.append([1, 1])
            self.blocks.append([1, 0])

    def rotate(self, direction):
        self.width, self.height = self.height, self.width
        if direction == "right":
            self.blocks = list(zip(*self.blocks[::-1]))
        elif direction == "left":
            self.blocks = list(zip(*self.blocks[::]))
        self.render_image()

    def get_blocks(self):
        result = []
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[0])):
                if self.blocks[y][x] == 1:
                    new_block = Tetris
                    result.append(pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size))
        return result

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def copy(self):
        t = TetrisBlock(self.name, self.color)
        t.x = self.x
        t.y = self.y
        return t

    def __str__(self):
        return "{}, {} - {} ({})".format(self.x, self.y, self.name, self.color)


class TetrisOld:
    def __init__(self):
        self.screenrect = get_screenrect()
        self.block_names = ["t", "straight", "normal_l", "backwards_l"]
        self.play_rect = pygame.Rect(16, 16, 320, 560)
        self.next_block_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.image = pygame.Surface((self.play_rect.width, self.play_rect.height), pygame.SRCALPHA)
        self.image.fill((50, 50, 50))
        self.block_colors = itertools.cycle([
            (255, 0, 200),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (0, 255, 200),
            (255, 200, 0),
        ])
        self.blocks = []
        self.move_speed = 400
        self.move_ticker = 0
        t = TetrisBlock(random.choice(self.block_names), next(self.block_colors))
        t2 = TetrisBlock(random.choice(self.block_names), next(self.block_colors))
        self.blocks.append(t)
        self.current_block = t
        self.next_block = t2
        self.render_next_block_window()

    def draw(self, canvas):
        canvas.blit(self.image, (self.play_rect.x, self.play_rect.y))
        canvas.blit(self.next_block_image, (self.play_rect.right + 16, 16))
        for block in self.blocks:
            block.draw(canvas)

    def render_next_block_window(self):
        self.next_block_image = pygame.Surface((100, 100))
        x = (100 - self.next_block_image.get_rect().width) // 2
        y = (100 - self.next_block_image.get_rect().height) // 2
        self.next_block_image.blit(self.next_block.image, (x, y))

    def update(self, dt):
        self.move_ticker += dt
        if self.move_ticker > self.move_speed:
            self.move_ticker = 0
            self.update_blocks()
            
    def update_blocks(self):
        new_rect = self.current_block.get_rect()
        new_rect.y += self.current_block.block_size
        new_block = self.current_block.copy()
        new_block.y = new_rect.y
        if self.check_block(new_block):
            print("Updating current block position")
            self.current_block.x = new_rect.x
            self.current_block.y = new_rect.y
        else:
            self.spawn_block()

    def spawn_block(self):
        block_type = random.choice(self.block_names)
        block_color = next(self.block_colors)
        block = TetrisBlock(block_type, block_color)

        self.current_block = self.next_block.copy()
        self.blocks.append(self.current_block)
        self.next_block = block
        self.render_next_block_window()

        return block

    def check_block(self, block):
        if not self.play_rect.contains(block.get_rect()):
            print("check_block returning because rect is not within play_rect")
            return False

        for a_block in self.blocks:
            print("Checking block", a_block)
            if a_block == self.current_block:
                print("block is same block skipping")
                continue
            if a_block.get_rect().colliderect(block.get_rect()):
                print("piece collided with rect, checking blocks")
                block_list = a_block.get_blocks()
                target_block_list = block.get_blocks()
                for b in block_list:
                    collide_list = b.collidelistall(target_block_list)
                    if collide_list:
                        for c in collide_list:
                            print(c)
        return True

    def handle_event(self, event):
        if self.current_block is None:
            return

        event_type = None
        if event.type == pygame.KEYUP:
            new_rect = self.current_block.get_rect()
            if event.key == pygame.K_RIGHT:
                new_rect.x += self.current_block.block_size
                event_type = "move"
            elif event.key == pygame.K_LEFT:
                new_rect.x -= self.current_block.block_size
                event_type = "move"
            elif event.key == pygame.K_DOWN:
                new_rect.y += self.current_block.block_size
                event_type = "move"
            elif event.key == pygame.K_q:
                self.current_block.rotate("left")
                event_type = "rotate"
            elif event.key == pygame.K_e:
                self.current_block.rotate("right")
                event_type = "rotate"
            elif event.key == pygame.K_SPACE:
                print(self.current_block.get_blocks())
            if event_type == "move":
                new_block = self.current_block.copy()
                new_block.x = new_rect.x
                new_block.y = new_rect.y
                can_move = self.check_block(new_block)
                if can_move:
                    self.current_block.x = new_rect.x
                    self.current_block.y = new_rect.y
                else:
                    print("Can't move there")



class Tetrimino:
    def __init__(self, name, color, size):
        self.x = size * 2 + 16
        self.y = 16
        self.name = name
        self.color = color
        self.size = size
        self.width = 0
        self.height = 0
        self.image = None
        self.blocks = []
        self.setup(self.name)
    
    def setup(self, name):
        if name == "t":
            self.blocks.append([0, 1, 0])
            self.blocks.append([1, 1, 1])
        elif name == "straight":
            self.blocks.append([1])
            self.blocks.append([1])
            self.blocks.append([1])
            self.blocks.append([1])
        elif name == "normal_l":
            self.blocks.append([1, 0])
            self.blocks.append([1, 0])
            self.blocks.append([1, 1])
        elif name == "backwards_l":
            self.blocks.append([0, 1])
            self.blocks.append([0, 1])
            self.blocks.append([1, 1])
        elif name == "normal_zigzag":
            self.blocks.append([1, 0])
            self.blocks.append([1, 1])
            self.blocks.append([0, 1])
        elif name == "backwards_zigzag":
            self.blocks.append([0, 1])
            self.blocks.append([1, 1])
            self.blocks.append([1, 0])
        elif name == "square":
            self.blocks.append([1, 1])
            self.blocks.append([1, 1])

        self.width = len(self.blocks[0]) * self.size
        self.height = len(self.blocks) * self.size
        self.render_image()

    def rotate(self, direction):
        # we need to be able to roll this back if 
        # the shape gets off of the play area
        # after a rotate
        # may have to just build a new piece and test it
        # will check later
        self.width, self.height = self.height, self.width
        if direction == "right":
            self.blocks = list(zip(*self.blocks[::-1]))
        elif direction == "left":
            self.blocks = list(zip(*self.blocks[::]))
        self.render_image()

    def get_blocks(self, parent_offset=False):
        result = []
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[0])):
                if self.blocks[y][x] == 1:
                    if parent_offset:
                        result.append((pygame.Rect(
                            (self.x) + (x * self.size),
                            (self.y - self.size) + (y * self.size),
                            self.size, 
                            self.size
                        ), self.color))
                    else:
                        result.append((pygame.Rect(x * self.size, y * self.size, self.size, self.size), self.color))
        return result

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render_image(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for block, color in self.get_blocks():
            pygame.draw.rect(self.image, self.color, block.inflate(-4, -4))

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    def copy(self, x, y):
        t = Tetrimino(self.name, self.color, self.size)
        t.x = x
        t.y = y
        return t


class Tetris:
    def __init__(self):
        self.screenrect = get_screenrect()
        self.block_names = ["t", "straight", "normal_l", "backwards_l", "normal_zigzag", "backwards_zigzag", "square"]
        self.tiles_wide = 8
        self.tiles_high = 10
        self.grid_size = 24
        self.padding = 16
        self.play_rect = pygame.Rect(self.padding, self.padding, self.tiles_wide * self.grid_size, self.tiles_high * self.grid_size)
        
        self.grid = Grid(self.generate_blank_grid())
        self.image = pygame.Surface((self.play_rect.width, self.play_rect.height), pygame.SRCALPHA)
        self.background_image = None
        self.blocks = []
        self.tick_count = 0
        self.piece_count = 0
        self.move_counter = 0
        self.move_timer = 300
        self.block_colors = itertools.cycle([
            (255, 0, 200),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (0, 255, 200),
            (255, 200, 0),
        ])
        self.current_block = Tetrimino(random.choice(self.block_names), next(self.block_colors), self.grid_size)
        self.next_block = Tetrimino(random.choice(self.block_names), next(self.block_colors), self.grid_size)
        self.render_grid()
        self.render_ui()

    def render_ui(self):
        self.render_background()
        self.render_next_block()
        tick_text = text_surface("Ticks: {}".format(self.tick_count), font_size=36)
        piece_text = text_surface("Pieces: {}".format(self.piece_count), font_size=36)
        self.background_image.blit(tick_text, (self.play_rect.right + self.padding, 400))
        self.background_image.blit(piece_text, (self.play_rect.right + self.padding, 400 + tick_text.get_rect().height + self.padding))

    def pixel_to_tile(self, pos):
        if type(pos) == int:
            result = pos // self.grid_size
            return result
        else:
            x = (pos[0]) // self.grid_size
            y = (pos[1]) // self.grid_size
            return (x, y)

    def render_background(self):
        self.background_image = pygame.Surface((self.screenrect.width, self.screenrect.height), pygame.SRCALPHA)
        self.background_image.fill((0, 0, 0))

    def render_next_block(self):
        self.background_image.blit(self.next_block.image, (self.play_rect.right + 16, 16))

    def generate_blank_grid(self):
        result = []
        for y in range(self.tiles_high):
            result.append([])
            for x in range(self.tiles_wide):
                result[y].append(None)
        return result

    def tick(self):
        self.tick_count += 1
        if self.current_block:
            # new_block = Tetrimino(self.current_block.name, self.current_block.color, self.current_block.size)
            # new_block.y = new_rect.y
            cur_rect = self.current_block.get_rect()
            self.current_block.y += self.current_block.size
            can_move = self.check_block(self.current_block)
            if not can_move:
                self.spawn_new_block()
            self.render_ui()

    def spawn_new_block(self):
        self.piece_count += 1
        blocks = self.current_block.get_blocks(parent_offset=True)
        for block in blocks:
            gx, gy = self.pixel_to_tile((block[0].x, block[0].y))
            if not self.grid.set_cell(gx, gy, block[1]):
                print("Unable to set cell: ", gx, gy, block[1])
        self.current_block = self.next_block
        self.next_block = Tetrimino(random.choice(self.block_names), next(self.block_colors), self.grid_size)
        self.render_next_block()
        self.update_grid()
        self.check_for_rows()

    def check_for_rows(self):
        print("Checking for rows")
        full_rows = []
        for index, row in enumerate(self.grid.grid):
            if None not in row:
                full_rows.append(index)
        if full_rows:
            full_rows.sort()
            print("We found some full rows: ", full_rows)
            for row_index in full_rows:
                del self.grid.grid[row_index]
                new_row = list([None for x in range(self.grid.width)])
                print(new_row)
                self.grid.grid.insert(0, new_row)
            self.update_grid()
        
    def print_grid(self):
        for row in self.grid.grid:
            print(row)

    def update_grid(self):
        self.image = pygame.Surface((self.play_rect.width, self.play_rect.height), pygame.SRCALPHA)
        self.render_grid()
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell:
                    cell_rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                    pygame.draw.rect(self.image, cell, cell_rect.inflate(-4, -4))

    def check_block(self, block):
        block_rect = block.get_rect()
        if not self.play_rect.contains(block_rect):
            return False
        block_list = block.get_blocks(parent_offset=True)
        for b in block_list:
            bx, by = self.pixel_to_tile((b[0].x, b[0].y + self.grid_size))
            cell = self.grid.get_cell(bx, by)
            if cell is not None:
                return False
        return True

    def update(self, dt):
        self.move_counter += dt
        if self.move_counter > self.move_timer:
            self.move_counter = 0
            self.tick()

    def render_grid(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                r = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.image, (100, 100, 100), r.inflate(-1, -1), 1)
                if y == 0:
                    if x == self.grid.width - 1:
                        txt = text_surface("{}".format(self.pixel_to_tile(r.x)))
                        txt2 = text_surface("{}".format(self.pixel_to_tile(r.y)))
                        self.image.blit(txt, (r.x + 6, r.y + 6))
                        self.image.blit(txt2, (r.x + 12, r.y + 12))
                    else:
                        txt = text_surface("{}".format(self.pixel_to_tile(r.x)))
                        self.image.blit(txt, (r.x + 6, r.y + 6))

                elif x == self.grid.width - 1:
                    if y != 0:
                        txt = text_surface("{}".format(self.pixel_to_tile(r.y)))
                        self.image.blit(txt, (r.x + 6, r.y + 6))

    def draw(self, canvas):
        canvas.blit(self.background_image, (0, 0))
        pygame.draw.rect(canvas, (25, 25, 25), self.play_rect)
        canvas.blit(self.image, (16, 16))
        if self.current_block:
            self.current_block.draw(canvas)

    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def handle_event(self, event):
        if self.current_block is None:
            return
        if event.type == pygame.KEYUP:
            test_block = None
            if event.key == pygame.K_RIGHT:
                test_block = self.current_block.copy(x=self.current_block.x + self.current_block.size, y=self.current_block.y)
            elif event.key == pygame.K_LEFT:
                test_block = self.current_block.copy(x=self.current_block.x - self.current_block.size, y=self.current_block.y)
            elif event.key == pygame.K_DOWN:
                test_block = self.current_block.copy(x=self.current_block.x, y=self.current_block.y + self.current_block.size)

            if test_block and self.check_block(test_block):
                self.current_block.x = test_block.x
                self.current_block.y = test_block.y
                return

            if event.key == pygame.K_UP:
                self.current_block.rotate("right")


if __name__ == "__main__":
    set_screensize(800, 600)
    e = Engine(Tetris)
    e.game_loop()
