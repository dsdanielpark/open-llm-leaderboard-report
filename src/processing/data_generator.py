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
