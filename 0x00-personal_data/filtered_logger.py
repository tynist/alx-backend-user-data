#!/usr/bin/env python3
"""
Personal data
"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialize RedactingFormatter object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting specified fields."""
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates the specified fields in the log message.

    Arguments:
    - fields: list of strings representing all fields to obfuscate.
    - redaction: string representing by what the field will be obfuscated.
    - message: string represents the log line.
    - separator: string representing by which character separats all fields

    Returns:
    - The obfuscated log message.

    """
    # Create an expression pattern to match the fields with the seperator
    pattern = r"(?<={}=)[^{}]+".format(separator, separator)

    # substitution using the regular expression pattern & redaction value
    obfuscated_message = re.sub(pattern, redaction, message)

    # Return the obfuscated log message
    return obfuscated_message
