class Puzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.unique_states = set()
        self.actions = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}

    def goal_test(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = []
        zero_index = state.index(0)
        for action in self.actions:
            target_index = zero_index + self.actions[action]
            # перевіряємо чи після свапу "0" не буде за межами пазлу
            if (action in ["UP", "DOWN"] and 0 <= target_index < len(state)) or \
                    (action == "LEFT" and zero_index % 3 != 0) or \
                    (action == "RIGHT" and zero_index % 3 != 2):
                new_state = state.copy()
                new_state[zero_index], new_state[target_index] = new_state[target_index], new_state[zero_index]
                successors.append((new_state, action))
                self.unique_states.add(tuple(new_state))

        return successors
