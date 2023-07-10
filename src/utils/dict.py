def convert_dict_to_yaml(dictionary):
    yaml_output = ""
    for key, value in dictionary.items():
        yaml_output += key + ":\n"
        for inner_key, inner_value in value.items():
            if isinstance(inner_value, bool):
                inner_value = str(inner_value).lower()
            elif isinstance(inner_value, int):
                inner_value = str(inner_value)
            yaml_output += "  " + inner_key + ": " + inner_value + "\n"
    return yaml_output