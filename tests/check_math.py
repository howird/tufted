#!/usr/bin/env python3
"""Compile the regression fixture and inspect actual Typst HTML (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class HTMLTree(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.root = ET.Element("document")
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = ET.SubElement(self.stack[-1], tag, dict(attrs))
        if tag not in {"meta", "link", "img", "br", "hr", "input", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, (self.stack[-1].tag, tag)
        self.stack.pop()

    def handle_data(self, data):
        node = self.stack[-1]
        node.text = (node.text or "") + data


class MathHTMLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "math.html"
            subprocess.run([
                "typst", "compile", "--root", str(ROOT),
                "--features", "html", "--format", "html",
                str(ROOT / "tests/math.typ"), str(output),
            ], check=True)
            cls.html = HTMLTree(output.read_text()).root

    def test_native_math_and_numbering(self):
        self.assertEqual(len(self.html.findall(".//math")), 5)
        self.assertIsNotNone(self.html.find(".//math/msup"))
        self.assertEqual(len(self.html.findall(".//mtable/mtr")), 2)
        numbers = self.html.findall(".//div[@class='math-number']")
        self.assertEqual([n.text for n in numbers], ["(1)", "[ii]", "(4)"])
        # Unnumbered displays stay native and do not consume the counter.
        self.assertEqual(len(self.html.findall(".//math[@display='block']")), 4)

    def test_references_and_unique_anchors(self):
        ids = [n.get("id") for n in self.html.iter() if n.get("id")]
        self.assertEqual(len(ids), len(set(ids)))
        for anchor, number in [
            ("native-first", "(1)"), ("custom-number", "[ii]"),
            ("svg-equation", "(3)"), ("native-last", "(4)"),
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, ids)
                links = self.html.findall(f".//a[@href='#{anchor}']")
                self.assertEqual([n.text for n in links], [number])

    def test_svg_fallback(self):
        self.assertIsNotNone(self.html.find(".//span[@class='math-svg']/svg"))
        figure = self.html.find(".//figure[@id='svg-equation']")
        self.assertEqual(figure.get("role"), "math")
        self.assertIsNotNone(figure.find("svg"))
        self.assertEqual(len(self.html.findall(".//svg")), 2)
        self.assertIsNone(figure.find(".//math"))
        self.assertIsNone(figure.find(".//div[@class='math-number']"))

    def test_custom_head_retains_generated_mathml_css(self):
        head = self.html.find(".//head")
        self.assertEqual(head.find("title").text, "Math regression")
        self.assertIsNotNone(head.find("link[@href='/assets/tufted.css']"))
        styles = "\n".join(n.text or "" for n in head.findall("style"))
        self.assertIn("mtable.multiline-equation", styles)
        self.assertIn("math-style:", styles)


if __name__ == "__main__":
    unittest.main()
