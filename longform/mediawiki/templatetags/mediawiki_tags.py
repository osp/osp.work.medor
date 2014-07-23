import re
import lxml
import codecs
import html5lib
import requests
from django import template
from django.conf import settings
from urlparse import parse_qsl, urlparse
import os.path

register = template.Library()


def cache(URL):
    qs = parse_qsl(urlparse(URL).query)
    title = dict((x, y) for x, y in qs)['title']
    filename = os.path.join(settings.CACHE_PATH, title)

    if not os.path.exists(settings.CACHE_PATH):
        os.makedirs(settings.CACHE_PATH)

    if not os.path.exists(filename):
        r = requests.get(URL)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)

    return filename


def outline(tree):
    pattern = re.compile('^h(\d)')
    last_depth = None
    sections = [] # [header, <section />]

    for child in tree.iterchildren():
        tag = child.tag

        if tag is lxml.etree.Comment:
            continue

        match = pattern.match(tag.lower())

        if match:
            depth = int(match.group(1))

            if depth <= last_depth or last_depth is None:
                last_depth = depth

                sections.append([child, lxml.etree.Element('section')])
                continue

        if sections:
            sections[-1][1].append(child)

    for section in sections:
        outline(section[1])
        section[0].addprevious(section[1])
        section[1].insert(0, section[0])


def extract(src, id):
    f = codecs.open(src, "r", "utf-8")
    html = f.read()

    parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
    tree = parser.parse(html, encoding=None, parseMeta=True, useChardet=True)

    outline(tree.xpath("//div[@id='mw-content-text']")[0])

    for elt in tree.xpath('//span[@class="editsection"]'):
        elt.getparent().remove(elt)

    for elt in tree.xpath('//span[@class="mw-headline"]'):
        parent = elt.getparent()
        parent.getparent().attrib['id'] = elt.attrib.pop('id')
        text = elt.text
        parent.remove(elt)
        parent.text = text

    for elt in tree.xpath('//img'):
        elt.attrib['src'] = 'http://tunakutafuta.be/' + elt.attrib['src']

    #walker = html5lib.getTreeWalker("lxml")
    #stream = walker(tree)

    #serializer = html5lib.serializer.HTMLSerializer(quote_attr_values=True, omit_optional_tags=False)
    #output = serializer.render(stream)

    try:
        frag = lxml.etree.tostring(tree.xpath("//section[@id='%s']" % id)[0], method='xml', pretty_print=True, xml_declaration=None, encoding="utf-8")
    except IndexError:
        print('There is no section with id "%s"' % id)
    return frag


def mwinclude(name, id):
    src = cache('http://tunakutafuta.be/index.php?title=%s' % name)
    section = extract(src, id)
    return section


register.simple_tag(mwinclude)
