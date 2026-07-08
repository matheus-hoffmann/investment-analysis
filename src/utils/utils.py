def normalize_list(l: list):
    min_val = min(l)
    max_val = max(l)
    return [(val - min_val) / (max_val - min_val) for val in l]

def inverse_normalize_list(l: list):
    min_val = min(l)
    max_val = max(l)
    return [(max_val - val) / (max_val - min_val) for val in l]