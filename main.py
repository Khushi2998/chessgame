import pygame
from pieces import Piece
from rules import valid_move
from check import (
    is_check,
    copy_board,
    is_checkmate
)

pygame.init()


WIDTH = 640
HEIGHT = 640

SIZE = WIDTH // 8


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Chess Game"
)


font = pygame.font.SysFont(
    "segoeuisymbol",
    55
)


# create pieces

board = [[None for x in range(8)] for y in range(8)]


# black pieces

board[0] = [
    Piece("rook","black"),
    Piece("knight","black"),
    Piece("bishop","black"),
    Piece("queen","black"),
    Piece("king","black"),
    Piece("bishop","black"),
    Piece("knight","black"),
    Piece("rook","black")
]


for i in range(8):
    board[1][i] = Piece("pawn","black")



# white pieces

board[7] = [
    Piece("rook","white"),
    Piece("knight","white"),
    Piece("bishop","white"),
    Piece("queen","white"),
    Piece("king","white"),
    Piece("bishop","white"),
    Piece("knight","white"),
    Piece("rook","white")
]


for i in range(8):
    board[6][i] = Piece("pawn","white")





def draw_board():

    colors=[
        (240,217,181),
        (181,136,99)
    ]


    for row in range(8):

        for col in range(8):

            color = colors[
                (row+col)%2
            ]
            if selected == (row,col):
             color = (100,200,100)


            pygame.draw.rect(
                screen,
                color,
                (
                    col*SIZE,
                    row*SIZE,
                    SIZE,
                    SIZE
                )
            )


            piece = board[row][col]


            if piece:

                text = font.render(
                    piece.symbol(),
                    True,
                    (0,0,0)
                )


                screen.blit(
                    text,
                    (
                     col*SIZE+20,
                     row*SIZE+15
                    )
                )





selected = None

turn = "white"
game_over = False
winner = ""
promotion = False
promotion_piece = None
promotion_color = None
running=True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and promotion:

            x,y = pygame.mouse.get_pos()


            choice = (y-220)//55


            pieces = [
                "queen",
                "rook",
                "bishop",
                "knight"
            ]


            if 0 <= choice < 4:


                # find pawn waiting for promotion

                for r in range(8):

                    for c in range(8):

                        piece = board[r][c]


                        if (
                            piece
                            and piece.name == "pawn"
                            and piece.color == promotion_color
                        ):

                            piece.name = pieces[choice]


                promotion = False
        if (event.type == pygame.MOUSEBUTTONDOWN
            and not game_over
            and not promotion):

            x, y = pygame.mouse.get_pos()

            row = y // SIZE
            col = x // SIZE


            # FIRST CLICK
            if selected is None:

                piece = board[row][col]


                if piece and piece.color == turn:

                    selected = (row,col)



            # SECOND CLICK
            else:

                old_row, old_col = selected

                selected_piece = board[old_row][old_col]


                # clicked same square
                if (row,col) == selected:

                    selected = None



                else:


                    # legal movement check

                    if valid_move(
                        board,
                        selected,
                        (row,col)
                    ):


                        # temporary board

                        temp_board = copy_board(board)


                        temp_piece = temp_board[old_row][old_col]


                        # simulate move

                        temp_board[row][col] = temp_piece

                        temp_board[old_row][old_col] = None



                        # king safety

                        if is_check(
                            temp_board,
                            turn
                        ):


                            print(
                                "Illegal move! King is in danger"
                            )


                        else:


                            # REAL MOVE

                            board[row][col] = selected_piece

                            board[old_row][old_col] = None



                            selected_piece.moved = True
                            # promotion check

                            if selected_piece.name == "pawn":


                                if selected_piece.color == "white" and row == 0:

                                    promotion = True

                                    promotion_color = "white"



                                elif selected_piece.color == "black" and row == 7:

                                    promotion = True

                                    promotion_color = "black"   


                            # switch turn ONCE

                            if turn == "white":

                                turn = "black"

                            else:

                                turn = "white"

                            if is_checkmate(board,turn):

                                game_over = True

                                if turn == "white":

                                    winner = "Black Wins!"

                                else:

                                    winner = "White Wins!"

                            elif is_check(board, turn):

                                print(
                                    turn,
                                    "is in CHECK"
                                )


                    selected = None



    def draw_promotion():

        pygame.draw.rect(
        screen,
        (220,220,220),
        (220,200,200,250)
    )


    options = [
        "Queen",
        "Rook",
        "Bishop",
        "Knight"
    ]


    for i, option in enumerate(options):

        text = font.render(
            option,
            True,
            (0,0,0)
        )

        screen.blit(
            text,
            (
                250,
                220 + i*55
            )
        )
    draw_board()

    if promotion:

        draw_promotion(promotion_color)

    # show winner screen
    if game_over:

        text = font.render(
            winner,
            True,
            (255,0,0)
        )

        screen.blit(
            text,
            (
                200,
                300
            )
        )


    pygame.display.update()



pygame.quit()