import random
from re import findall
from typing import List, Tuple, Iterable
from math_game.business_rules import GameRule, ArithmeticRules


class MathAction(ArithmeticRules):
    def __init__(self, data: Tuple[int, int]):
        super().__init__(data)

    def get_arithmetic_actions(self) -> dict:
        action_dict = {
            "*": self.multiplication(),
            "+": self.sum(),
            "-": self.subtraction(),
            "/": self.division(),
            "**": self.exponentiation()
        }
        return action_dict


class ArithmeticGame(GameRule):
    First_range_of_numbers = (1, 9)
    Second_range_of_numbers = (1, 9)
    show_message_time = 0.9
    max_steps = 7
    level = 1

    def __init__(self, interface_class):
        self.interface_class_obj = interface_class

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        true_answer = MathAction(data).get_arithmetic_actions()[math_action]
        return answer == str(true_answer), true_answer

    def _get_random_pairs_of_numbers(self) -> list:
        return [(random.randint(*self.First_range_of_numbers),
                 random.randint(*self.Second_range_of_numbers))
                for i in range(1, self.max_steps)
                ]

    def get_random_pairs_of_numbers_with_math_action(self,
                                                     math_actions: List[str]):
        # for data in self._get_random_pairs_of_numbers():
        #     math_action = random.choice(math_actions)
        #     yield data, math_action
        return [(data, random.choice(math_actions)) for data in
                self._get_random_pairs_of_numbers()]

    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        return self.interface_class_obj.send_message_to_user(message,
                                                             show_message_time)

    def choice_user_action(self, actions: Iterable[str]) -> List[str]:
        return self.interface_class_obj.choice_user_action(actions)

    def get_user_answer(self) -> str:
        return self.interface_class_obj.get_user_answer()

    def _is_even_numbered(self, number):
        return number % 2 == 0

    def _get_level_ratio(self, level):
        if self._is_even_numbered(level):
            first_ratio, second_ratio = 1, 0
        else:
            first_ratio, second_ratio = 0, 1

        return first_ratio, second_ratio

    def set_next_level(self):

        if self.incorrect_answers < 3:
            first_ratio, second_ratio = self._get_level_ratio(self.level)
            setattr(ArithmeticGame, 'level', self.level + 1)

            self.First_range_of_numbers = [i + first_ratio * 10 for i in
                                           self.First_range_of_numbers]
            self.Second_range_of_numbers = [i + second_ratio * 10 for i in
                                            self.Second_range_of_numbers]


class FastArithmeticGame(ArithmeticGame):
    First_range_of_numbers = (1, 9)
    arithmetic_number = 2

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        result_numbers_list = [
            MathAction(
                (value, self.arithmetic_number)).get_arithmetic_actions()[
                math_action]
            for value in data
        ]
        answer_number_list = list(map(int, findall(r"\d+", answer)))
        return answer_number_list == result_numbers_list, result_numbers_list

    def _get_values(self):
        return [
            random.randint(*self.First_range_of_numbers)
            for i in range(self.level + 1)
        ]

    def _get_random_pairs_of_numbers(self) -> list:
        return [self._get_values() for i in range(1, self.max_steps)]

    def set_next_level(self):
        if self.incorrect_answers < 3:
            self.level += 1
            self.show_message_time = self.level * 0.2835
