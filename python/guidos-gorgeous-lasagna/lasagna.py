"""Functions used in preparing Guido's gorgeous lasagna.

Learn about Guido, the creator of the Python language: https://en.wikipedia.org/wiki/Guido_van_Rossum
"""

EXPECTED_BAKE_TIME = 40
PREPARATION_TIME = 2


def bake_time_remaining(elapsed_bake_time):
    """Calculate the bake time remaining.

    :param elapsed_bake_time: int - baking time already elapsed.
    :return: int - remaining bake time (in minutes) derived from 'EXPECTED_BAKE_TIME'.

    Function that takes the actual minutes the lasagna has been in the oven as
    an argument and returns how many minutes the lasagna still needs to bake
    based on the `EXPECTED_BAKE_TIME`.
    """

    return elapsed_bake_time - EXPECTED_BAKE_TIME


def preparation_time_in_minutes(number_of_layers):
    """Calculate how many minutes you would spend making the lasagna.

    :param number_of_layers: int - number of layers you want to add to the lasagna.
    :return: int * the time it takes to prepare a single layer from 'PREPARATION_TIME'.
    
    Function that takes the number of layers you want to add to the lasagna as
    an argument and returns how many minutes you would spend making them.
    Assume each layer takes 2 minutes to prepare.
    """

    return number_of_layers * PREPARATION_TIME


# TODO: define the 'elapsed_time_in_minutes()' function
