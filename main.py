import argparse
import logging
import re
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Replaces specific characters in data fields with a specified replacement character.")

    parser.add_argument("input_data", help="The input data string to process.")
    parser.add_argument("-c", "--characters", default="\\d", help="The character set to replace (regular expression). Defaults to '\\d' (digits).")
    parser.add_argument("-r", "--replacement", default="X", help="The replacement character. Defaults to 'X'.")
    parser.add_argument("-g", "--global_replace", action="store_true", help="Replace all occurences of the matching characters, otherwise only the first.")
    parser.add_argument("-i", "--ignore_case", action="store_true", help="Ignore case during character matching (useful for letters)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    parser.add_argument("-s", "--security", action="store_true", help="Enable secure processing that avoids printing the original input data if possible.")

    return parser


def replace_characters(input_data, characters, replacement, global_replace, ignore_case, security):
    """
    Replaces specific characters in the input data with the specified replacement character.

    Args:
        input_data (str): The input data string.
        characters (str): The regular expression for the characters to replace.
        replacement (str): The replacement character.
        global_replace (bool): Whether to replace all occurrences or only the first.
        ignore_case (bool): Whether to ignore case during character matching.
        security (bool): Avoid displaying original data

    Returns:
        str: The modified data string.

    Raises:
        TypeError: If input data is not a string.
        ValueError: If characters or replacement are invalid.
        re.error: If the regular expression is invalid.
    """

    if not isinstance(input_data, str):
        logging.error("Input data must be a string.")
        raise TypeError("Input data must be a string.")

    if not isinstance(characters, str):
        logging.error("Characters must be a string (regular expression).")
        raise ValueError("Characters must be a string (regular expression).")

    if not isinstance(replacement, str):
        logging.error("Replacement must be a string.")
        raise ValueError("Replacement must be a string.")

    if len(replacement) != 1:
         logging.warning("Replacement should be single character, otherwise, results may vary.")

    try:
        if ignore_case:
            regex = re.compile(characters, re.IGNORECASE)
        else:
            regex = re.compile(characters)

        if global_replace:
            modified_data = regex.sub(replacement, input_data)
        else:
            modified_data = regex.sub(replacement, input_data, count=1)
    except re.error as e:
        logging.error(f"Invalid regular expression: {e}")
        raise

    if security:
        logging.info("Secure processing enabled.  The original input data has not been printed to the logs.")
    else:
        logging.debug(f"Original data: {input_data}")


    logging.info(f"Replaced '{characters}' with '{replacement}'")
    logging.debug(f"Modified data: {modified_data}")  # Debug logging is important.

    return modified_data


def main():
    """
    Main function to parse arguments and execute the data replacement.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        modified_data = replace_characters(
            args.input_data,
            args.characters,
            args.replacement,
            args.global_replace,
            args.ignore_case,
            args.security
        )
        print(modified_data)

    except (TypeError, ValueError, re.error) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Usage Examples:
    # python main.py "123-456-7890" -c "\d" -r "X"
    # python main.py "John Doe" -c "[aeiou]" -r "*" -i
    # python main.py "Password123" -c "\d" -r "0" -g
    # python main.py "SensitiveData" -c "." -r "*" -g -s
    main()