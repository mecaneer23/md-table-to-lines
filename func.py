def md_table_to_lines(
    first_line_idx: int,
    last_line_idx: int,
    filename: str = "README.md",
    remove: list[str] = [],
    column_count: int = 2,
) -> list[str]:
    """Converts a markdown table to a list of formatted strings.

    Args:
        first_line_idx (int): Index of the first line of the markdown table to be converted.
        last_line_idx (int): Index of the last line of the markdown table (+ 1) to be converted.
        filename (str, optional): Name of the markdown file containing the table. Defaults to "README.md".
        remove (list[str], optional): List of characters to be removed from each line. Defaults to [].
        column_count (int, optional): Number of columns in the markdown table. Defaults to 2.

    Returns:
        List of formatted strings representing the converted markdown table.
    """
    # get raw lines
    with open(str(filename)) as f:
        lines = f.readlines()[first_line_idx - 1 : last_line_idx - 1]

    # remove unwanted characters
    for i, _ in enumerate(lines):
        for item in remove:
            lines[i] = lines[i].replace(item, "")
        lines[i] = lines[i].split("|")[1:-1]

    # make lists of columns
    columns = [[0, []] for _ in range(column_count)]
    for i in range(column_count):
        for line in lines:
            columns[i][1].append(line[i])

    # find max length of each column
    for i, (_, v) in enumerate(columns):
        columns[i][0] = len(max([w.strip() for w in v], key=len))
    lines[1] = ["-" * (l + 1) for l, _ in columns]

    # join lines together
    for i, line in enumerate(lines):
        for j, v in enumerate(line):
            line[j] = v.lstrip() + v[-1]
        lines[i] = "".join(lines[i])
    return lines
