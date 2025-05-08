def compute_tk(t: float, toe: float) -> float:
    tk = t - toe
    while tk > 302400:
        tk -= 604800
    while tk < -302400:
        tk += 604800
    return tk
