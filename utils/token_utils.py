def count_tokens(text):
    """
    Estimates token count. 
    Rule of thumb: 1 token ~= 4 chars in English.
    """
    if not text:
        return 0
    return len(text) / 4