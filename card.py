import parse_url
import android_color

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
            expiry=None,
            headercolor=None,
            ):
        # TODO: expiry is currently ignored
        self.store = store
        self.note = note
        self.cardid = cardid
        self.balance = balance
        self.balancetype = balancetype

        self.headercolor = android_color.AndroidColor(headercolor)

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

        return parse_url.generate_url(data)

    @staticmethod
    def from_url(url):
        return Card(**parse_url.split_url(url))
