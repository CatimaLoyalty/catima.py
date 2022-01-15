from urllib.parse import urlparse, parse_qs, unquote, quote, urlencode

class CatimaURLSyntaxError(BaseException):
    pass

def split_url(url):
    parsed_url = urlparse(url)

    path = parsed_url.path
    if not path.endswith('/'):
        path += '/'

    if not (parsed_url.netloc, path,) in (
            ('catima.app', '/share/',),
            ('thelastproject.github.io', '/Catima/share/',),
            ('brarcher.github.io', '/loyalty-card-locker/share/',),
            ):
        raise CatimaURLSyntaxError('invalid host or path')

    data = parsed_url.fragment or parsed_url.query
    if data == '':
        raise CatimaURLSyntaxError('no data')

    parsed_data = parse_qs(unquote(data))

    return {k:v[0] for k, v in parsed_data.items()}

def generate_url(data, base_url='https://catima.app/share/', query=False):
    encoded_data = quote(urlencode(data))
    separator = '?' if query else '#'
    return f'{base_url}{separator}{encoded_data}'
