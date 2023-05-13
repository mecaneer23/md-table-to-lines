def md_table_to_lines(
    first_line_idx: int,
    last_line_idx: int,
    filename: str = "README.md",
    remove: list[str] = [],
) -> list[str]:
    """
    Converts a markdown table to a list of formatted strings.

    Args:
        first_line_idx (int): The index of the first line of the markdown table to be converted.
        last_line_idx (int): The index of the last line of the markdown table to be converted.
        filename (str, optional): The name of the markdown file containing the table. Default is "README.md".
        remove (list[str], optional): The list of strings to be removed from each line. This is in the case of formatting that should exist in markdown but not python. Default is an empty list.

    Returns:
        list[str]: A list of formatted strings representing the converted markdown table.

    Raises:
        ValueError: If the last line index is less than or equal to the first line index.
        FileNotFoundError: If the specified markdown file cannot be found.
    """

    # Check for valid line indices
    if last_line_idx <= first_line_idx:
        raise ValueError("Last line index must be greater than first line index.")

    # Get raw lines from the markdown file
    try:
        with open(filename) as f:
            lines = f.readlines()[first_line_idx - 1 : last_line_idx - 1]
    except FileNotFoundError:
        raise FileNotFoundError("Markdown file not found.")

    # Remove unwanted characters and split each line into a list of values
    for i, _ in enumerate(lines):
        for item in remove:
            lines[i] = lines[i].replace(item, "")
        lines[i] = lines[i].split("|")[1:-1]
    column_count = len(lines[0])
    lines[1] = ["-" for _ in range(column_count)]

    # Create lists of columns
    columns = [[0, []] for _ in range(column_count)]
    for i in range(column_count):
        for line in lines:
            columns[i][1].append(line[i])

    # Find the maximum length of each column
    for i, (_, v) in enumerate(columns):
        columns[i][0] = len(max([w.strip() for w in v], key=len))
    lines[1] = ["-" * (l + 1) for l, _ in columns]

    # Join the lines together into a list of formatted strings
    for i, line in enumerate(lines):
        for j, v in enumerate(line):
            line[j] = v.strip().ljust(columns[j][0] + 2)
        lines[i] = "".join(lines[i])
    lines[1] = "-" * (
        sum(columns[i][0] for i, _ in enumerate(columns)) + 2 * (len(columns) - 1)
    )
    return lines
