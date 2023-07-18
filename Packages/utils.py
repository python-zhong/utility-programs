def express_file_size(n: int) -> tuple[float, str]:
    from collections import namedtuple
    ExpressFunction = namedtuple('ExpressFunction', ['converter', 'suggester'])
    if not isinstance(n, int):
        raise TypeError('Expected int, got ', n.__class__.__name__)
    elif n < 0:
        raise ValueError('Got ' + str(n))
    data = {
        'Bytes': ExpressFunction(lambda n: n, lambda n: n < 2 ** 10),
        'KB'   : ExpressFunction(lambda n: n/(2**10), lambda n: n < 2 ** 20),
        'MB'   : ExpressFunction(lambda n: n/(2**20), lambda n: n < 2 ** 30),
        'GB'   : ExpressFunction(lambda n: n/(2**30), lambda n: n < 2 ** 40),
        'TB'   : ExpressFunction(lambda n: n/(2**40), lambda n: n < 2 ** 50),
        'PB'   : ExpressFunction(lambda n: n/(2**50), lambda n: n < 2 ** 60),
        'EB'   : ExpressFunction(lambda n: n/(2**60), lambda n: n < 2 ** 70),
        'ZB'   : ExpressFunction(lambda n: n/(2**70), lambda n: n < 2 ** 80),
        'YB'   : ExpressFunction(lambda n: n/(2**80), lambda n: n >= 2 ** 80),
    }
    for item, fn in data.items():
        if fn.suggester(n):
            return fn.converter(n), item
    return n, 'Bytes'