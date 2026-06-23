class Piece:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moved = False

    def symbol(self):

        symbols = {

            "white": {
                "king":"♔",
                "queen":"♕",
                "rook":"♖",
                "bishop":"♗",
                "knight":"♘",
                "pawn":"♙"
            },

            "black": {
                "king":"♚",
                "queen":"♛",
                "rook":"♜",
                "bishop":"♝",
                "knight":"♞",
                "pawn":"♟"
            }
        }


        return symbols[self.color][self.name]