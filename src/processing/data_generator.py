def data_gen(text: str) -> list:
    """
    Generate a 2D list from the given text.

    Args:
        text (str): The input text.

    Returns:
        list: A 2D list generated from the input text.
    """
    lines = text.strip().split("\n")
    result = []
    current_list = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isnumeric() or line.replace(".", "", 1).isdigit():
            current_list.append(float(line))
        else:
            if current_list:
                result.append(current_list)
            current_list = [line]

    if current_list:
        result.append(current_list)

    data = [result[i] + result[i + 1] for i in range(0, len(result), 2)]

    return data


def create_2d_list(text: str) -> list:
    """
    Given a multiline text, this function creates a 2D list where each line of text
    represents a sublist. The second element onwards in each sublist is converted to
    float values.

    Args:
        text (str): Multiline text containing the data for the 2D list.

    Returns:
        list: 2D list with the second element onwards in each sublist converted to float values.
    """
    lines = text.strip().split("\n")
    result, sublist = [], []

    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if i % 7 == 0 and sublist:
            result.append(sublist)
            sublist = []
        sublist.append(line.strip())

    if sublist:
        result.append(sublist)

    result = [[x[0]] + [float(elem) for elem in x[1:]] for x in result]

    return result
