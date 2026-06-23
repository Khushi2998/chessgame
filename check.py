from rules import path_clear, valid_move

def copy_board(board):

    new_board = []

    for row in board:

        new_row = []

        for piece in row:

            new_row.append(piece)

        new_board.append(new_row)


    return new_board

def find_king(board, color):

    for row in range(8):

        for col in range(8):

            piece = board[row][col]

            if piece:

                if piece.name == "king" and piece.color == color:
                    return (row, col)

    return None



def can_attack(board, start, end):

    old_row, old_col = start
    new_row, new_col = end


    piece = board[old_row][old_col]


    if piece is None:
        return False



    row_diff = abs(new_row - old_row)
    col_diff = abs(new_col - old_col)



    # pawn

    if piece.name == "pawn":

        direction = -1

        if piece.color == "black":
            direction = 1


        if (
            new_row - old_row == direction
            and col_diff == 1
        ):
            return True


        return False




    # knight

    if piece.name == "knight":

        return (
            row_diff == 2 and col_diff == 1
            or
            row_diff == 1 and col_diff == 2
        )




    # bishop

    if piece.name == "bishop":

        if row_diff == col_diff:

            return path_clear(
                board,
                start,
                end
            )

        return False




    # rook

    if piece.name == "rook":

        if old_row == new_row or old_col == new_col:

            return path_clear(
                board,
                start,
                end
            )

        return False




    # queen

    if piece.name == "queen":

        straight = (
            old_row == new_row
            or
            old_col == new_col
        )


        diagonal = (
            row_diff == col_diff
        )


        if straight or diagonal:

            return path_clear(
                board,
                start,
                end
            )

        return False




    # king

    if piece.name == "king":

        return (
            row_diff <= 1
            and col_diff <= 1
        )



    return False





def is_check(board, color):


    king = find_king(board,color)


    if king is None:
        return False



    enemy = "black"

    if color == "black":
        enemy = "white"



    for row in range(8):

        for col in range(8):

            piece = board[row][col]


            if piece and piece.color == enemy:


                if can_attack(
                    board,
                    (row,col),
                    king
                ):

                    return True


    return False

def has_any_move(board, color):


    for old_row in range(8):

        for old_col in range(8):


            piece = board[old_row][old_col]


            # only player's pieces

            if piece and piece.color == color:


                for new_row in range(8):

                    for new_col in range(8):


                        # cannot move to same square

                        if old_row == new_row and old_col == new_col:
                            continue



                        if valid_move(
                            board,
                            (old_row,old_col),
                            (new_row,new_col)
                        ):


                            # simulate move

                            temp = copy_board(board)


                            temp[new_row][new_col] = temp[old_row][old_col]

                            temp[old_row][old_col] = None



                            # king safe?

                            if not is_check(
                                temp,
                                color
                            ):

                                return True



    return False

def is_checkmate(board,color):


    if is_check(board,color):


        if not has_any_move(board,color):

            return True


    return False