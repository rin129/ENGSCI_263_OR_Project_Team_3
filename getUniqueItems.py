# ENGSCI 263
# OR Project, Team 03

# This a helper function for route generation

def getUniqueItems(array):

    '''
    This is a helper function for route generation function
    It removes all duplicates of a certain item if they exist in a list or an array

    Inputs: 
    
            array
            a list or array that the user wants to clean

    Outputs: 
    
            results
            a list or array that does not contain any duplicates

    '''

    seen = set()
    result = []
    for item in array:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result