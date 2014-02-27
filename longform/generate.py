#! /usr/bin/env python2


import codecs
import html5lib
import lxml
import re
import requests
import sys
import xml.etree.ElementTree as etree
from html5lib.filters import _base
from html5tidy import tidy
from lxml.html.clean import Cleaner


class OutlineFilter(_base.Filter):
    def __iter__(self):
        level = opened = 0

        for token in _base.Filter.__iter__(self):
            if token['type'] == 'StartTag' and token['name'] in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                current_level = int(token['name'][1:])

                if level and current_level <= level:
                    while opened:
                        yield {u'namespace': u'', u'type': u'EndTag', u'name': u'section', u'data': {}}
                        opened -= 1
                else:
                    level = current_level

                yield {u'namespace': u'', u'type': u'StartTag', u'name': u'section', u'data': {}}
                opened += 1
                yield token

            elif token['type'] == 'EndTag' and token['name'] == "body":
                while opened:
                    yield {u'namespace': u'', u'type': u'EndTag', u'name': u'section', u'data': {}}
                    opened -= 1
                yield token

            else:
                yield token

def outline(tree, level=0):
    pattern = re.compile('^h(\d)')
    last_depth = None
    sections = [] # [header, <section />]

    for child in tree.iterchildren():
        tag = child.tag

        if tag is lxml.etree.Comment:
            continue

        match = pattern.match(tag.lower())
        #print("%s%s" % (level * ' ', child))

        if match:
            depth = int(match.group(1))

            if depth <= last_depth or last_depth is None:
                #print("%ssection %d" % (level * ' ', depth))
                last_depth = depth

                sections.append([child, lxml.etree.Element('section')])
                continue

        if sections:
            sections[-1][1].append(child)

    for section in sections:
        outline(section[1], level=((level + 1) * 4))
        section[0].addprevious(section[1])
        section[1].insert(0, section[0])


def clean(tree):
    root = tree.getroot()

    for child in root.iterchildren():
        tag = child.tag
        if tag is lxml.etree.Comment:
            child.getparent().remove(tag)


def run():
    f = codecs.open("index.html", "r", "utf-8")
    html = f.read()
    #html = "<html><head></head><body><h2><span class='mw-headline' id='foo'>titre</span></h2></body></html>"
    #html = """
    #<html>
        #<head></head>
        #<body>
            #<p>introduction</p>
            #<h1>first heading</h1>
            #<p>some text</p>
            #<h2>first heading</h2>
            #<p>some text</p>
            #<h2>first heading</h2>
            #<p>some text</p>
            #<h1>first heading</h1>
            #<p>some text</p>
        #</body>
    #</html>
    #"""
    parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
    tree = parser.parse(html, encoding=None, parseMeta=True, useChardet=True)

    #clean(tree)

    # outline the content
    outline(tree.xpath("//div[@id='mw-content-text']")[0])

    for elt in tree.xpath('//span[@class="editsection"]'):
        elt.getparent().remove(elt)

    for elt in tree.xpath('//span[@class="mw-headline"]'):
        parent = elt.getparent()
        parent.getparent().attrib['id'] = elt.attrib.pop('id')
        text = elt.text
        parent.remove(elt)
        parent.text = text

    walker = html5lib.getTreeWalker("lxml")
    stream = walker(tree)
    #stream = OutlineFilter(stream)

    serializer = html5lib.serializer.HTMLSerializer(quote_attr_values=True, omit_optional_tags=False)
    output = serializer.render(stream)
    #sys.stdout.write(output.encode('utf-8'))

    frag = lxml.etree.tostring(tree.xpath("//section[@id='Naissance']")[0], method='xml', pretty_print=True, xml_declaration=None, encoding="utf-8")
    sys.stdout.write(frag)



if __name__ == "__main__":
    run()
