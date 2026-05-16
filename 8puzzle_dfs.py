import tkinter as tk
import random

goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

moves = {
    "Left": -1,
    "Right": 1,
    "Up": -3,
    "Down": 3
}


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action


def goal_test(state):
    return state == goal


def valid_actions(state):
    i = state.index(0)
    actions = []

    if i % 3 != 0:
        actions.append("Left")
    if i % 3 != 2:
        actions.append("Right")
    if i >= 3:
        actions.append("Up")
    if i <= 5:
        actions.append("Down")
    return actions


def swap(state, action):
    state = list(state)
    i_0 = state.index(0)
    new_0 = i_0 + moves[action]
    state[i_0], state[new_0] = state[new_0], state[i_0]
    return tuple(state)


def child_node(node, action):
    new_state = swap(node.state, action)
    return Node(new_state, node, action)


def solution(node):
    steps = []
    states = []
    while node is not None:
        states.append(node.state)
        if node.action is not None:
            steps.append(node.action)
        node = node.parent

    states.reverse()
    steps.reverse()
    return steps, states


def dfs(initial_state):
    node = Node(initial_state)

    if goal_test(node.state):
        return [], [node.state]
    frontier = []
    frontier.append(node)

    frontier1 = {node.state}
    explored = set()

    while frontier:
        node = frontier.pop()
        frontier1.remove(node.state)

        explored.add(node.state)

        for action in valid_actions(node.state):
            child = child_node(node, action)

            if child.state not in explored and child.state not in frontier1:
                if goal_test(child.state):
                    return solution(child)

                frontier.append(child)
                frontier1.add(child.state)
    return None


def generate_random_state():
    state = goal
    for _ in range(40):
        actions = valid_actions(state)
        action = random.choice(actions)
        state = swap(state, action)
    return state


class EightPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle DFS")

        self.current_state = generate_random_state()
        self.steps = []
        self.states = []
        self.index = 0

        title = tk.Label(
            root,
            text="8 Puzzle giải bằng DFS",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.tiles = []
        for i in range(9):
            tile = tk.Label(
                self.frame,
                text="",
                width=6,
                height=3,
                font=("Arial", 24, "bold"),
                borderwidth=2,
                relief="ridge",
                bg="white"
            )
            tile.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.tiles.append(tile)
        self.info = tk.Label(
            root,
            text="",
            font=("Arial", 13)
        )
        self.info.pack(pady=10)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        self.random_button = tk.Button(
            button_frame,
            text="Tạo random",
            width=18,
            height=2,
            font=("Arial", 12, "bold"),
            command=self.generate_random
        )
        self.random_button.grid(row=0, column=0, padx=10)
        self.solve_button = tk.Button(
            button_frame,
            text="Giải",
            width=18,
            height=2,
            font=("Arial", 12, "bold"),
            command=self.auto_solve
        )
        self.solve_button.grid(row=0, column=1, padx=10)
        self.draw_board(self.current_state)

    def draw_board(self, state):
        for i, value in enumerate(state):
            if value == 0:
                self.tiles[i].config(text="", bg="lightgray")
            else:
                self.tiles[i].config(text=str(value), bg="white")

    def generate_random(self):
        self.current_state = generate_random_state()
        self.steps = []
        self.states = []
        self.index = 0
        self.draw_board(self.current_state)
        self.info.config(text="Đã tạo random.")

    def auto_solve(self):
        result = dfs(self.current_state)

        if result is None:
            self.info.config(text="Không tìm thấy hướng giải.")
            return

        self.steps, self.states = result
        self.index = 0
        self.random_button.config(state="disabled")
        self.solve_button.config(state="disabled")
        self.show_step()

    def show_step(self):
        if self.index < len(self.states):
            state = self.states[self.index]
            self.draw_board(state)

            if self.index == 0:
                self.info.config(
                    text=f"Khởi tạo| Tổng bước: {len(self.steps)}"
                )
            else:
                move = self.steps[self.index - 1]
                self.info.config(
                    text=f"Bước {self.index}/{len(self.steps)} | Di chuyển: {move}"
                )

            self.index += 1
            self.root.after(700, self.show_step)

        else:
            self.current_state = goal
            self.random_button.config(state="normal")
            self.solve_button.config(state="normal")
            self.info.config(text="Giải thành công!")


root = tk.Tk()
app = EightPuzzleApp(root)
root.mainloop()