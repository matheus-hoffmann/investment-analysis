def normalize_list(l: list):
    min_val = min(l)
    max_val = max(l)
    return [(val - min_val) / (max_val - min_val) for val in l]

def inverse_normalize_list(l: list):
    min_val = min(l)
    max_val = max(l)
    return [(max_val - val) / (max_val - min_val) for val in l]

def increment_version(current_version: str, patch_limit: int = 99, minor_limit: int = 99) -> str:
    """
    Increments a version string in the 'Major.Minor.Patch' format based on configurable limits.
    """
    # Split the version string into a list of integers: [major, minor, patch]
    major, minor, patch = map(int, current_version.split('.'))
    
    # Increment the lowest unit (Patch)
    patch += 1
    
    # Check if Patch exceeded the configured limit
    if patch > patch_limit:
        patch = 0
        minor += 1  # Overflow to Minor
        
        # Check if Minor exceeded the configured limit
        if minor > minor_limit:
            minor = 0
            major += 1  # Overflow to Major
            
    # Return the formatted version string
    return f"{major}.{minor}.{patch}"

def get_highest_version_index(data_list: list, version_key: str) -> int:
    """
    Finds the index of the dictionary that contains the highest version string.
    """
    if not data_list:
        return -1
    
    # Find the dictionary with the maximum version based on the parsed tuple
    highest_version_item = max(data_list, key=lambda x: tuple(map(int, x.get(version_key, "0.0.0").split('.'))))
    
    # Return the index of that dictionary in the original list
    return data_list.index(highest_version_item)