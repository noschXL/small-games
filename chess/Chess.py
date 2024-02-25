import pygame
import pygame_gui
import os
import time
import sys
# Load pygame
pygame.init()
pygame.mixer.init()
pathdir = os.path.dirname(os.path.abspath(__file__))
start_pos = "ts/ks/ls/ds/as/ls/ks/ts/bs8/e32/bw8/tw/kw/lw/dw/aw/lw/kw/tw/p" # b = pawn, t = rook, k = knight, l = bishop, d = queen, a = king, e = empty, w = white, s = black, p = white player, P = black player

open(pathdir + "/saves/save.dat", "a").close()
# english / deutsch
# plans / Pläne
# play against AI / gegen einen Computer spielen
# online multiplayer / online mehrspieler
# different graphics or colors / verschiedene Grafiken or colors
# show captured pieces / geschlagene Figuren zeigen
# freeplay / freie Züge
# limited time / begrenzte Zeit

black_color = pygame.Color(93, 50, 49)
white_color = pygame.Color(121, 72, 57)
default_black = black_color
default_white = white_color
select_color = pygame.Color(255, 247, 37)
possible_color = pygame.Color(80, 150, 15)
rook_loc = (0*15, 0, 15, 15)
knight_loc = (1*15, 0, 15, 15)
bishop_loc = (2*15, 0, 15, 15)
queen_loc = (3*15, 0, 15, 15)
king_loc = (4*15, 0, 15, 15)
pawn_loc = (5*15, 0, 15, 15)
# Classes
# Display
WIDTH = 640
HEIGHT = 690
manager = pygame_gui.UIManager((WIDTH, HEIGHT), pathdir + "/img/theme.json")
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")  # Set the initial caption
running = True
wh_bl = 0
current_player = "white"  # Variable to track the current player's turn
music = ["\\snd\\1.mp3","\\snd\\2.mp3","\\snd\\3.mp3"]
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 16)
config_file = "/saves/settings.config"

def save(data, file = "saves/save.dat"):
    f = open(pathdir + "/"+ file, "+a")
    f.writelines(data + "\n")
    f.close()

def quit():
    pygame.quit()
    sys.exit()


def write_config(line, insert):
    with open(pathdir + config_file, "r") as f:
        lines = f.readlines()
        lines[line] = insert + "\n"
        f.close()
    open(pathdir + config_file, 'w').close()
    with open(pathdir + config_file, 'w') as f:
        f.writelines(lines)
        f.close()

def read_config(line):
    with open(pathdir + config_file, "r") as f:
        lines = f.readlines()
        f.close()
        return lines[line]

QUITB = 0
NEWB = 1
LOADB = 2

REVERSEB = 0
EXITB = 1

QUEENB = 0
ROOKB = 1
KNIGHTB = 2
BISHOPB = 3
SELECTL = 4

menuBl = []
menuBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 50,HEIGHT - HEIGHT / 5 * 1 - 25),(100,50)),"Quit", manager, object_id= "#1"))
menuBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100,HEIGHT - HEIGHT / 5 * 4 - 25),(200,50)),"New Game", manager, object_id= "#1"))
menuBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100,HEIGHT - HEIGHT / 5 * 3 - 25),(200,50)),"Load Game", manager, object_id= "#1"))
menuBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100,HEIGHT - HEIGHT / 5 * 2 - 25),(200,50)),"Options", manager, object_id= "#1"))


gameBl = []
gameBl.append(pygame_gui.elements.UIButton(pygame.Rect((0,640),(WIDTH / 2,50)),"undo last move", manager, object_id= "#1"))
gameBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2,640),(WIDTH / 2,50)),"Exit to Main Menu", manager, object_id= "#1"))

promoBl = []
promoBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 2 - 25),(200, 50)),"Queen", manager, object_id= "#1"))
promoBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 3 - 25),(200, 50)),"Rook", manager, object_id= "#1"))
promoBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 4 - 25),(200, 50)),"Knight", manager, object_id= "#1"))
promoBl.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 5 - 25),(200, 50)),"Bishop", manager, object_id= "#1"))
promoBl.append(pygame_gui.elements.UILabel(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 1 - 35),(200, 100)), "Select to which piece"))
promoBl.append(pygame_gui.elements.UILabel(pygame.Rect((WIDTH / 2 - 100, 100  + 440 / 6 * 1 - 15),(200, 100)), "to promote to"))

optionsBL = []
optionsBL.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, HEIGHT - HEIGHT / 5 * 2 - 50),(200, 50)), "Toggle Debugmode", manager, object_id= "#1"))
optionsBL.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, HEIGHT - HEIGHT / 5 * 1 - 50),(200, 50)), "return to main Menu", manager, object_id= "#1"))
optionsBL.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, HEIGHT - HEIGHT / 5 * 3 - 50),(200, 50)), "Pick Color For Black Fields", manager, object_id= "#1"))
optionsBL.append(pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2 - 100, HEIGHT - HEIGHT / 5 * 4 - 50),(200, 50)), "Pick Color For White Fields", manager, object_id= "#1"))

for Button in menuBl + gameBl + promoBl:
    Button.hide()

Debug = True if read_config(0)[:-1] == "True" else False

class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        self.spritepath = os.path.join(pathdir, 'img', filename)
        try:
            self.sheet = pygame.image.load(self.spritepath).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    
sheetblack = SpriteSheet("pieces_black_1.png")
sheetwhite = SpriteSheet("pieces_white_1.png")

class Timer():
    def __init__(self, func):
        self.func = func
        self.running = False

class Board:
    fields = []

    def __init__(self, x, y, colorblack, width, height):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.piece = None
        self.index = len(Board.fields) - 1
        self.old_piece = None
        self.color = colorblack
        self.originalcolor = self.color

    def draw(self):

        
        if self.color == possible_color:
            pygame.draw.rect(wn, self.originalcolor, (self.x * 80, self.y * 80, self.width, self.height))
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(128)
            s.fill(possible_color)
            wn.blit(s, (self.x * 80, self.y * 80))
        else:
            pygame.draw.rect(wn, black_color if self.color == 0 else white_color, (self.x * 80, self.y * 80, self.width, self.height))

            
        if self.piece is not None:
            wn.blit(self.piece.get_sprite(), (self.x * 80 + 5, self.y * 80 + 5))  # Offset the pawn sprite position

        if Debug:
            surf = font.render(str(self.index), False, (0,0,0), (255,255,255))
            wn.blit(surf, (self.x * 80, self.y * 80))

    def get_xy(self):
        return self.x, self.y

    def get_pos(self):
        return self.y * 8 + self.x

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.old_piece = self.piece
        self.piece = piece

    def set_color(self,color):
        self.oldcolor = self.color
        self.color = color

    def reset_color(self):
        self.color = self.originalcolor

    def reset_piece(self):
        self.set_piece(self.old_piece)

class pieces:

    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.has_moved = False

    def __str__(self):
        print(f"ich bin auf dem feld {self.square} und ich bin {self.color}")

    def get_sprite(self):
        return self.sprite
    
    def get_king(self):
        for fig in Board.fields:
            fig = fig.get_piece()
            if isinstance(fig, king):
                if fig.color == self.color:
                    return fig
    
class pawn(pieces):

    def get_moves(self):
        moves = []
        direction = 1 if self.color == "black" else -1
        starting_row = 1 if self.color == "black" and self.square <= 15 else 6 if self.color == "white" and self.square >= 48 else 0

        # Check the square in front
        front_square = self.square + direction * 8
        if Board.fields[front_square].get_piece() is None:
            moves.append(front_square)

            # Check the square two steps ahead (only for pawns in starting position)
            if self.square // 8 == starting_row and Board.fields[self.square + direction * 16].get_piece() is None:
                moves.append(self.square + direction * 16)

        if direction == 1:
            # Check diagonally left
            if self.square % 8 != 7 :
                left_diagonal = self.square + direction * 9
                if Board.fields[left_diagonal].get_piece() is not None and Board.fields[left_diagonal].get_piece().color != self.color:
                    moves.append(left_diagonal)

            # Check diagonally right
            if self.square % 8 != 0:
                right_diagonal = self.square + direction * 7
                if Board.fields[right_diagonal].get_piece() is not None and Board.fields[right_diagonal].get_piece().color != self.color:
                    moves.append(right_diagonal)

        if direction == -1:
            # Check diagonally left
            if self.square % 8 != 0:
                left_diagonal = self.square + direction * 9
                if Board.fields[left_diagonal].get_piece() is not None and Board.fields[left_diagonal].get_piece().color != self.color:
                    moves.append(left_diagonal)

            # Check diagonally right
            if self.square % 8 != 7:
                right_diagonal = self.square + direction * 7
                if Board.fields[right_diagonal].get_piece() is not None and Board.fields[right_diagonal].get_piece().color != self.color:
                    moves.append(right_diagonal)

        return moves
    
        

    def set_square(self, square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(pawn(self.color, square))
        self.square = square  # Update the current pawn's square

    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(pawn_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(pawn_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite

class knight(pieces):

    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(knight_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(knight_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite

    def get_moves(self):
        moves = []
        directions = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
        for dx, dy in directions:
            new_x, new_y = self.square % 8 + dx, self.square // 8 + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                new_square = new_y * 8 + new_x
                if Board.fields[new_square].get_piece() is None or Board.fields[new_square].get_piece().color != self.color:
                    moves.append(new_square)
        return moves
    
    

    def set_square(self,square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(knight(self.color, square))
        self.square = square  # Update the current knight's square

class rook(pieces):

    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(rook_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(rook_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite
        self.has_moved = False



    def get_moves(self):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in directions:
            x, y = self.square % 8, self.square // 8
            for _ in range(1, 8):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    new_square = new_y * 8 + new_x
                    if Board.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Board.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
                        break
                    else:
                        break
                else:
                    break
                x, y = new_x, new_y
        return moves
    
    
    
    def set_square(self,square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(rook(self.color, square))
        self.square = square  # Update the current rook's square
        self.has_moved = True

class bishop(pieces):

    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(bishop_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(bishop_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite
        



    def get_moves(self):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            x, y = self.square % 8, self.square // 8
            for _ in range(1, 8):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    new_square = new_y * 8 + new_x
                    if Board.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Board.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
                        break
                    else:
                        break
                else:
                    break
                x, y = new_x, new_y
        return moves
    
    
    
    def set_square(self,square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(bishop(self.color, square))
        self.square = square  # Update the current bishop's square

class queen(pieces):
    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(queen_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(queen_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite
        

    def set_square(self,square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(queen(self.color, square))
        self.square = square  # Update the current queens's square


    
    def get_moves(self):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            x, y = self.square % 8, self.square // 8
            for _ in range(1, 8):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    new_square = new_y * 8 + new_x
                    if Board.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Board.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
                        break
                    else:
                        break
                else:
                    break
                x, y = new_x, new_y
        return moves
    
    
    
class king(pieces):

    def __init__(self, color, square):
        super().__init__(square, color)
        if color == "black":
            original_sprite = sheetblack.image_at(king_loc,colorkey =(0,0,0))
        else:
            original_sprite = sheetwhite.image_at(king_loc,colorkey =(0,0,0))
        resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
        self.sprite = resized_sprite
        self.sc_possible = False
        self.lc_possible = False
        self.has_moved = False

    def get_color(self):
        return self.color



    def set_square(self,square):
        Board.fields[self.square].set_piece(None)
        Board.fields[square].set_piece(king(self.color, square))

        if self.square + 2 == square:
            Board.fields[square + 1].get_piece().set_square(square - 1)
        elif self.square - 2 == square:
            Board.fields[square -2].get_piece().set_square(square + 1)
            
        self.square = square  # Update the current king's square
        self.has_moved = True

    def get_moves(self):

        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            new_x, new_y = self.square % 8 + dx, self.square // 8 + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                new_square = new_y * 8 + new_x
                piece = Board.fields[new_square].get_piece()
                if piece is None or Board.fields[new_square].get_piece().color != self.color and not isinstance(piece, king):
                    moves.append(new_square)

        # Castling
        if  not self.has_moved :
            # Short castling (kingside)
            ll = self.square + 2
            if ll < 63:
                if Board.fields[self.square + 1].get_piece() is None and Board.fields[self.square + 2].get_piece() is None:
                    piece = Board.fields[self.square + 3].get_piece()
                    if  piece is not None and isinstance(piece, rook) and not piece.has_moved:
                        moves.append(self.square + 2)
                        self.sc_possible = True

        # Long castling (queenside)
        if not self.has_moved :
            if Board.fields[self.square - 1].get_piece() is None and Board.fields[self.square - 2].get_piece() is None and Board.fields[self.square - 3].get_piece() is None:
                piece = Board.fields[self.square - 4].get_piece()
                if piece is not None and isinstance(piece, rook) and not piece.has_moved:
                    moves.append(self.square - 2)
                    self.lc_possible = True

        return moves
    
    def is_in_check(self, checksq = None):
        enemy_fields = []
        checksq = self.square if checksq == None else checksq
        for field in Board.fields:
            piece = field.get_piece()
            if piece != None and piece.color != self.color:
                enemy_fields.append(piece.get_moves())

        if enemy_fields is not None and  self.square in enemy_fields:        
            return True
        else:
            return False

# Draw Board
for y in range(8):
    for x in range(8):
        if wh_bl % 2 == 0:
            Board.fields.append(Board(x, y, False, 80, 80))  # Create black square
        else:
            Board.fields.append(Board(x, y, True, 80, 80))  # Create white square
        wh_bl = 1 - wh_bl
    wh_bl = 1 - wh_bl

def set_board_from_string(string):
    global current_player
    for sq in Board.fields:
        sq.set_piece(None)
    pos = 0
    color = None
    piece = None
    times = 0
    for i in range(len(string)):
        match string[i]:
            case "/":
                if times == 0:
                    times += 1
                for i in range(times):
                    if piece == "b":
                        Board.fields[pos].set_piece(pawn(color,pos))
                    if piece == "l":
                        Board.fields[pos].set_piece(bishop(color,pos))
                    if piece == "k":
                        Board.fields[pos].set_piece(knight(color,pos))
                    if piece == "d":
                        Board.fields[pos].set_piece(queen(color,pos))
                    if piece == "a":
                            Board.fields[pos].set_piece(king(color,pos))
                    if piece == "t":
                        Board.fields [pos].set_piece(rook(color,pos))
                    if piece == None:
                        pass
                    pos += 1
                times = 0
            case "t":
                piece = "t"
            case "b":
                piece = "b"
            case "l":
                piece = "l"
            case "k":
                piece = "k"
            case "d":
                piece = "d"
            case "a":
                piece = "a"
            case "e":
                piece = None
            case "w":
                color = "white"
            case "s":
                color = "black"
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                times = times * 10
                times += int(string[i])
            case "p":
                current_player = "white"
            case "P":
                current_player = "black"
            case "-":
                pass
            case _:
                raise Exception(f"unknown position: {string[i]}")

    for square in Board.fields:
        square.draw()

    pygame.display.flip()


def reverse():
    try:
        f = open(pathdir + "/saves/save.dat", "r")
        lines = f .readlines()
        f.close()
        del lines[-1]
        set_board_from_string(lines[-1][:-1])
        f = open(pathdir + "/saves/save.dat", "w")
        f.writelines(lines)
        f.close()
    except:
        open(pathdir + "/saves/save.dat", 'w').close()
        set_board_from_string(start_pos)

def check_legal(ban_sq_or_new_sq, color, mode = 0):
    if mode == 0:
        Board.fields[ban_sq_or_new_sq].set_piece(pawn(ban_sq_or_new_sq, color))
        if check_in_check(color):
            return False
        else:
            return True
    else:
        for f in Board.fields:
            figure = f.get_piece()
            if isinstance(figure, king):
                if figure.color == color:
                    return check_in_check(color, ban_sq_or_new_sq)

def check_in_check(color, new_square = None):
    for f in Board.fields:
        figure = f.get_piece()
        if isinstance(figure, king):
            if figure.color == color:
                return figure.is_in_check()
def new_game():
    open(pathdir + "/saves/save.dat", 'w').close()
    set_board_from_string(start_pos)
    
def load_game():
    try:
        f = open(pathdir + "/saves/save.dat", "r")
        save_pos = f.readlines()
        save_pos = save_pos[-1]
        f.close() 

        if save_pos == "":
            return False
        set_board_from_string(save_pos[:-1])
        return True
    except:
        return False

def getline(line):
    f = open(pathdir + "/saves/colors.config")
    lines = f.readlines()
    f.close()
    return lines[line]

def setline(line, text : str):
    f = open(pathdir + "/saves/colors.config", "r")
    lines = f.readlines()
    f.close()
    lines[line] = text
    open(pathdir + "/saves/colors.config", "w").close()
    f = open(pathdir + "/saves/colors.config", "w")
    f.writelines(lines)
    f.close()

def get_string_from_board():
    color = ""
    times = 0
    string = ""
    curr_piece = ""
    for square in Board.fields:
        piece = square.get_piece()
        if piece is not None:
            piececolor = "w" if piece.color == "white" else "s"
        if piece is None:
            if curr_piece == "e":
                curr_piece = "e"
                color = ""
                times += 1
            elif curr_piece != "e":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "e"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, pawn):
            if curr_piece == "b" and color == piececolor:
                times += 1
            elif curr_piece != "b" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "b"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, knight):
            if curr_piece == "k" and color == piececolor:
                curr_piece = "k"
                times += 1
            elif curr_piece != "k" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "k"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, bishop):
            if curr_piece == "l" and color == piececolor:
                curr_piece = "l"
                times += 1
            elif curr_piece != "l" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "l"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, rook):
            if curr_piece == "t" and color == piececolor:
                curr_piece = "t"
                times += 1
            elif curr_piece != "t" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "t"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times} color: {color}")
        elif isinstance(piece, queen):
            if curr_piece == "d" and color == piececolor:
                curr_piece = "d"
                times += 1
            elif curr_piece != "d" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "d" 
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, king):
            if curr_piece == "a" and color == piececolor:
                curr_piece = "a"
                times += 1
            elif curr_piece != "a" or color != piececolor:
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "a" 
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
    string += f"{curr_piece}{color}{'' if times == 1 else times}/"
    string += f"{'P' if current_player == 'black' else 'p'}"
    return string[2:]

def titleScreen():
    for button in menuBl:
        button.show()
    for button in gameBl + promoBl + optionsBL:
        button.hide()

    while True:
        wn.fill((65,65,67))
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == menuBl[0]:
                    quit()
                elif event.ui_element == menuBl[1]:
                    new_game()
                    multi()
                elif event.ui_element == menuBl[2]:
                    if load_game():
                        multi()
                elif event.ui_element == menuBl[3]:
                    options()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(wn)
        pygame.display.flip()

def options():
    global black_color
    global Debug
    for button in optionsBL:
        button.show()
    for button in gameBl + promoBl + menuBl:
        button.hide()

    while True:
        wn.fill((65,65,67))
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == optionsBL[0]:
                    Debug = False if Debug else True
                    write_config(0, str(Debug))
                elif event.ui_element == optionsBL[1]:
                    titleScreen()
                elif event.ui_element == optionsBL[2]:
                    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),manager, initial_colour=black_color, window_title="Change Black Colour", object_id= "#2")
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    black_colour = event.colour

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(wn)
        pygame.display.flip()

def promotion(square, color):

    time_delta = clock.tick(60)/1000.0


    pygame.draw.rect(wn, (0,0,0), pygame.Rect((100,100),(440,440)), 10, 12)
    pygame.draw.rect(wn, (64,66,64), pygame.Rect((110,110),(420,420)))


    for bttn in promoBl + gameBl + optionsBL:
        bttn.show()
    for bttn in menuBl:
        bttn.hide()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == promoBl[QUEENB]:
                    Board.fields[square].set_piece(queen(color, square))
                    multi()
                elif event.ui_element == promoBl[ROOKB]:
                    Board.fields[square].set_piece(rook(color, square))
                    multi()
                elif event.ui_element == promoBl[KNIGHTB]:
                    Board.fields[square].set_piece(knight(color, square))
                    multi()
                elif event.ui_element == promoBl[BISHOPB]:
                    Board.fields[square].set_piece(bishop(color, square))
                    multi()
                elif event.ui_element == gameBl[REVERSEB]:
                    reverse()
                    multi()
                elif event.ui_element == gameBl[EXITB]:
                    titleScreen()
                    
            manager.process_events(event)

        manager.draw_ui(wn)
        manager.update(time_delta)

        pygame.display.flip()

def multi():
    global current_player

    for button in menuBl + promoBl + optionsBL:
        button.hide()
    for button in gameBl:
        button.show()

    pygame.key.set_repeat(1000, 500)
    running = True
    storage = None
    oldsquare = 0
    square = 0
    while running:
        time_delta = clock.tick(60)/1000.0
        for field in Board.fields:
            field.draw()
        pygame.draw.rect(wn, (64,66,64), pygame.Rect(0, 640, 640, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_LCTRL] and key[pygame.K_z]:
                    reverse()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                buttons = pygame.mouse.get_pressed(num_buttons=5)

                # Left click
                if not buttons[0]:
                    continue

                x = mousepos[0] // 80  # Calculate the column of the clicked square
                y = mousepos[1] // 80  # Calculate the row of the clicked square
                xy = (x, y)

                for square in range(64):
                    xypos = Board.fields[square].get_xy()

                    if xypos != xy:
                        continue

                    clicked_piece = Board.fields[square].get_piece()

                    if storage is None and clicked_piece is not None and clicked_piece.color == current_player:
                        # select
                        storage = clicked_piece
                        Board.fields[square].set_color(select_color)
                        oldsquare = square
                        
                        for square in clicked_piece.get_moves():
                            Board.fields[square].set_color(possible_color)
                    elif storage is not None:
                        if clicked_piece is None and square in storage.get_moves():
                            # move
                            storage.set_square(square)
                            Board.fields[oldsquare].set_piece(None)
                            storage = None
                            current_player = "black" if current_player == "white" else "white"
                            for square in Board.fields:
                                square.reset_color()
                            save(get_string_from_board())
                        elif clicked_piece is not None and clicked_piece.color != current_player and square in storage.get_moves():
                            # attack
                            storage.set_square(square)
                            Board.fields[oldsquare].set_piece(None)
                            storage = None
                            current_player = "black" if current_player == "white" else "white"
                            for square in Board.fields:
                                square.reset_color()
                            #pygame.mixer.music.load(pathdir +'\\..\\'+ music[random.randint(0, 2)])
                            #pygame.mixer.music.play()
                            save(get_string_from_board())
                        elif clicked_piece is not None and clicked_piece.color == current_player:
                            # select
                            storage = clicked_piece
                            oldsquare = square
                            for sq in Board.fields:
                                sq.reset_color()
                            for sq in clicked_piece.get_moves():
                                Board.fields[sq].set_color(possible_color)
                            Board.fields[square].set_color(select_color)
                        else:
                            # illegal move, reset selection
                            storage = None
                            for square in Board.fields:
                                square.reset_color()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gameBl[0]:
                    reverse()
                elif event.ui_element == gameBl[1]:
                    running = False

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(wn)
        pygame.display.flip()

        caption = f'chess ({current_player}\'s turn)'

        white_king_found = False
        black_king_found = False

        for sq in Board.fields:
            f = sq.get_piece()
            if isinstance(f, king):
                if f.color == "white":
                    white_king_found = True
                    if f.is_in_check():
                        caption = "white is in check"
                if f.color == "black":
                    black_king_found = True
                    if f.is_in_check():
                        caption = "black is in check"

            if isinstance(f, pawn):
                if f.color == "white" and f.square // 8 == 0:
                    promotion(f.square, "white")
                elif f.color == "black" and f.square // 8 == 7:
                    promotion(f.square, "black")

        pygame.display.set_caption(caption)

        if not black_king_found:
            pygame.display.set_caption("white won! congrats to white! (game made by noschXL)")
            time.sleep(5)
            running = False


        if not white_king_found:
            pygame.display.set_caption("black won! congrats to black! (game made by noschXL)")  
            time.sleep(5)
            running = False
    titleScreen()

titleScreen()