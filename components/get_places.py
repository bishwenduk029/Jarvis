def get_place_from_phrase(phrase: str) -> str:
    """Looks for the name of a place in the phrase received.

    Args:
        phrase: Takes the phrase converted as an argument.

    Returns:
        str:
        Returns the name of place if skimmed.
    """
    place = ''
    for word in phrase.split():
        if word[0].isupper():
            place += word + ' '
        elif '.' in word:
            place += word + ' '
    if place:
        return place
