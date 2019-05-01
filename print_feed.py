def pretty_print(value, indentation):
    if isinstance(value, dict):
        for field in value:
            print(indentation, field, sep="")
            pretty_print(value[field], indentation + "    ")
    elif isinstance(value, list):
        index = 0
        for element in value:
            print(indentation, "[", index, "]", sep="")
            index += 1
            pretty_print(element, indentation + "    ")
    elif value:
        print(indentation + str(value))
