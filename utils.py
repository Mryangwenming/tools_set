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

# 签名函数
def sign(public_data, json_data, app_secret):
    args = []
    json_data.update(public_data)
    for k in sorted(json_data.keys()):
        v = json_data.get(k)
        if v is None or v == '' or isinstance(v, list) or isinstance(v, dict):
            continue
        args.append('{}={}'.format(k, v))
    sign_str = '&'.join(args)
    sign = hmac.new(app_secret.encode(), sign_str.encode(), hashlib.sha1)
    this_sign = sign.hexdigest()
    return this_sign.upper()
