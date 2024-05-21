import pygame,sys,random,time

pygame.init()

bg_color = (253, 245, 230)
sq_color = (211,211,211)

number_font  = pygame.font.SysFont( None, 150 )                # Default font, Size 128
class square:
    Square = []
    def __init__(self):
        self.pos = len(square.Square)
        self.x = self.pos % 4
        self.y = self.pos // 4
        self.number = None
        self.lenght = 150
        self.space = 10

    def set_number(self, number = None):
        self.number = number

    def get_square(pos):
        return square.Square[pos]
    
    def get_pos(self):
        return self.pos
    
    def draw(self):
        pygame.draw.rect(wn, sq_color, #display and color
                        (self.x * self.lenght + self.x * self.space + 10, #x
                         self.y * self.lenght + self.y * self.space + 100, #y
                         self.lenght, self.lenght) ) #lenght
        if self.number is not None:
            number_image = number_font.render(str(self.number), True, "BLACK", "WHITE" )  # Number 8
            wn.blit(number_image,
                    (self.x * self.lenght + self.x * self.space + 10, #x
                     self.y * self.lenght + self.y * self.space + 100)) #y
            
    def get_number(self):
        return self.number
    
wn = pygame.display.set_mode((650,740))
pygame.display.set_caption("2048")
pygame.draw.rect(wn, bg_color,(0,0,650,740))


for i in range(16):
    square.Square.append(square())

def draw_squares():
    for sq in square.Square:
        sq.draw()

def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def check_inputs():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_up()
    elif keys[pygame.K_a]:
        move_left()
    elif keys[pygame.K_s]:
        move_down()
    elif keys[pygame.K_d]:
        move_right()

def move_up():
    moved = False  # Flag to track if any move was made

    for x in range(4):
        for y in range(3, 0, -1):
            current_sq = square.get_square(y * 4 + x)
            if current_sq.get_number() is not None:
                for y2 in range(y - 1, -1, -1):
                    next_sq = square.get_square(y2 * 4 + x)
                    if next_sq.get_number() is None:
                        next_sq.set_number(current_sq.get_number())
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    elif next_sq.get_number() == current_sq.get_number():
                        # Merge Square with the same number
                        next_sq.set_number(next_sq.get_number() * 2)
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    else:
                        break

    if moved:  # Only add a new square if a move was made
        new_move()

def move_down():
    moved = False  # Flag to track if any move was made

    for x in range(4):
        for y in range(2, -1, -1):
            current_sq = square.get_square(y * 4 + x)
            if current_sq.get_number() is not None:
                for y2 in range(y + 1, 4):
                    next_sq = square.get_square(y2 * 4 + x)
                    if next_sq.get_number() is None:
                        next_sq.set_number(current_sq.get_number())
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    elif next_sq.get_number() == current_sq.get_number():
                        # Merge Square with the same number
                        next_sq.set_number(next_sq.get_number() * 2)
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    else:
                        break

    if moved:  # Only add a new square if a move was made
        new_move()

def move_left():
    moved = False  # Flag to track if any move was made

    for y in range(4):
        for x in range(1, 4):
            current_sq = square.get_square(y * 4 + x)
            if current_sq.get_number() is not None:
                for x2 in range(x - 1, -1, -1):
                    next_sq = square.get_square(y * 4 + x2)
                    if next_sq.get_number() is None:
                        next_sq.set_number(current_sq.get_number())
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    elif next_sq.get_number() == current_sq.get_number():
                        # Merge Square with the same number
                        next_sq.set_number(next_sq.get_number() * 2)
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    else:
                        break

    if moved:  # Only add a new square if a move was made
        new_move()

def move_right():
    moved = False  # Flag to track if any move was made

    for y in range(4):
        for x in range(2, -1, -1):
            current_sq = square.get_square(y * 4 + x)
            if current_sq.get_number() is not None:
                for x2 in range(x + 1, 4):
                    next_sq = square.get_square(y * 4 + x2)
                    if next_sq.get_number() is None:
                        next_sq.set_number(current_sq.get_number())
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    elif next_sq.get_number() == current_sq.get_number():
                        # Merge Square with the same number
                        next_sq.set_number(next_sq.get_number() * 2)
                        current_sq.set_number(None)
                        moved = True  # A move was made
                        break
                    else:
                        break

    if moved:  # Only add a new square if a move was made
        new_move()

def new_move():
    empty_sq = [sq.get_pos() for sq in square.Square if sq.get_number() is None]
    chosen_sq = random.choice(empty_sq)
    luck = random.randint(0,10)
    new_number = 4 if luck == 0 else 2
    square.get_square(chosen_sq).set_number(new_number)

new_move()

while True:
    check_exit()
    check_inputs()
    draw_squares()
    pygame.display.flip()
    Clock =pygame.time.Clock()
    Clock.tick(5)