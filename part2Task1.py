def sort_list_of_dicts_manual(data, key):
    """
    Sorts a list of dictionaries by a specific key using the sorted function.
    """
    return sorted(data, key=lambda x: x[key])





def sort_list_of_dicts_ai(data, key):
    """
    Sorts a list of dictionaries by a specific key.
    """
    # The following line is AI-suggested
    return sorted(data, key=lambda item: item.get(key))
