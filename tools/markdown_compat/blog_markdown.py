"""Accept same-line display math without bypassing Markdown's code protection."""

import re
from xml.etree import ElementTree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.util import AtomicString


class DisplayMath(InlineProcessor):
    def __init__(self, original, md):
        self.original = original
        # Keep original groups first: Arithmatex uses their numeric positions.
        # One combined pattern parses $a$$b$ from left to right, without
        # mistaking the two adjacent delimiters for the start of display math.
        display = r"(?<![\\$])\$\$(?!\$)(?P<display>[^\n]+?)(?<!\\)\$\$(?!\$)"
        super().__init__(original.pattern + "|" + display, md)

    def handleMatch(self, match, data):
        if match.group("display") is None:
            return self.original.handleMatch(match, data)
        element = ElementTree.Element("span", {"class": "arithmatex"})
        element.text = AtomicString(r"\[" + match.group("display").strip() + r"\]")
        return element, match.start(0), match.end(0)


class ParagraphList(BlockProcessor):
    # Run after fences, HTML, indented code and existing list/block processors,
    # but before paragraphs. Never rewrite the source or code-block contents.
    marker = re.compile(r"\n(?= {0,3}(?:[*+-] |1\. ))")

    def test(self, parent, block):
        return self.marker.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.marker.search(block)
        self.parser.parseBlocks(parent, [block[:match.start()]])
        blocks.insert(0, block[match.end():])


class BlogMarkdownExtension(Extension):
    def extendMarkdown(self, md):
        original = md.inlinePatterns["arithmatex-inline"]
        md.inlinePatterns.register(
            DisplayMath(original, md), "arithmatex-inline", 189.9,
        )
        md.parser.blockprocessors.register(ParagraphList(md.parser), "blog-paragraph-list", 15)


def makeExtension(**kwargs):
    return BlogMarkdownExtension(**kwargs)
