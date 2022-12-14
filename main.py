from project import commands
from rich.console import Console
from rich.panel import Panel

import logging

from project.extra_dataclasses import TextData
from project.constants import InterfaceCommands, STYLES, ConsoleDefaultMessages

logging.basicConfig(
    filename="application.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(filename)s:%(message)s",
)

def read_file():
    try:
        text = list(
            line.rstrip('\n')
            for line in open("text.txt", "r", encoding="utf-8").readlines()
        )[::-1]
    except FileNotFoundError:
        print("there is no file available.")
        text = None
    return text


if __name__ == "__main__":
    text_input = read_file()
    if text_input is None:
        exit()
    text_state = TextData(main_stack=text_input)

    command_mapping = {
        InterfaceCommands.MOVE_NEXT_COMMAND: commands.MoveNextCommand,
        InterfaceCommands.MOVE_PREVIOUS_COMMAND: commands.MovePreviousCommand,
        InterfaceCommands.EXIT_COMMAND: commands.ExitCommand,
        InterfaceCommands.COMPARE_COMMAND: commands.CompareCommand,
        InterfaceCommands.SUMMARY_COMMAND: commands.SummaryCommand,
        InterfaceCommands.RETURN_COMMAND: commands.ReturnCommand,
        InterfaceCommands.HELP_COMMAND: commands.HelpCommand,
    }
    handler = commands.CommandHandler(command_mapping=command_mapping)
    console = Console()

    while True:
        console.print("")
        command_input = console.input(ConsoleDefaultMessages.INPUT_MESSAGE)
        response, status = handler.execute(
            command_input=command_input,
            text_data=text_state,
        )
        console.print(Panel(response), style=STYLES[status])
