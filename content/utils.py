import re
import unicodedata

from django.core.validators import RegexValidator

E_pun = u',.!?()'
C_pun = u'，。！？（）'
E2C_PUN_TABLE= {ord(f):ord(t) for f, t in zip(E_pun, C_pun)}
C2E_PUN_TABLE= {ord(f):ord(t) for f, t in zip(C_pun, E_pun)}


def punctuate_English(s):
    s = s.translate(C2E_PUN_TABLE)
    # guarantee space after punctuation
    s = re.sub(r'(?<=[,.!?])(?! |$)', r' ', s)
    return "%s%s" % (s[0].upper(), s[1:])


def punctuate_Chinese(s):
    s2 = s.translate(E2C_PUN_TABLE)
    # remove space after punctuation
    return re.sub(r'(?<=[，。！？]) +', r'', s)


CHINESE_CHAR_REGEX = "[\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-" \
                     "\u9FCC\uF900-\uFAAD\U00020000-\U0002A6D6]"
validate_chinese_character_or_x = RegexValidator(
    f'^(({CHINESE_CHAR_REGEX}+)|x)\Z',
    'this need to be either in Chinese or "x"'
)

def unaccent(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore'
                                                   ).decode('utf-8')


def add_highlight(s, *targets, add_all=False):
    """ returns (text, highlight_text)"""
    # if already manually highlighted, do nothing
    if re.search(r"<.*?>", s):
        return re.sub(r"<(.*?)>", r"\1", s), s
    highlight_s = s
    for target in targets:
        if not isinstance(target, (list, tuple)):
            target = [target]
        tot_sub = 0
        for t in target:
            highlight_s, num_sub = re.subn(f"({re.escape(t.strip())})", r'<\1>',
                                           highlight_s, flags=re.IGNORECASE)
            tot_sub += num_sub
        if tot_sub and not add_all:
            return s, highlight_s
    return s, highlight_s
