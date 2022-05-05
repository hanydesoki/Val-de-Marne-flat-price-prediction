import math

def distance_coords(m1, m2, r=6371):
    '''Calculate distance beetween coordinates (in km)'''

    phi1, lam1 = m1
    phi2, lam2 = m2

    phi1 = math.radians(phi1)
    phi2 = math.radians(phi2)
    lam1 = math.radians(lam1)
    lam2 = math.radians(lam2)

    return 2 * r * math.asin(
        math.sqrt(math.sin((phi2 - phi1) / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin((lam2 - lam1) / 2) ** 2))

def convert_kj_kcal(e_kj):
    '''Convert kilojoule to kilocal'''
    e_kcal = e_kj/4.184
    return e_kcal

def weights_sum(values, weights=None):
    '''Return sum of values with weights'''

    if weights is None:
        return sum(values)

    a = len(values)
    b = len(weights)

    if a != b:
        raise IndexError(f'values ({a}) and weights ({b}) must be same lenght')

    return sum([v * w for v, w in zip(values, weights)])


def digitin(string):
    for char in string:
        if char.isdigit():
            return True
    return False
