import pygame
import os
import time
import sys
import random
# Load pygame
pygame.init()
pygame.mixer.init()

select_color = pygame.Color(255, 247, 37)
rook_loc = (0*15, 0, 15, 15)
knight_loc = (1*15, 0, 15, 15)
bishop_loc = (2*15, 0, 15, 15)
queen_loc = (3*15, 0, 15, 15)
king_loc = (4*15, 0, 15, 15)
pawn_loc = (5*15, 0, 15, 15)
# Classes
# Display
WIDTH = 640
HEIGHT = 640
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess (whites turn)")  # Set the initial caption
running = True
wh_bl = 0
current_player = "white"  # Variable to track the current player's turn

music = ["\snd\\1.mp3","\snd\\2.mp3","\snd\\3.mp3"]

pathdir = os.path.abspath(__file__)

start_pos = "ts/ks/ls/ds/as/ls/ks/ts/bs8/e32/bw8/tw/kw/lw/dw/aw/lw/kw/tw/" # b = pawn, t = rook, k = knight, l = bishop, d = queen, a = king, e = empty, w = white, s = black


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        self.spritepath = os.path.join(pathdir,'..','img',filename)
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

class Square:
    fields = []

    def __init__(self, x, y, colorblack, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.piece = None
        if colorblack:
            self.color = pygame.Color(93, 50, 49)  # Color for black Square
        else:
            self.color = pygame.Color(121, 72, 57, 255)  # Color for white Square
        self.originalcolor = self.color

    def draw(self):
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

    def __str__(self):
        print(f"ich bin auf dem feld {self.square} und ich bin {self.color}")

    def set_square(self, square):
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(pawn(self.color, square))
        self.square = square  # Update the current pawn's square

    def get_sprite(self):
        return self.sprite
class pawn(pieces):

    def get_moves(self):
        moves = []
        direction = 1 if self.color == "black" else -1
        starting_row = 1 if self.color == "black" and self.square <= 15 else 6 if self.color == "white" and self.square >= 48 else 0

        # Check the square in front
        front_square = self.square + direction * 8
        if Square.fields[front_square].get_piece() is None:
            moves.append(front_square)

            # Check the square two steps ahead (only for pawns in starting position)
            if self.square // 8 == starting_row and Square.fields[self.square + direction * 16].get_piece() is None:
                moves.append(self.square + direction * 16)

        # Check diagonally left
        if self.square % 8 != 0:
            left_diagonal = self.square + direction * 7
            if Square.fields[left_diagonal].get_piece() is not None:
                moves.append(left_diagonal)

        # Check diagonally right
        if self.square % 8 != 7:
            right_diagonal = self.square + direction * 9
            if Square.fields[right_diagonal].get_piece() is not None:
                moves.append(right_diagonal)

        return moves


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
                if Square.fields[new_square].get_piece() is None or Square.fields[new_square].get_piece().color != self.color:
                    moves.append(new_square)
        return moves
    
    def set_square(self,square):
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(knight(self.color, square))
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
                    if Square.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Square.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
                        break
                    else:
                        break
                else:
                    break
                x, y = new_x, new_y
        return moves
    
    def set_square(self,square):
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(rook(self.color, square))
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
                    if Square.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Square.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
                        break
                    else:
                        break
                else:
                    break
                x, y = new_x, new_y
        return moves
    
    def set_square(self,square):
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(bishop(self.color, square))
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
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(queen(self.color, square))
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
                    if Square.fields[new_square].get_piece() is None:
                        moves.append(new_square)
                    elif Square.fields[new_square].get_piece().color != self.color:
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
        
        self.has_moved = False

    def get_color(self):
        return self.color



    def set_square(self,square):
        Square.fields[self.square].set_piece(None)
        Square.fields[square].set_piece(king(self.color, square))
        if self.square + 2 == square:
            Square.fields[square + 1].get_piece().set_square(square - 1)
        elif self.square - 2 == square:
            Square.fields[square -2].get_piece().set_square(square + 1)
            
        self.square = square  # Update the current king's square
        self.has_moved = True

    def get_moves(self):

        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            new_x, new_y = self.square % 8 + dx, self.square // 8 + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                new_square = new_y * 8 + new_x
                if Square.fields[new_square].get_piece() is None or Square.fields[new_square].get_piece().color != self.color:
                    moves.append(new_square)

        # Castling
        if  not self.has_moved:
            # Short castling (kingside)
            ll = self.square + 2
            if ll < 63:
                if Square.fields[self.square + 1].get_piece() is None and Square.fields[self.square + 2].get_piece() is None:
                    piece = Square.fields[self.square + 3].get_piece()
                    if  piece is not None and isinstance(piece, rook) and not rook.has_moved:
                        moves.append(self.square + 2)

        # Long castling (queenside)
        if not self.has_moved:
            if Square.fields[self.square - 1].get_piece() is None and Square.fields[self.square - 2].get_piece() is None and Square.fields[self.square - 3].get_piece() is None:
                piece = Square.fields[self.square - 4].get_piece()
                if piece is not None and isinstance(piece, rook) and not rook.has_moved:
                    moves.append(self.square - 2)
        return moves

    def is_in_check(self, checksq = None):
        for field in Square.fields:
            piece = field.get_piece()
            if piece != None and piece.color != current_player:
                for sq in piece.get_moves():
                    checking_square = self.square if checksq == None else checksq == sq
                    if checking_square == sq:
                        return True
                    
        return False

# Draw Square
for y in range(8):
    for x in range(8):
        if wh_bl % 2 == 0:
            Square.fields.append(Square(x, y, False, 80, 80))  # Create black square
        else:
            Square.fields.append(Square(x, y, True, 80, 80))  # Create white square
        wh_bl = 1 - wh_bl
    wh_bl = 1 - wh_bl

def set_board_from_string(string):
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
                        Square.fields[pos].set_piece(pawn(color,pos))
                    if piece == "l":
                        Square.fields[pos].set_piece(bishop(color,pos))
                    if piece == "k":
                        Square.fields[pos].set_piece(knight(color,pos))
                    if piece == "d":
                        Square.fields[pos].set_piece(queen(color,pos))
                    if piece == "a":
                            Square.fields[pos].set_piece(king(color,pos))
                    if piece == "t":
                        Square.fields [pos].set_piece(rook(color,pos))
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
            case _:
                print(string[i])
                print("ungültige position")
                pygame.quit()
                sys.exit()

    for square in Square.fields:
        square.draw()

    pygame.display.flip()

set_board_from_string(start_pos)

def get_string_from_board():
    color = ""
    times = 0
    string = ""
    curr_piece = ""
    for square in Square.fields:
        piece = square.get_piece()
        if piece is None:
            if curr_piece == "e":
                curr_piece = "e"
                color = ""
                times += 1
            elif curr_piece != "e":
                string += f"{curr_piece}{'' if times == 1 else times}/"
                curr_piece = "e"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, pawn):
            if curr_piece == "b" or curr_piece == "":
                curr_piece = "b"
                times += 1
            elif curr_piece != "b":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "b"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, knight):
            if curr_piece == "k":
                curr_piece = "k"
                times += 1
            elif curr_piece != "k":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "k"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, bishop):
            if curr_piece == "l" :
                curr_piece = "l"
                times += 1
            elif curr_piece != "l":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "l"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, rook):
            if curr_piece == "t" :
                curr_piece = "t"
                times += 1
            elif curr_piece != "t":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "t"
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, queen):
            if curr_piece == "d" :
                curr_piece = "d"
                times += 1
            elif curr_piece != "d":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "d" 
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
        elif isinstance(piece, king):
            if curr_piece == "a" :
                curr_piece = "a"
                times += 1
            elif curr_piece != "a":
                string += f"{curr_piece}{color}{'' if times == 1 else times}/"
                curr_piece = "a" 
                color = "w" if piece.color == "white" else "s"
                times = 1
            else:
                print(f"curr_piece: {curr_piece} times: {times}")
    string += f"{curr_piece}{color}{'' if times == 1 else times}/"
    return string


storage = None
oldsquare = 0
square = 0
while running:
    for field in Square.fields:
        field.draw()
        
    pygame.key.set_repeat()
    key = pygame.key.get_pressed()
    if key[pygame.K_g]:
        print(get_string_from_board())

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
                xypos = Square.fields[square].get_xy()

                if xypos != xy:
                    continue

                clicked_piece = Square.fields[square].get_piece()

                if storage is None and clicked_piece is not None and clicked_piece.color == current_player:
                    # select
                    storage = clicked_piece
                    Square.fields[square].set_color(select_color)
                    oldsquare = square
                elif storage is not None:
                    if clicked_piece is None and square in storage.get_moves():
                        # move
                        storage.set_square(square)
                        Square.fields[oldsquare].set_piece(None)
                        storage = None
                        current_player = "black" if current_player == "white" else "white"
                        Square.fields[oldsquare].reset_color()
                    elif clicked_piece is not None and clicked_piece.color != current_player and square in storage.get_moves():
                        # attack
                        storage.set_square(square)
                        Square.fields[oldsquare].set_piece(None)
                        storage = None
                        current_player = "black" if current_player == "white" else "white"
                        Square.fields[oldsquare].reset_color()
                        pygame.mixer.music.load(pathdir +'\\..\\'+ music[random.randint(0, 2)])
                        pygame.mixer.music.play()
                    elif clicked_piece is not None and clicked_piece.color == current_player:
                        # select
                        storage = clicked_piece
                        Square.fields[oldsquare].reset_color()
                        Square.fields[square].set_color(select_color)
                        oldsquare = square
                    else:
                        # illegal move, reset selection
                        storage = None
                        Square.fields[oldsquare].reset_color()

    pygame.display.flip()

    caption = f'chess ({current_player}\'s turn)'

    white_king_found = False
    black_king_found = False

    for f in Square.fields:
        figure = f.get_piece()
        if isinstance(figure, king):
            if figure.color == "white":
                white_king_found = True
                if figure.is_in_check():
                    caption = "white is in check"
            else:
                black_king_found = True
                if figure.is_in_check():
                    caption = "black is in check"

            
    for i in range(64):
        xy = Square.fields[i].get_xy()
        if figure != None:
            if xy[1] == 7 and figure.color == "black" and isinstance(figure, pawn):
                #print(f"xy: {xy} figure.color: {figure.color} isinstance: {isinstance(figure, pawn)}")
                checking = False
                #caption = "waiting for input(1 = queen,2 = rook,p 3 = bishop, 4 = knight)"

                while checking:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_1]:
                        square.set_piece(queen("black",Square.fields[i]))
                        checking = False
                    elif keys[pygame.K_2]:
                        square.set_piece(rook("black",Square.fields[i]))
                        checking = False
                    elif keys[pygame.K_3]:
                        square.set_piece(bishop("black",Square.fields[i]))
                        checking = False
                    elif keys[pygame.K_1]:
                        square.set_piece(knight("black",Square.fields[i]))
                        checking = False

    
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