def path_clear(board, start, end):

    old_row, old_col = start
    new_row, new_col = end


    row_step = 0
    col_step = 0


    # vertical movement

    if new_row > old_row:
        row_step = 1

    elif new_row < old_row:
        row_step = -1



    # horizontal movement

    if new_col > old_col:
        col_step = 1

    elif new_col < old_col:
        col_step = -1



    current_row = old_row + row_step
    current_col = old_col + col_step



    while (current_row != new_row or current_col != new_col):


        if board[current_row][current_col] is not None:

            return False


        current_row += row_step
        current_col += col_step



    return True
def can_castle(board,start,end):
    from check import is_check 
    row,col = start
    new_row,new_col = end

    king = board[row][col]


    if not king:
        return False


    if king.name != "king":
        return False


    if king.moved:
        return False


    # must stay same row
    if row != new_row:
        return False


    # two squares only
    if abs(new_col-col)!=2:
        return False



    # king cannot castle while in check
    if is_check(board, king.color):
        return False



    # kingside
    if new_col > col:

        rook = board[row][7]


        if not rook:
            return False


        if rook.name!="rook":
            return False


        if rook.color != king.color:
            return False


        if rook.moved:
            return False


        # squares between king and rook
        if board[row][5] or board[row][6]:
            return False


        return True



    # queenside
    else:

        rook = board[row][0]


        if not rook:
            return False


        if rook.name!="rook":
            return False


        if rook.color != king.color:
            return False


        if rook.moved:
            return False


        if board[row][1] or board[row][2] or board[row][3]:
            return False


        return True

    row,col = start
    new_row,new_col = end


    king = board[row][col]


    if not king:
        return False


    if king.name != "king":
        return False


    if king.moved:
        return False



    # must move two squares

    if abs(new_col-col)!=2:
        return False



    # kingside

    if new_col > col:

        rook = board[row][7]


        if not rook:
            return False


        if rook.name!="rook":
            return False


        if rook.moved:
            return False



        # space between

        if board[row][5] or board[row][6]:
            return False



        return True



    # queenside

    else:

        rook = board[row][0]


        if not rook:
            return False


        if rook.name!="rook":
            return False


        if rook.moved:
            return False



        if board[row][1] or board[row][2] or board[row][3]:
            return False



        return True
    
def valid_move(board, start, end):

    old_row, old_col = start
    new_row, new_col = end


    piece = board[old_row][old_col]


    # empty square
    if piece is None:
        return False



    target = board[new_row][new_col]


    # can't capture own piece

    if target:

        if target.color == piece.color:
            return False



    # direction

    if piece.color == "white":
        direction = -1
    else:
        direction = 1



    # -----------------
    # PAWN
    # -----------------

    if piece.name == "pawn":


        # simple forward

        if new_col == old_col:

            if target is None:

                if new_row - old_row == direction:
                    return True

                 # first move two squares

            if piece.moved == False:


                if new_row - old_row == (2 * direction):

                    return True

        # diagonal capture

        if abs(new_col-old_col) == 1:

            if new_row-old_row == direction:

                if target:
                    return True


        return False




    # -----------------
    # ROOK
    # -----------------

    elif piece.name == "rook":


        if old_row == new_row or old_col == new_col:


         return path_clear(
            board,
            start,
            end
        )


        return False




    # -----------------
    # BISHOP
    # -----------------

    elif piece.name == "bishop":


        if abs(new_row-old_row) == abs(new_col-old_col):
            return path_clear(
            board,
            start,
            end
        )


        return False




    # -----------------
    # QUEEN
    # -----------------

    elif piece.name == "queen":


        straight = (
            old_row == new_row
            or
            old_col == new_col
        )


        diagonal = (
            abs(new_row-old_row)
            ==
            abs(new_col-old_col)
        )


        if straight or diagonal:
            return path_clear(
            board,
            start,
            end
        )


        return False




    # -----------------
    # KNIGHT
    # -----------------

    elif piece.name == "knight":


        row_move = abs(new_row-old_row)
        col_move = abs(new_col-old_col)


        if (
            row_move == 2 and col_move == 1
            or
            row_move == 1 and col_move == 2
        ):
            return True


        return False





    # -----------------
    # KING
    # -----------------

    elif piece.name == "king":


        if (
            abs(new_row-old_row)<=1
            and
            abs(new_col-old_col)<=1
        ):
            return True


        return False



    return False