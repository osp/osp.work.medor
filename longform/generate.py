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

def outline(tree):
    pattern = re.compile('^h(\d)')
    section = None

    for child in tree.iterchildren():
        tag = child.tag

        if tag is lxml.etree.Comment:
            continue

        match = pattern.match(tag.lower())

        # If a header tag is found
        if match:

            if section:
                child.addprevious(section)

            section = lxml.etree.Element('section')
            section.append(child)

        else:
            if section:
                section.append(child)
            else:
                pass

        if child:
            outline(child)


    if section:
        tree.append(section)



def clean(tree):
    root = tree.getroot()

    for child in root.iterchildren():
        tag = child.tag
        if tag is lxml.etree.Comment:
            child.getparent().remove(tag)


def run():
    #f = codecs.open("index.html", "r", "utf-8")
    #html = f.read()
    #html = "<html><head></head><body><h2><span class='mw-headline' id='foo'>titre</span></h2></body></html>"
    html = """
    <html>
        <head></head>
        <body>
            <p>introduction</p>
            <h2>first heading</h2>
            <p>some text</p>
            <h1>second heading</h1>
        </body>
    </html>
    """
    parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
    tree = parser.parse(html, encoding=None, parseMeta=True, useChardet=True)

    clean(tree)
    outline(tree.find('body'))

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
    sys.stdout.write(output.encode('utf-8'))



if __name__ == "__main__":
    run()
