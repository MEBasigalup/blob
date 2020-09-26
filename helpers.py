def lines(a, b):
    """Return lines in both a and b"""
    """Separate files by lines"""
    list_a = a.splitlines()
    list_b = b.splitlines()

    """Check that lines in both lists are equal"""
    lines = []
    for x in list_a:
        for y in list_b:
            if x == y:
                """Check for duplicates"""
                if lines.count(x) == 0:
                    lines.append(x)
    return lines


def sentences(a, b):
    """Return sentences in both a and b"""
    from nltk.tokenize import sent_tokenize

    """Separate files by sentences"""
    list_a = sent_tokenize(a)
    list_b = sent_tokenize(b)

    """Check that sentences in both lists are equal"""
    sentences = []
    for x in list_a:
        for y in list_b:
            if x == y:
                """Check for duplicates"""
                if sentences.count(x) == 0:
                    sentences.append(x)
    return sentences


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    """Create lists"""
    list_a = []
    list_b = []

    """Check for strings shorter in length than n"""
    if n <= len(a):
        """Separate by substrings of length n"""
        for i in range(len(a)-n+1):
            list_a.append(a[i:i+n])

    if n <= len(b):
        """Separate by substrings of length n"""
        for i in range(len(b)-n+1):
            list_b.append(b[i:i+n])

    substrings = []
    """Check that substrings are equal"""
    for x in list_a:
        for y in list_b:
            if x == y:
                """Check for duplicates"""
                if substrings.count(x) == 0:
                    substrings.append(x)
    return substrings
