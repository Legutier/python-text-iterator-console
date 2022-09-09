NOT_VALID_COMMAND = (
    "Invalid command. Please use specified options. Press H to get help of all commands."
)

NO_TEXT_AVAILABLE = "No text Available here."
HELP_MESSAGE = (
    "A and D to move between texts(previous and next respectively).\n"
    "X to exit application.\n"
    "C to compare a text with another one: first one selects, "
    "and then you can press C again on another text to compare.\n"
    "S to summarize data.\n"
    "Q to go back to the text you were reading.\n"
    "H to get this message."
)


class ConsoleDefaultMessages:
    INPUT_MESSAGE = "what is your [bold red]command[/]? :smiley:"
    GUIDE_MAIN = "press H to get [italic green]help[/]"


class InterfaceCommands:
    MOVE_NEXT_COMMAND = "D"
    MOVE_PREVIOUS_COMMAND = "A"
    EXIT_COMMAND = "X"
    COMPARE_COMMAND = "C"
    SUMMARY_COMMAND = "S"
    RETURN_COMMAND = "Q"
    HELP_COMMAND = "H"


class OutputType:
    MESSAGE = 0
    TEXT = 1
    ACTION_ON_TEXT = 2


STYLES = ["bold", "italic black on white", "italic black on yellow"]
