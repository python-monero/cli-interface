from PyInquirer import Validator, ValidationError
from .commands import address
from .commands import balance
from .commands import help
from .commands import refresh
from .commands import transfer

# from .commands import unspent_outputs
from .commands import version
from .commands import exit


class CommandValidator(Validator):
    def validate(self, document):
        valid_commands = (
            address.COMMAND,
            balance.COMMAND,
            help.COMMAND,
            refresh.COMMAND,
            transfer.COMMAND,
            # unspent_outputs.COMMAND,
            version.COMMAND,
            exit.COMMAND,
        )
        command = document.text.split()[0]
        if not command in valid_commands:
            raise ValidationError(
                message=f"unknown command: {document.text}",
                cursor_position=len(document.text),
            )
