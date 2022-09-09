import abc
import logging

from dataclasses import asdict
from typing import Dict, Type, Optional, Tuple

import project.constants as constants
from .extra_dataclasses import TextData


logger = logging.getLogger(__name__)


class CommandMeta(type(abc.ABC)):

    def __call__(cls, *args, **kwargs):
        logger.info(
            f"COMMAND {cls.__name__} EXECUTED",
        )
        return super(CommandMeta, cls).__call__(*args, **kwargs)


class AbstractCommand(abc.ABC, metaclass=CommandMeta):
    @abc.abstractmethod
    def __call__(self, text_state: TextData):
        raise NotImplementedError


class CommandHandler:
    def __init__(self, command_mapping: Dict[str, Type[AbstractCommand]]):
        self.commands = command_mapping
        self.invalid_command = UndefinedCommand

    def execute(
        self, command_input: str, text_data: TextData
    ) -> Optional[Tuple[str, str]]:
        command = self.commands.get(command_input.upper(), self.invalid_command)()
        return command(text_data)


class UndefinedCommand(AbstractCommand):
    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        return constants.NOT_VALID_COMMAND, constants.OutputType.MESSAGE


class MoveCommand(AbstractCommand):

    def __init__(self):
        self.main_stack = None
        self.backup_stack = None

    def move_stacks(self, text_state: TextData) -> Tuple[str, str]:
        if text_state.actual_text is not None:
            self.backup_stack.append(text_state.actual_text)
        try:
            text = self.main_stack.pop()
        except IndexError:
            text_state.actual_text = None
            return constants.NO_TEXT_AVAILABLE, constants.OutputType.MESSAGE
        text_state.actual_text = text
        return text, constants.OutputType.TEXT


class MoveNextCommand(MoveCommand):
    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        self.main_stack = text_state.main_stack
        self.backup_stack = text_state.traversed_stack
        return self.move_stacks(text_state)


class MovePreviousCommand(MoveCommand):

    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        self.main_stack = text_state.traversed_stack
        self.backup_stack = text_state.main_stack
        return self.move_stacks(text_state)


class ExitCommand(AbstractCommand):
    def __call__(self, text_state: TextData) -> None:
        exit(0)


class CompareCommand(AbstractCommand):

    def resolve_no_actual_text_available(self, text_state: TextData) -> Tuple[str, str]:
        return constants.NO_TEXT_AVAILABLE, constants.OutputType.MESSAGE

    def resolve_no_compared_text(self, text_state: TextData) -> Tuple[str, str]:
        text_state.to_compare_text = text_state.actual_text
        return text_state.actual_text, constants.OutputType.ACTION_ON_TEXT

    def resolve_comparison(self, text_state: TextData) -> Tuple[str, str]:
        if text_state.actual_text == text_state.to_compare_text:
            message = (
                f"[bold red]both text are the same[/]: {text_state.actual_text}\n"
                f"length: {len(text_state.actual_text)}"
            )
            text_state.to_compare_text = None
            return message, constants.OutputType.MESSAGE
        sorted_text = sorted(
            [text_state.to_compare_text, text_state.actual_text],
            key=len,
        )
        message = (
            f"{sorted_text[1]}\n\n\n"
            f"[bold dark_green]is bigger than [underline grey0]{sorted_text[0]}[/] "
            f"by [underline]{abs(len(sorted_text[0]) - len(sorted_text[1]))}.[/] "
            f"Bigger text has [grey0]{len(sorted_text[1])}[/] length. "
            f"Smaller one has [red]{len(sorted_text[0])}[/] length.[/]"
        )
        text_state.to_compare_text = None
        return message, constants.OutputType.TEXT

    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        resolvers = [
            (text_state.actual_text is None, self.resolve_no_actual_text_available),
            (text_state.to_compare_text is None, self.resolve_no_compared_text),
        ]
        resolver = next(
            (resolver for condition, resolver in resolvers if condition),
            self.resolve_comparison,
        )
        logger.info(
            f"EXECUTING {resolver} ON COMPARE COMMAND.",
            extra={"data": asdict(text_state)}
        )
        return resolver(text_state=text_state)


class SummaryCommand:

    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        complete_stack = text_state.main_stack + text_state.traversed_stack
        if text_state.actual_text is not None:
            complete_stack.append(text_state.actual_text)
        logger.info(f"STACK_LENGTH: {len(complete_stack)}")
        biggest_text = max(complete_stack, key=len)
        smallest_text = min(complete_stack, key=len)
        message = (
            f"Biggest text is {biggest_text} with {len(biggest_text)} length.\n"
            f"Smallest text is {smallest_text} with {len(smallest_text)} length"
        )
        return message, constants.OutputType.MESSAGE


class HelpCommand:

    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        return constants.HELP_MESSAGE, constants.OutputType.MESSAGE


class ReturnCommand:

    def __call__(self, text_state: TextData) -> Tuple[str, str]:
        return text_state.actual_text or "", constants.OutputType.TEXT
