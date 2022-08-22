import random
import threading
from tkinter import Frame, Label, CENTER, Button

from stopwatch import Stopwatch

import constants as c
from original import logic, autosolve


def gen():
    return random.randint(0, c.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        frame = Frame.__init__(self)
        self.step_count = 0
        self.grid()
        self.master.title('2048')

        # A button to start auto-solve
        Button(frame, text='Auto-Solve', command=self.start_auto_solve_thread).grid(column=1, row=0)
        Button(frame, text='Repeat Auto-Solve', command=self.start_repeating_auto_solve_thread).grid(column=1, row=1)
        Button(frame, text='Refresh', command=self.refresh).grid(column=1, row=2)

        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.update_grid_cells()
        # Timing
        self.stop_watch = Stopwatch()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def refresh(self):
        self.step_count = 0
        self.matrix = logic.new_game(c.GRID_LEN)
        self.update_grid_cells()
        self.stop_watch.stop()

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT:
            exit()
        elif key in self.commands:
            self.commit_move(key)

    def commit_move(self, key):

        if not self.stop_watch.running:
            self.stop_watch.start()

        self.matrix, done = self.commands[key](self.matrix)
        # Print the score

        if done:
            self.step_count += 1
            self.matrix = logic.add_two_or_four(self.matrix)
            '''
            print("The monotone score: " + str(logic.score_monotone(self.matrix)) +
                  " square amount score: " + str(logic.score_number_of_squares(self.matrix)) +
                  " weighted square amount score: " + str(logic.score_weighted_squares(self.matrix)))
            '''
            # record last move
            self.update_grid_cells()
            state = logic.game_state(self.matrix)

            if state != 'not over':
                self.stop_watch.stop()
                if state == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                elif state == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                time_cost = round(self.stop_watch.duration, 0)
                print("State: " + state + " Time cost: " + str(time_cost) + " Total steps: " + str(self.step_count))

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

    def start_auto_solve_thread(self):
        thread = threading.Thread(target=self.auto_solve, args=())
        thread.setDaemon(True)
        thread.start()  # 启动线程

    def auto_solve(self):
        current_status = logic.game_state(self.matrix)
        while current_status != 'win' and current_status != 'lose':
            # next_step = autosolve.get_solution_1(self.matrix)
            next_step = autosolve.get_solution_2(self.matrix)
            if next_step == 'STOP':
                break
            else:
                self.commit_move(next_step)
                current_status = logic.game_state(self.matrix)

    def start_repeating_auto_solve_thread(self):
        thread = threading.Thread(target=self.repeating_auto_solve, args=())
        thread.setDaemon(True)
        thread.start()  # 启动线程

    def repeating_auto_solve(self):

        for test_round in range(1, 1000):

            current_status = logic.game_state(self.matrix)
            while current_status != 'win' and current_status != 'lose':

                next_step = autosolve.get_solution_2_cache(autosolve.convert_matrix_to_string(self.matrix))
                if next_step == 'STOP':
                    break
                else:
                    self.commit_move(next_step)
                    current_status = logic.game_state(self.matrix)

            # refresh
            self.refresh()


game_grid = GameGrid()
