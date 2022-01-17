class AndroidColor(int):
    @property
    def argb_tuple(self):
        a = self >> 24 & 0xff
        r = self >> 16 & 0xff
        g = self >> 8 & 0xff
        b = self & 0xff
        return a, r, g, b
       
    @property
    def rgba_tuple(self):
        a, r, g, b = self.argb_tuple
        return r, g, b, a
       
    @property
    def rgb_tuple(self):
        _, r, g, b = self.argb_tuple
        return r, g, b
       
    @property
    def hex_rgb_string(self):
        string_end = hex(self & 0xFFFFFF)[2:]
        return ' ' * (6 - len(string_end)) + string_end

    @propery
    def css_rgb_string(self):
        r, g, b = self.rgb_tuple
        return f'rgb({r}, {g}, {b})'

    @propery
    def css_rgba_string(self):
        r, g, b, a_raw = self.rgba_tuple
        a = a_raw / 0xFF # Android stores alpha as 0...255; CSS uses 0.0...1.0
        return f'rgba({r}, {g}, {b}, {a})'

    @staticmethod
    def from_argb_tuple(argb):
        a, r, g, b = argb
        return AndroidColor((a<<24) | (r<<16) | (g<<8) | b)

    @staticmethod
    def from_rgba_tuple(rgba):
        r, g, b, a = rgba
        return AndroidColor.from_argb_tuple((a, r, g, b,))
