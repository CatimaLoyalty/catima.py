import android_color
import datetime


class IndependentCard:
    """

    Represents a card that is independent of any other cards, e.g. a card
    decoded from a URL.
    
    """

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
        starstatus="0",
    ):
        self.store = store
        self.note = note
        self.cardid = cardid

        self.barcodeid = barcodeid
        self.barcodetype = barcodetype

        self.balance = balance
        self.balancetype = balancetype

        try:
            self.expiry = expiry
        except ValueError:
            self.expiry = None

        try:
            self.headercolor = headercolor
        except ValueError:
            self.headercolor = 0xFF0000FF  # blue as an Android color

        try:
            self.starstatus = starstatus
        except ValueError:
            self.starstatus = "0"

    def store_value(self, key, value):
        print(key, value)

    def _get_store(self):
        return self._store

    def _set_store(self, new):
        self._store = str(new)
        self.store_value('store', str(new))

    store = property(_get_store, _set_store)

    def _get_note(self):
        return self._note

    def _set_note(self, new):
        self._note = str(new)
        self.store_value('note', str(new))

    note = property(_get_note, _set_note)

    def _get_cardid(self):
        return self._cardid

    def _set_cardid(self, new):
        self._cardid = str(new)
        self.store_value('cardid', str(new))

    cardid = property(_get_cardid, _set_cardid)

    @property
    def has_barcode(self):
        return self.barcodetype != ""

    def _get_barcodeid_tracks_cardid(self):
        return self._barcodeid == ""

    def _set_barcodeid_tracks_cardid(self, new):
        new = bool(new)
        if self.barcodeid_tracks_cardid == new:
            return

        if new:
            del self.barcodeid
        else:
            self.barcodeid = self.cardid

    barcodeid_tracks_cardid = property(
        _get_barcodeid_tracks_cardid, _set_barcodeid_tracks_cardid
    )

    def _get_barcodeid(self):
        if self.barcodeid_tracks_cardid:
            return self.cardid
        else:
            return self._barcodeid

    def _set_barcodeid(self, new):
        self.store_value('barcodeid', new)
        self._barcodeid = new

    def _del_barcodeid(self):
        self.barcodeid = ""

    barcodeid = property(_get_barcodeid, _set_barcodeid, _del_barcodeid)

    @property
    def has_balance(self):
        return self._balance is not None

    def _get_balance(self):
        return self._balance

    def _set_balance(self, new):
        if new is None or new == "":
            self._balance = None
            self.store_value('balance', '')
        else:
            self._balance = float(new)
            self.store_value('balance', str(float(new)))

    def _del_balance(self):
        self.balance = None

    balance = property(_get_balance, _set_balance, _del_balance)

    def _get_headercolor(self):
        return android_color.AndroidColor(self._headercolor)

    def _set_headercolor(self, new):
        self.store_value('headercolor', str(int(new)))
        self._headercolor = android_color.AndroidColor(new)

    headercolor = property(_get_headercolor, _set_headercolor)

    @property
    def has_expiry(self):
        return self.expiry is not None

    def _get_expiry(self):
        return self._expiry

    def _set_expiry(self, new):
        if new is None:
            self._expiry = None
            self.store_value('expiry', '')
        else:
            self._expiry = int(new)
            self.store_value('expiry', str(int(new)))

    def _del_expiry(self):
        self.expiry = None

    expiry = property(_get_expiry, _set_expiry, _del_expiry)

    def _get_expiry_datetime(self):
        return datetime.datetime.fromtimestamp(self.expiry, tz=datetime.timezone.utc)

    expiry_datetime = property(_get_expiry_datetime)

    def _get_starstatus(self):
        return self._starstatus

    def _set_starstatus(self, new):
        self._starstatus = str(int(bool(int(new))))
        self.store_value('starstatus', str(int(bool(int(new)))))

    starstatus = property(_get_starstatus, _set_starstatus)

    def _get_starstatus_bool(self):
        return bool(int(self.starstatus))

    # No need for _set_starstatus_bool because _set_starstatus can handle bool

    starstatus_bool = property(_get_starstatus_bool, _set_starstatus)
