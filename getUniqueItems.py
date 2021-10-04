def getUniqueItems(array):
    seen = set()
    result = []
    for item in array:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result