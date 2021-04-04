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

def get_hashtag(anime):
    '''Given an AniList anime object, returns the hashtag string to be used in tweets'''
    title = anime['title']['romaji']

    if 'Horimiya' in title:
        return '#horimiya ' + anime['hashtag']
    elif 'Haikyuu' in title:
        return '#haikyuu'
    elif 'Shingeki no Kyojin' in title:
        return '#shingeki #AttackOnTitan'
    elif 'One Piece' in title:
        return '#OnePiece'
    elif 'Bleach' in title:
        return '#Bleach'
    else:
        # No custom rule found, use default
        return anime['hashtag']
