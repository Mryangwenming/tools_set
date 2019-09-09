def get_nest_key(dict1, res=None):
    if res is None:
        res = []
    for key, value in dict1.items():
        res.append(key)
        if isinstance(value, dict):
            for _ in get_nest_key(value, res):
                yield res
        else:
            res.append(value)
            yield res
