class Mancala(object):
    def __init__(self, m=6, k=4, state=None):
        self.M = m
        self.K = k
        self.ready_player = 1
        self.state = state if state else self.generate_init_state()

    def reset(self):
        """reset the environment"""
        self.ready_player = 1
        self.state = self.generate_init_state()

    def generate_init_state(self):
        """initial state"""
        return [self.K] * self.M + [0] + [self.K] * self.M + [0]

    def p1_pits(self):
        """get pits number for player1"""
        return self.state[:self.M]

    def p2_pits(self):
        """get pits number for player2"""
        return self.state[self.M + 1:-1]

    def p1_store(self):
        """get the store number for player1"""
        return self.state[self.M]

    def p2_store(self):
        """get the store number for player2"""
        return self.state[-1]

    def p_pits(self, index):
        """get pits number for the player"""
        if index == 1:
            return self.p1_pits()
        else:
            return self.p2_pits()

    def p_store(self, index):
        """get the store number for player"""
        if index == 1:
            return self.p1_store()
        else:
            return self.p2_store()

    def update_store(self, value, index):
        """update the store of the player (index) with value"""
        if index == 1:
            self.state[self.M] = value
        else:
            self.state[-1] = value

    def update_pit(self, value, pit_index, index):
        """update the pit in the pir_index of the player (index) with value"""
        if index == 1:
            self.state[pit_index] = value
        else:
            self.state[pit_index + self.M + 1] = value

    def filter_actions(self, player):
        """filter legal actions"""
        pits = self.p_pits(player.index)
        return [i for i, v in enumerate(pits) if v > 0]

    def show_board(self):
        """visualize the board state"""
        board_vis = f"\n{'*' * 22}Board state{'*' * 23}\n"
        str_p2_store=" "+str(self.p2_store()) if self.p2_store()<10 else str(self.p2_store())
        board_vis += (f" {str_p2_store} - |   " +
                      " ||  ".join(
                          [i if len(i) == 2 else ' ' + i for i in list(map(str, self.p2_pits()[::-1]))]) + " |      \n")
        board_vis += f"{'-------' * (self.M + 2)}\n"
        board_vis += ("      |   " + " ||  ".join(
            [i if len(i) == 2 else ' ' + i for i in list(map(str, self.p1_pits()))]) +
                      f" | -   {self.p1_store()}\n")
        board_vis += f"{'*' * 56}\n"
        print(board_vis)

    def check_end_game(self):
        """either players runs out of stones"""
        return False if (any(self.p1_pits()) and any(self.p2_pits())) else True

    def find_scores(self):
        """get the scores of both players"""
        p1_score = self.p1_store()
        p2_score = self.p2_store()
        return p1_score, p2_score

    def find_winner_scores(self):
        """find the winner and scores of two players"""
        p1_score, p2_score = self.find_scores()
        if p1_score > p2_score:
            winner = 1
        elif p1_score < p2_score:
            winner = 2
        else:
            winner = 0
        return winner, p1_score, p2_score

    def end_game(self, show_flag=True):
        """Game over and choose to visualize it"""
        winner, p1_score, p2_score = self.find_winner_scores()

        if show_flag:
            self.show_board()

            go_str = "Game Over!\n"
            if winner == 1:
                go_str += f"{'#' * 24}\n##   Player 1 wins!   ##\n"
            elif winner == 2:
                go_str += f"{'#' * 24}\n##   Player 2 wins!   ##\n"
            else:
                go_str += f"{'#' * 24}\n##        Draw.       ##\n"
            go_str += f"## Player 1 score: {self.p1_store():2d} ##\n"
            go_str += f"## Player 2 score: {self.p2_store():2d} ##\n{'#' * 24}\n"
            print(go_str)
        return winner

    def check_illegal_move(self, player, action):
        """check if the move is legal"""
        available_actions = self.filter_actions(player)
        if action not in available_actions:
            print('Illegal move! Please choose another move!')
            return False
        return True

    def sow_step(self, player, move):
        """update the board for the player with move"""
        init_pit = move
        stones = self.p_pits(player.index)[init_pit]
        clen = 2 * self.M + 1

        if player.index == 1:
            cstate = self.state[:-1]
        else:
            cstate = self.p2_pits() + [self.p2_store()] + self.p1_pits()

        per_add = stones // clen
        dis_pit = stones % clen

        cstate[init_pit] = 0
        last_pit = (init_pit + dis_pit) % clen
        new_state = [i + per_add for i in cstate]
        if last_pit > init_pit:
            new_state = [
                v + 1 if init_pit < i <= last_pit else v
                for i, v in enumerate(new_state)
            ]
        elif last_pit < init_pit:
            new_state = [
                v + 1 if (init_pit < i or i <= last_pit) else v
                for i, v in enumerate(new_state)
            ]
        else:
            pass

        if player.index == 1:
            return new_state + [self.p2_store()], last_pit
        else:
            return new_state[-self.M:] + [self.p1_store()
                                          ] + new_state[:-self.M], last_pit

    def sowing(self, player, move):
        """update state
        ---
        return True if it is still this player's turn; False to change the player"""
        self.state, last_pit = self.sow_step(player, move)
        if last_pit == self.M:
            """If the last stone is sowed into the store, then the player gets to take another turn."""
            return True
        if last_pit < self.M and self.p_pits(player.index)[last_pit] == 1:
            """If the last stone is sowed into one of the player’s own empty pits, 
            then the player captures any stones in their opponents pit directly across the board."""
            opp_last_pit = self.M - 1 - last_pit
            # update the store
            self.update_store(
                self.p_store(player.index) + 1 +
                self.p_pits(player.opp_index)[opp_last_pit], player.index)
            # empty two puts
            self.update_pit(0, last_pit, player.index)
            self.update_pit(0, opp_last_pit, player.opp_index)
        return False

    def play_game(self, player_1, player_2, show_flag=True):
        """play the whole game"""
        players = [player_1, player_2]
        player = players[self.ready_player - 1]

        if show_flag:
            print('initial state:')
            self.show_board()

        while True:
            if self.check_end_game():
                return self.end_game(show_flag)

            if show_flag:
                print(f"Player {player.index}:")
            move = player.get_move(self)
            moves = [move]
            while self.sowing(player, move):

                if self.check_end_game():
                    return self.end_game(show_flag)
                move = player.get_move(self)
                if show_flag: print(f'\t {player.algo} choice: {move}')
                moves.append(move)
            if show_flag: self.show_board()
            player = players[player.opp_index - 1]
