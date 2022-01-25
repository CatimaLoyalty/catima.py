from urllib.parse import urlparse, parse_qs, unquote, quote, urlencode


class CatimaURLSyntaxError(BaseException):
    pass


def split_url(url):
    parsed_url = urlparse(url)

    path = parsed_url.path
    if not path.endswith("/"):
        path += "/"

    if not (parsed_url.netloc, path,) in (
        (
            "catima.app",
            "/share/",
        ),
        (
            "thelastproject.github.io",
            "/Catima/share/",
        ),
        (
            "brarcher.github.io",
            "/loyalty-card-locker/share/",
        ),
    ):
        raise CatimaURLSyntaxError("invalid host or path")

    data = parsed_url.fragment or parsed_url.query
    if data == "":
        raise CatimaURLSyntaxError("no data")

    parsed_data = parse_qs(unquote(data))

    return {k: v[0] for k, v in parsed_data.items()}

def generate_url(card, base_url="https://catima.app/share/", query=False):
    data = {}
    data["store"] = card.store
    data["note"] = card.note
    data["cardid"] = card.cardid

    if card.balance is not None:
        data["balance"] = card.balance

    if card.balancetype is not None:
        data["balancetype"] = card.balancetype

    if card.barcodetype is not None:
        data["barcodetype"] = card.barcodetype

    if not card.barcodeid_tracks_cardid:
        data["barcodeid"] = card.barcodeid

    if card.has_expiry:
        data["expiry"] = str(card.expiry)

    data["headercolor"] = str(card.headercolor)

    encoded_data = quote(urlencode(data))
    separator = "?" if query else "#"
    return f"{base_url}{separator}{encoded_data}"
