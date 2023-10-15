# Piece class for chess
from square import *
from Spritesheet import *
import pygame
 

sheetwhite = SpriteSheet("pieces_white_1.png")
sheetblack = SpriteSheet("pieces_black_1.png")

rook_loc = (0*15, 0, 15, 15)
knight_loc = (1*15, 0, 15, 15)
bishop_loc = (2*15, 0, 15, 15)
queen_loc = (3*15, 0, 15, 15)
king_loc = (4*15, 0, 15, 15)
pawn_loc = (5*15, 0, 15, 15)

current_player = "white"
class Piece:


    def update():
        current_player = "white" if current_player == "black" else "black"

    class pawn:
        pawns = []

        def set_square(self, square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.pawn(self.color, square))
            self.square = square  # Update the current pawn's square

        def get_moves(self):
            moves = []
            if self.color == "black":
                if self.square + 8 < 64:
                    if squares.fields[self.square + 8].get_piece() is None:
                        moves.append(self.square + 8)
                        if self.square <= 15 and squares.fields[self.square + 16].get_piece() is None:
                            moves.append(self.square + 16)
                    if self.square % 8 != 0 and squares.fields[self.square + 7].get_piece() is not None:
                        moves.append(self.square + 7)
                    if self.square % 8 != 7 and squares.fields[self.square + 9].get_piece() is not None:
                        moves.append(self.square + 9)
            else:
                if self.square - 8 >= 0:
                    if squares.fields[self.square - 8].get_piece() is None:
                        moves.append(self.square - 8)
                        if self.square >= 48 and squares.fields[self.square - 16].get_piece() is None:
                            moves.append(self.square - 16)
                    if self.square % 8 != 0 and squares.fields[self.square - 9].get_piece() is not None:
                        moves.append(self.square - 9)
                    if self.square % 8 != 7 and squares.fields[self.square - 7].get_piece() is not None:
                        moves.append(self.square - 7) 

            return moves

        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(pawn_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(pawn_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color

        def get_sprite(self):
            return self.sprite
        
    class knight:

        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(knight_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(knight_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color

        def get_sprite(self):
            return self.sprite

        def get_moves(self):
            moves = []
            directions = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
            for dx, dy in directions:
                new_x, new_y = self.square % 8 + dx, self.square // 8 + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    new_square = new_y * 8 + new_x
                    if squares.fields[new_square].get_piece() is None or squares.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)
            return moves
        
        def set_square(self,square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.knight(self.color, square))
            self.square = square  # Update the current knight's square

    class rook:

        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(rook_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(rook_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color
            self.has_moved = False

        def get_sprite(self):
            return self.sprite

        def get_moves(self):
            moves = []
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dx, dy in directions:
                x, y = self.square % 8, self.square // 8
                for _ in range(1, 8):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        new_square = new_y * 8 + new_x
                        if squares.fields[new_square].get_piece() is None:
                            moves.append(new_square)
                        elif squares.fields[new_square].get_piece().color != self.color:
                            moves.append(new_square)
                            break
                        else:
                            break
                    else:
                        break
                    x, y = new_x, new_y
            return moves
        
        def set_square(self,square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.rook(self.color, square))
            self.square = square  # Update the current rook's square
            self.has_moved = True

    class bishop:

        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(bishop_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(bishop_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color

        def get_sprite(self):
            return self.sprite

        def get_moves(self):
            moves = []
            directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                x, y = self.square % 8, self.square // 8
                for _ in range(1, 8):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        new_square = new_y * 8 + new_x
                        if squares.fields[new_square].get_piece() is None:
                            moves.append(new_square)
                        elif squares.fields[new_square].get_piece().color != self.color:
                            moves.append(new_square)
                            break
                        else:
                            break
                    else:
                        break
                    x, y = new_x, new_y
            return moves
        
        def set_square(self,square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.bishop(self.color, square))
            self.square = square  # Update the current bishop's square

    class queen():
        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(queen_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(queen_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color

        def set_square(self,square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.queen(self.color, square))
            self.square = square  # Update the current queens's square

        def get_sprite(self):
            return self.sprite
        
        def get_moves(self):
            moves = []
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                x, y = self.square % 8, self.square // 8
                for _ in range(1, 8):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        new_square = new_y * 8 + new_x
                        if squares.fields[new_square].get_piece() is None:
                            moves.append(new_square)
                        elif squares.fields[new_square].get_piece().color != self.color:
                            moves.append(new_square)
                            break
                        else:
                            break
                    else:
                        break
                    x, y = new_x, new_y
            return moves
        
    class king:

        def __init__(self, color, square):
            if color == "black":
                original_sprite = sheetblack.image_at(king_loc,colorkey =(0,0,0))
            else:
                original_sprite = sheetwhite.image_at(king_loc,colorkey =(0,0,0))
            resized_sprite = pygame.transform.scale(original_sprite, (70, 70))
            self.sprite = resized_sprite
            self.square = square
            self.color = color
            self.has_moved = False

        def get_color(self):
            return self.color

        def get_sprite(self):
            return self.sprite

        def set_square(self,square):
            squares.fields[self.square].set_piece(None)
            squares.fields[square].set_piece(Piece.king(self.color, square))
            if self.square + 2 == square:
                squares.fields[square + 1].get_piece().set_square(square - 1)
            elif self.square - 2 == square:
                squares.fields[square -2].get_piece().set_square(square + 1)
                
            self.square = square  # Update the current king's square
            self.has_moved = True

        def get_moves(self):

            moves = []
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = self.square % 8 + dx, self.square // 8 + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    new_square = new_y * 8 + new_x
                    if squares.fields[new_square].get_piece() is None or squares.fields[new_square].get_piece().color != self.color:
                        moves.append(new_square)

            # Castling
            if  not self.has_moved:
                # Short castling (kingside)
                ll = self.square + 2
                if ll < 63:
                    if squares.fields[self.square + 1].get_piece() is None and squares.fields[self.square + 2].get_piece() is None:
                        rook = squares.fields[self.square + 3].get_piece()
                        if isinstance(rook, Piece.rook) and not rook.has_moved:
                            moves.append(self.square + 2)

            # Long castling (queenside)
            if not self.has_moved:
                if squares.fields[self.square - 1].get_piece() is None and squares.fields[self.square - 2].get_piece() is None and squares.fields[self.square - 3].get_piece() is None:
                    rook = squares.fields[self.square - 4].get_piece()
                    if isinstance(rook, Piece.rook) and not rook.has_moved:
                        moves.append(self.square - 2)
            return moves

        def is_in_check(self, checksq = None):
            for field in squares.fields:
                piece = field.get_piece()
                if piece != None and piece.color != current_player:
                    for sq in piece.get_moves():
                        checking_square = self.square if checksq == None else checksq == sq
                        if checking_square == sq:
                            return True
                        
            return False
