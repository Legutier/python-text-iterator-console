import abc
import logging

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
        if text_state.actual_text:
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
