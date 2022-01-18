import parse_url
import android_color
import datetime
import pytz

class Card:
    def __init__(
            self,
            store='',
            note='',
            cardid='',
            barcodeid=None,
            barcodetype=None,
            balance=None,
            balancetype=None,
            expiry=-1,
            headercolor=None,
            ):
        self.store = store
        self.note = note
        self.cardid = cardid
        self.balance = balance
        self.balancetype = balancetype

        self.headercolor = None if headercolor is None else android_color.AndroidColor(int(headercolor))
        if not expiry:
            expiry = -1
        self._expiry_datetime = datetime.datetime.fromtimestamp(int(expiry), datetime.timezone.utc)

        self._barcodeid = barcodeid
        self.barcodetype = barcodetype
        self._barcodeid_tracks_cardid = barcodeid in (None, '',)

    @property
    def has_barcode(self):
        return self.barcodetype is not None

    def _get_barcodeid_tracks_cardid(self):
        return self._barcodeid_tracks_cardid

    def _set_barcodeid_tracks_cardid(self, value):
        old = self._barcodeid_tracks_cardid
        self._barcodeid_tracks_cardid = value
        if value != old:
            self._barcodeid = self.cardid

    barcodeid_tracks_cardid = property(
            _get_barcodeid_tracks_cardid,
            _set_barcodeid_tracks_cardid
            )

    def _get_barcodeid(self):
        if self.barcodeid_tracks_cardid:
            return self.cardid
        else:
            return self._barcodeid

    def _set_barcodeid(self, barcodeid):
        self.barcodeid_tracks_cardid = False
        self._barcodeid = barcodeid

    barcodeid = property(_get_barcodeid, _set_barcodeid)

    @property
    def url(self):
        data = {}
        data['store'] = self.store
        data['note'] = self.note
        data['cardid'] = self.cardid

        if self.balance is not None:
            data['balance'] = self.balance

        if self.balancetype is not None:
            data['balancetype'] = self.balancetype

        if self.barcodetype is not None:
            data['barcodetype'] = self.barcodetype

        if not self.barcodeid_tracks_cardid:
            data['barcodeid'] = self.barcodeid

        if self.has_expiry:
            data['expiry'] = str(self.expiry)

        if self.headercolor is not None:
            data['headercolor'] = str(self.headercolor)

        return parse_url.generate_url(data)

    def _get_expiry(self):
        if self.has_expiry:
            return int(self.expiry_datetime.timestamp())
        else:
            raise AttributeError('card has no expiry date')

    def _set_expiry(self, expiry):
        self.expiry_datetime = datetime.datetime.fromtimestamp(expiry, datetime.timezone.utc)

    def _del_expiry(self):
        self.expiry = -1

    expiry = property(_get_expiry, _set_expiry, _del_expiry)

    def _get_expiry_datetime(self):
        if self.has_expiry:
            return self._expiry_datetime
        else:
            raise AttributeError('card has no expiry date')

    def _set_expiry_datetime(self, expiry_datetime):
        try:
            self._expiry_datetime = pytz.utc.localize(expiry_datetime)
        except ValueError:
            self._expiry_datetime = expiry_datetime.astimezone(datetime.timezone.utc)

    expiry_datetime = property(_get_expiry_datetime, _set_expiry_datetime)

    @property
    def has_expiry(self):
        return self.expiry != -1

    @staticmethod
    def from_url(url):
        return Card(**parse_url.split_url(url))
