def escape(s):
    for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        s = s.replace(old, new)
    return s
