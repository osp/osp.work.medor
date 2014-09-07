import re
import lxml
import codecs
import html5lib
import requests
from django import template
from django.conf import settings
from urlparse import parse_qsl, urlparse
import os.path
from hashlib import sha1
from django.utils.functional import curry
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def cache(url):
    name = sha1(url).hexdigest()
    path = os.path.join(settings.CACHE_PATH, name)

    if not os.path.exists(settings.CACHE_PATH):
        os.makedirs(settings.CACHE_PATH)

    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)

    return path


@register.filter
def tree(path):
    f = codecs.open(path, "r", "utf-8")
    html = f.read()

    parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
    tree = parser.parse(html, encoding=None, parseMeta=True, useChardet=True)

    return tree


@register.filter
def outline(tree, path=None):
    pattern = re.compile('^h(\d)')
    last_depth = None
    sections = [] # [header, <section />]

    if path:
        root = tree.xpath(path)[0]
    else:
        try:
            root = tree.getroot()
        except:
            root = tree

    for child in root.iterchildren():
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

    return tree


@register.filter
def cleanmw(tree):
    for elt in tree.xpath('//span[@class="editsection"]'):
        elt.getparent().remove(elt)

    for elt in tree.xpath('//span[@class="mw-headline"]'):
        parent = elt.getparent()
        parent.getparent().attrib['id'] = elt.attrib.pop('id')
        text = elt.text
        parent.remove(elt)
        parent.text = text

    for elt in tree.xpath('//section'):
        wrapper =  lxml.etree.Element('div')
        wrapper.attrib['class'] = 'wrapper'
        for child in elt.getchildren():
            wrapper.append(child)
        elt.append(wrapper)

    for elt in tree.xpath('//img'):
        if not elt.attrib['src'].startswith('http'):
            elt.attrib['src'] = 'http://tunakutafuta.be/' + elt.attrib['src']

    return tree



@register.filter
def xpath(tree, xpath):
    return tree.xpath(xpath)


@register.filter(is_safe=True)
def serialize(tree):
    tostring = curry(lxml.etree.tostring, method='xml', pretty_print=True, xml_declaration=None, encoding="utf-8")

    if isinstance(tree, list):
        ret = "\n".join([tostring(item) for item in tree])
    else:
        ret = tostring(tree)

    return mark_safe(ret)
