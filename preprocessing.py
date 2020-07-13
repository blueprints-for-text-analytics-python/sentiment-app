import re
import html

# tags like <tab>
RE_TAG = re.compile(r'<[^<>]*>')
# markdown URLs, like [Some text](https://....)
RE_MD_URL = re.compile('\[([^\[\]]*)\]\([^\(\)]*\)')
# text or code in brackets like [0]
RE_BRACKET = re.compile('\[[^\[\]]*\]')
# standalone sequences of specials, matches &# but not #cool
RE_SPECIAL = re.compile(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)')
# standalone sequences of hyphens like --- or ==
RE_HYPHEN_SEQ = re.compile(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)')
# sequences of white spaces
RE_MULTI_SPACE = re.compile('\s+')

def clean(text):
    # convert html escapes like &amp; to characters.
    text = html.unescape(text)
    text = RE_TAG.sub(' ', text)
    text = RE_MD_URL.sub(r'\1', text)
    text = RE_BRACKET.sub(' ', text)
    text = RE_SPECIAL.sub(' ', text)
    text = RE_HYPHEN_SEQ.sub(' ', text)
    text = RE_MULTI_SPACE.sub(' ', text)
    return text.strip()
