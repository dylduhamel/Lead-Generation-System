import textwrap

def status_print(message):
    """
    Prints out a message in a formatted way.
    """
    print("*" * 50)  # Print a line of *s

    # Print each line of the message in a formatted way
    for line in textwrap.wrap(message, width=45):
        print("* {: <45}*".format(line))

    print("*" * 50)  # Print a line of *s
