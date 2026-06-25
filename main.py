import pygame
from pieces import Piece
from rules import valid_move,can_castle
from check import (
    is_check,
    copy_board,
    is_checkmate,
    has_any_legal_move,
    insufficient_material
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

result_font = pygame.font.SysFont(
    "arial",
    35
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


def draw_promotion():

    # dark transparent background
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(130)
    overlay.fill((0,0,0))
    screen.blit(overlay,(0,0))


    # popup
    popup = pygame.Rect(
        170,
        130,
        300,
        400
    )

    pygame.draw.rect(
        screen,
        (245,245,245),
        popup,
        border_radius=20
    )


    title_font = pygame.font.SysFont(
        "arial",
        32
    )

    button_font = pygame.font.SysFont(
        "arial",
        25
    )


    title = title_font.render(
        "Promote Pawn",
        True,
        (0,0,0)
    )


    screen.blit(
        title,
        (
            220,
            160
        )
    )


    options = [
        ("Queen","queen"),
        ("Rook","rook"),
        ("Bishop","bishop"),
        ("Knight","knight")
    ]


    for i,(label,piece) in enumerate(options):

        button = pygame.Rect(
            220,
            220+i*60,
            200,
            45
        )


        pygame.draw.rect(
            screen,
            (210,210,210),
            button,
            border_radius=12
        )


        text = button_font.render(
            label,
            True,
            (0,0,0)
        )


        screen.blit(
            text,
            (
                button.x+55,
                button.y+10
            )
        )


selected = None

turn = "white"
game_over = False
winner = ""
draw = False
draw_reason = ""
promotion = False
promotion_piece = None
promotion_color = None
promotion_position = None
running=True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and promotion:

            x, y = pygame.mouse.get_pos()


            choice = (y - 220) // 55


            pieces = ["queen","rook","bishop","knight"]


            if 0 <= choice < 4:

                r, c = promotion_position

                board[r][c].name = pieces[choice]


                promotion = False
                promotion_position = None
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

                    castle = can_castle(board,selected,(row,col))


                    if valid_move(board,selected,(row,col)) or castle:


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



                            # CASTLING MOVE

                            if castle:

                                # king side
                                if col > old_col:

                                    rook = board[row][7]

                                    board[row][5] = rook
                                    board[row][7] = None

                                    rook.moved = True


                                # queen side
                                else:

                                    rook = board[row][0]

                                    board[row][3] = rook
                                    board[row][0] = None

                                    rook.moved = True



                            selected_piece.moved = True
                            # promotion check

                            if selected_piece.name == "pawn":


                                if selected_piece.color == "white" and row == 0:

                                    promotion = True

                                    promotion_color = "white"

                                    promotion_position = (row,col)

                                elif selected_piece.color == "black" and row == 7:

                                    promotion = True

                                    promotion_color = "black"   

                                    promotion_position = (row,col)

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
                            elif not has_any_legal_move(board,turn):

                                draw = True
                                draw_reason = "DRAW - STALEMATE"
                    


                            elif insufficient_material(board):

                                draw = True
                                draw_reason = "DRAW - INSUFFICIENT MATERIAL"
                            elif is_check(board, turn):

                                print(
                                    turn,
                                    "is in CHECK"
                                )


                    selected = None

    draw_board()

    if promotion:

        draw_promotion()

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

    if draw:

        text = result_font.render(
        draw_reason,
        True,
        (255,0,0)
    )

        text_rect = text.get_rect(
        center=(WIDTH//2, HEIGHT//2))

        screen.blit(
        text,
        (
            150,
            300
        )
    )

    pygame.display.update()



pygame.quit()