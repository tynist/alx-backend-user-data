#!/usr/bin/env python3
"""
Regex-ing
"""
import re


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
