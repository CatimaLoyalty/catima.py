import android_color
import datetime

class IndependentCard:
    def __init__(
        self,
        store,
        note,
        cardid,
        barcodeid="",
        barcodetype="",
        balance="",
        balancetype="",
        expiry="",
        headercolor="",
    ):
        self.store = store
        self.note = note
        self.cardid = cardid

        self.barcodeid = barcodeid
        self.barcodetype = barcodetype

        self.balance = balance
        self.balancetype = balancetype

        self.expiry = expiry

        self.headercolor = headercolor

    @property
    def has_barcode(self):
        return self.barcodetype != ''

    def _get_barcodeid_tracks_cardid(self):
        return self._barcodeid == ''

    def _set_barcodeid_tracks_cardid(self, new):
        new = bool(new)
        if self.barcodeid_tracks_cardid == new:
            return
        
        if new:
            del self.barcodeid
        else:
            self.barcodeid = self.cardid

    barcodeid_tracks_cardid = property(_get_barcodeid_tracks_cardid, _set_barcodeid_tracks_cardid)

    def _get_barcodeid(self):
        if self.barcodeid_tracks_cardid:
            return self.cardid
        else:
            return self._barcodeid

    def _set_barcodeid(self, new):
        self._barcodeid = new

    def _del_barcodeid(self):
        self._barcodeid = ''

    barcodeid = property(_get_barcodeid, _set_barcodeid, _del_barcodeid)

    @property
    def has_balance(self):
        return self._balance is not None

    def _get_balance(self):
        return self._balance

    def _set_balance(self, new):
        if new is None:
            self._balance = None
        else:
            self._balance = float(new)

    def _del_balance(self):
        self.balance = None

    balance = property(_get_balance, _set_balance, _del_balance)

    def _get_headercolor(self):
        return android_color.AndroidColor(self._headercolor)

    def _set_headercolor(self, new):
        self._headercolor = android_color.AndroidColor(new)

    headercolor = property(_get_headercolor, _set_headercolor)
    
    def _get_expiry_datetime(self):
        return datetime.datetime.fromtimestamp(self.expiry, tz=datetime.timezone.utc)

    expiry_datetime = property(_get_expiry_datetime)
