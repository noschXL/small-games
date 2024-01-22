import pygame
import pygame_gui
import os
import time
import sys
import tkinter
from tkinter import messagebox
# Load pygame
pygame.init()
pygame.mixer.init()

pathdir = os.path.dirname(os.path.abspath(__file__))

start_pos = "ts/ks/ls/ds/as/ls/ks/ts/bs8/e32/bw8/tw/kw/lw/dw/aw/lw/kw/tw/" # b = pawn, t = rook, k = knight, l = bishop, d = queen, a = king, e = empty, w = white, s = black

open(pathdir + "/save.dat", "a").close()


def save(pos):
    open(pathdir + "/save.dat", 'w').close()
    f = open(pathdir + "/save.dat", "+a")
    f.write(pos)
    f.close


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
pygame.display.set_caption("chess (whites turn)")  # Set the initial caption
running = True
wh_bl = 0
current_player = "white"  # Variable to track the current player's turn
music = ["\snd\\1.mp3","\snd\\2.mp3","\snd\\3.mp3"]
clock = pygame.time.Clock()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

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
        if colorblack:
            self.color = pygame.Color(93, 50, 49)  # Color for black Board
        else:
            self.color = pygame.Color(121, 72, 57, 255)  # Color for white Board
        self.originalcolor = self.color

    def draw(self):
        
        if self.color == possible_color:
            pygame.draw.rect(wn, self.originalcolor, (self.x * 80, self.y * 80, self.width, self.height))
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(128)
            s.fill(possible_color)
            wn.blit(s, (self.x * 80, self.y * 80))
        else:
            pygame.draw.rect(wn, self.color, (self.x * 80, self.y * 80, self.width, self.height))

            
        if self.piece is not None:
            wn.blit(self.piece.get_sprite(), (self.x * 80 + 5, self.y * 80 + 5))  # Offset the pawn sprite position

    def get_xy(self):
        return self.x, self.y

    def get_pos(self):
        return self.y * 8 + self.x

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def set_color(self,color):
        self.oldcolor = self.color
        self.color = color

    def reset_color(self):
        self.color = self.originalcolor

class pieces:

    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.has_moved = False

    def __str__(self):
        print(f"ich bin auf dem feld {self.square} und ich bin {self.color}")

    def get_sprite(self):
        return self.sprite
    
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

        # Check diagonally left
        if self.square % 8 != 0:
            left_diagonal = self.square + direction * 7
            if Board.fields[left_diagonal].get_piece() is not None:
                moves.append(left_diagonal)

        # Check diagonally right
        if self.square % 8 != 7:
            right_diagonal = self.square + direction * 9
            if Board.fields[right_diagonal].get_piece() is not None:
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
        
        if self.is_in_check(self.square):
            if self.sc_possible:
                moves.remove(self.square + 2)
            if self.lc_possible:
                moves.remove(self.square - 2)
        return moves

    def is_in_check(self, checksq = None):
        checksq = self.square if checksq == None else checksq
        for field in Board.fields:
            piece = field.get_piece()
            if isinstance(piece, king):
                continue
            if piece != None and piece.color != self.color:
                if checksq in piece.get_moves():
                    return True
                    
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
    global destroyed
    set_board_from_string(start_pos)
    top.destroy()
    destroyed = True
    
def load_game():
    global destroyed
    try:
        f = open(pathdir + "/save.dat", "r")
        save_pos = f.read()
        f.close()

        if save_pos == "":
            raise Exception("empty save")
        set_board_from_string(save_pos)
        top.destroy()
        destroyed = True
    except Exception as e:
        messagebox.showinfo("Couldn't load", e)
destroyed = False
top = tkinter.Tk(className= "Chess")
top.geometry("200x200")
B1 = tkinter.Button(top, text= "New Game", command= new_game)
B1.place(x=50,y=50)
B2 = tkinter.Button(top, text= "Load Game", command= load_game)
B2.place(x = 50, y = 125)
label1 = tkinter.Label(top, text = "press 'S' in an Game")
label1.place(x=25,y = 150)
label2 = tkinter.Label(top, text = "to save")
label2.place(x=65,y = 175)
top.mainloop()

if top.state != 'normal' and not destroyed:
        pygame.quit()
        sys.exit()

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

pygame.key.set_repeat(1000, 500 )
storage = None
oldsquare = 0
square = 0
hello_button = pygame_gui.elements.UIButton(pygame.Rect((0,640),(100,50)),"Save", manager, object_id= "#1")
while running:
    time_delta = clock.tick(60)/1000.0
    for field in Board.fields:
        field.draw()
    pygame.draw.rect(wn, (64,66,64), pygame.Rect(0, 640, 640, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            if event.ui_element == hello_button:
                save(get_string_from_board())
                msg=messagebox.showinfo("Chess","Game Saved")

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
    
    pygame.display.set_caption(caption)

    if not black_king_found:
        pygame.display.set_caption("white won! congrats to white! (game made by noschXL)")
        time.sleep(5)
        running = False

 
    if not white_king_found:
        pygame.display.set_caption("black won! congrats to black! (game made by noschXL)")  
        time.sleep(5)
        running = False


pygame.quit()
sys.exit()