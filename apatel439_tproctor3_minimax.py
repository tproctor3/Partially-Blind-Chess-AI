#!/usr/bin/env python3

"""
File Name:      apatel439_tproctor_minimax.py
Authors:        Thomas Proctor and Aakanksha Patel
Date:           March 26, 2019

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
import math
from game import Game
from player import Player


# TODO: Rename this class to what you would like your bot to be named during the game.
class TheRoastedChessNuts(Player):
    moves = 0
    color = None
    board = None
    currGame = None
    baseBoard = chess.BaseBoard()

    recently_captured = None
    rejected_move = None
    def __init__(self):
        pass
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        # TODO: implement this method
        moves = 0
        self.board = board.copy()
        self.color = color
        self.currGame = Game()
        self.recently_captured = None
        self.rejected_move = None
        self.baseBoard = board.copy()
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        # self.board.push()
        if captured_piece:
            self.board.remove_piece_at(captured_square)
            # if(self.color == chess.WHITE):
            #     self.board.set_piece_at(captured_square, Piece(3, chess.BLACK))
            # else:
            #     self.board.set_piece_at(captured_square, Piece(3, chess.WHITE))
            self.recently_captured = captured_square
        else:
            self.recently_captured = None


    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        # TODO: update this method

        # edges = [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 ,
        #          8 , 16, 24, 32, 40, 48, 56
        #          15, 23, 31, 39, 47, 55, 63
        #          57, 58, 59, 60, 61, 62 ]
        # result = random.choice(possible_sense)

        # while result in edges:
        #     result = random.choice(possible_sense)

        result = random.choice(possible_sense)

        # if a piece has been recently captured, figured out what happened there
        if self.recently_captured is not None:
            result = self.recently_captured

        # if a move got rejected, chances are something is in the middle.
        # figure out what that is
        if self.rejected_move is not None:
            start = self.rejected_move.from_square
            end = self.rejected_move.to_square

            avg_file = int((chess.square_file(start) + chess.square_file(end)) / 2)
            avg_rank = int((chess.square_rank(start) + chess.square_rank(end)) / 2)

            result = (8 * avg_rank) + avg_file

         # shift the chosen square to produce a 3x3 within borders
        if chess.square_file(result) == 0:
            result += 1
        elif chess.square_file(result) == 7:
            result -= 1

        if chess.square_rank(result) == 0:
            result += 8
        elif chess.square_rank(result) == 7:
            result -= 8

        return result
        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        # TODO: implement this method
        # Hint: until this method is implemented, any senses you make will be lost.
        for sr in sense_result:
            self.board.remove_piece_at(sr[0])
            if sr[1]:   
                self.board.set_piece_at(sr[0], sr[1])

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        # TODO: update this method
        # choice = random.choice(possible_moves)
        choice = None
        best = None
        if self.color == chess.WHITE:
            if self.moves == 0:
                choice = chess.Move(chess.E2, chess.E4)
            elif self.moves == 1:
                choice = chess.Move(chess.G1, chess.F3)
            elif self.moves == 2:
                choice = chess.Move(chess.F1, chess.C4)
            elif self.moves == 3:
                choice = chess.Move(chess.E1, chess.G1)
            else:
                best = calculate_best_move(50, len(possible_moves), self.board, self.color, possible_moves)[1]
            self.moves = self.moves + 1
        if self.color == chess.BLACK:
            if self.moves == 0:
                choice = chess.Move(chess.E7, chess.E5)
            elif self.moves == 1:
                choice = chess.Move(chess.G8, chess.F6)
            elif self.moves == 2:
                choice = chess.Move(chess.F8, chess.C5)
            elif self.moves == 3:
                choice = chess.Move(chess.E8, chess.G8)
            else:
                best = calculate_best_move(50, len(possible_moves), self.board, self.color, possible_moves)[1]
            self.moves = self.moves + 1
        if best:
            return chess.Move(best.from_square, best.to_square)
        return choice

    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        # TODO: implement this method
        if not taken_move.__eq__(requested_move):
            self.rejected_move = requested_move
        else:
            self.rejected_move = None

        if taken_move is not None:    
            self.board.push(taken_move)
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        # print(winner_color, "by", win_reason)

        if(winner_color == self.color):
            print("Tom and Aaki won! :D", win_reason)
        else:
            print("Tom and Aaki lost :(", win_reason)

def calculate_best_move(depth, width, board, color, possMoves, alpha=-math.inf, beta=math.inf, isMaximizingPlayer = True):
    if depth == 0 or width > 4000:
        value = evaluate_board(board, color)
        return value, None

    bestMove = None
    plays = list(board.legal_moves)

    if len(plays) == 0:
        value = evaluate_board(board, color)
        return value, None
    # random.shuffle(possMoves)
    if isMaximizingPlayer:
        bestMoveValue = -math.inf
    else:
        bestMoveValue = math.inf
    for move in possMoves:
        board.push(move)

        value = calculate_best_move(depth - 1, (len(plays) * width), board, color, plays, alpha, beta, not isMaximizingPlayer)[0]

        if isMaximizingPlayer:
            if value > bestMoveValue:
                bestMoveValue = value
                bestMove = move
            alpha = max(alpha, value)
        else:
            if value < bestMoveValue:
                bestMoveValue = value
                bestMove = move
            beta = min(beta, value)
        board.pop()
        if beta <= alpha:
            break
    if bestMove:
        return bestMoveValue, bestMove
    return bestMoveValue, plays[0]


def evaluate_board(board, color):
    pieceValWhite = {
        'P' : 100,
        'N' : 350,
        'B' : 350,
        'R' : 525,
        'Q' : 1000,
        'K' : 10000,
    }
    pieceValBlack = {
        'p': 100,
        'n': 350,
        'b': 350,
        'r': 525,
        'q': 1000,
        'k': 10000
    }
    currVal = 0
    for x in chess.SQUARES:
        squareVal = chess.BaseBoard.piece_at(board, x)
        if squareVal:
            type = str(squareVal)
            if color == True:
                if type in pieceValWhite:
                    currVal = currVal + pieceValWhite[type]
                else:
                    currVal = currVal - pieceValBlack[type]
            else:
                if type in pieceValBlack:
                    currVal = currVal + pieceValBlack[type]
                else:
                    currVal = currVal - pieceValWhite[type]
    return currVal

