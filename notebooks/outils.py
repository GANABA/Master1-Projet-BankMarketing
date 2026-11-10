"""
Fonctions de presentation dans le shell.

Reprises de la correction du TD2 afin que la sortie du projet ait la meme forme que celle des TD.
"""


################################################################################
#
# PRESENTATION DANS LE SHELL
#
################################################################################
class ansi_esc:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def bold(s):
    return ansi_esc.BOLD + str(s) + ansi_esc.END


def green(s):
    return ansi_esc.GREEN + str(s) + ansi_esc.END


def cyan(s):
    return ansi_esc.CYAN + str(s) + ansi_esc.END


def print_title(s):
    print('\n' + 80 * '-')
    print(bold(green('Fichier :')) + ' : ' + s)
    print(80 * '-')


def print_step(s):
    print(ansi_esc.YELLOW + '\n*** ' + s + ' ***' + ansi_esc.END + '\n')


def print_error(s):
    print('\n\n')
    print(ansi_esc.RED + s + ansi_esc.END)
    print('\n\n')
