from __future__ import print_function
from sys import stderr

# @author Bastien Lecussan
# This program is made for python 3.6
# This code follow the Pep8 python guide code style
# This code use Typing Hint (Python 3.5 >) to type variables


def eprint(*args, **kwargs) -> None:
    """
    Print to the standard error output the given parameters
    :param args: An array of non keyworded object
    :param kwargs: An array of keyworded object
    :return: None
    """
    print(*args, file=stderr, **kwargs)
