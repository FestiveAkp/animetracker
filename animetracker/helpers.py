def ordinal(n):
    '''
    Converts integer to ordinal number: 3 -> 3rd
    https://leancrew.com/all-this/2020/06/ordinals-in-python/
    '''
    s = ('th', 'st', 'nd', 'rd') + ('th',)*10
    v = n%100
    if v > 13:
        return f'{n}{s[v%10]}'
    else:
        return f'{n}{s[v]}'
