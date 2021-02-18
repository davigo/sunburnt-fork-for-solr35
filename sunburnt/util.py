import re
import urllib

__all__ = ['strip_invalid_xml_chars', 'unicode_urlencode']

_valid_patt = re.compile(u'[^\u0020-\uD7FF\x09\x0A\x0D'
                         u'\uE000-\uFFFD\ud800\udc00-\udbff\udfff]', re.U)

#FOR WINDOW SYSTEM
#_valid_patt = re.compile(u'[^\u0020-\uD7FF\x09\x0A\x0D\uE000-\uFFFD]', re.U)

def strip_invalid_xml_chars(s, substitute=u''):
    r'''Replace characters in a unicode string s that are forbidden by XML 1.0

    XML 1.0 only a allows a subset of Unicode characters in an XML document.
    Others (e.g. U+0000, U+0013) are invalid - they may not be included
    regardless of encoding or escaping. Valid characters are U+0009, U+000A,
    U+000D, U+0020-U+D7FF, U+E000-U+FFFD, U+10000-U+10FFFF.

    See <http://www.w3.org/TR/2008/PER-xml-20080205/#charsets>
    >>> strip_invalid_xml_chars(u'a\x00bc\x13d\tef\n ghi')
    u'abcd\tef\n ghi'
    '''
    return _valid_patt.sub(substitute, s)

# Adapted from trac.trac.util.text.unicode_urlencode()
def unicode_urlencode(params):
    """A unicode aware version of urllib.urlencode.
    """
    if isinstance(params, dict):
        params = params.iteritems()
    l = []
    for k, v in params:
        k = urllib.quote_plus(str(k))
        if isinstance(v, unicode):
            l.append(k + '=' + urllib.quote_plus(v.encode('utf-8')))
        else:
            l.append(k + '=' + urllib.quote_plus(str(v)))
    return '&'.join(l)
