class Colors:
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m" 

def clear_markdown_to_color(text: str) -> str:
    """
    This function takes a markdown formatted text as input, processes it to add color to code blocks,
    and then returns the modified text.

    Args:
        text (str): The input string which may contain Markdown notation for code blocks.

    Returns:
        str: Colored text where code blocks are highlighted.
    """
    lines = text.split('\n')
    new_lines = []
    in_code_block = False

    for line in lines:
        if '```' in line:
            in_code_block = not in_code_block
            # new_lines.append( "") # line.strip() )
        elif in_code_block:
            new_lines.append(Colors.CYAN + line.strip() + Colors.ENDC)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def clear_markdown(text: str) -> str:

    fs = text.splitlines()
    # Remove markdown code blocks
    response = "\n".join([s for s in fs if "```" not in s])

    # Remove backticks
    response = "\n".join(
        [e for e in response.split("`") if e.strip() != ""])

    response = response.strip()

    return response



def ask_yes_no(question) -> bool :
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ['y', 'n']:
            if answer == 'y':
                return True
            return False

        else:
            print("Please respond with 'y' or 'n'.")






