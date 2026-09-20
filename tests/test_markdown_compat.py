"""Regression checks for authoring syntax accepted by the blog."""

from pathlib import Path
import tomllib
import unittest

import markdown


class MarkdownCompatibilityTests(unittest.TestCase):
    def render(self, text):
        config = tomllib.loads(
            (Path(__file__).resolve().parents[1] / "zensical.toml").read_text(encoding="utf-8")
        )["project"]["markdown_extensions"]
        names = ["pymdownx.arithmatex", "blog_markdown",
                 "pymdownx.superfences"]
        return markdown.markdown(
            text, extensions=names, extension_configs={name: config[name] for name in names}
        )

    def test_list_without_blank_line(self):
        html = self.render("Paragraph:\n* first\n* second")
        self.assertIn("<ul>", html)
        self.assertEqual(html.count("<li>"), 2)

    def test_ordered_list_without_blank_line(self):
        self.assertIn("<ol>", self.render("Steps:\n1. first\n2. second"))

    def test_same_line_display_math(self):
        html = self.render(r"At least $$\lceil \frac{h-kB}{A-B} \rceil$$ times.")
        self.assertIn(r'\[\lceil \frac{h-kB}{A-B} \rceil\]', html)
        self.assertNotIn("$", html)

    def test_standard_math(self):
        self.assertIn(r'\(x_i\)', self.render("Value $x_i$."))
        self.assertIn('<div class="arithmatex">', self.render("$$\nx_i\n$$"))

    def test_inline_code_untouched(self):
        html = self.render("`$$x_i$$` and `$x_i$`")
        self.assertIn("<code>$$x_i$$</code>", html)
        self.assertNotIn('class="arithmatex"', html)

    def test_fenced_code_untouched(self):
        html = self.render("```text\nparagraph\n* literal\n$$x_i$$\n```")
        self.assertNotIn("<ul>", html)
        self.assertNotIn('class="arithmatex"', html)
        self.assertIn("$$x_i$$", html)

    def test_escaped_dollars_untouched(self):
        self.assertNotIn('class="arithmatex"', self.render(r"\$\$x\$\$"))

    def test_indented_code_untouched(self):
        html = self.render("    paragraph\n    * literal\n    $$x_i$$")
        self.assertIn("paragraph\n* literal\n$$x_i$$", html)
        self.assertNotIn("<ul>", html)

    def test_fence_preserves_line_spacing(self):
        html = self.render("```\nparagraph\n* literal\n```")
        self.assertIn("paragraph\n* literal", html)

    def test_adjacent_inline_math(self):
        html = self.render(r"$a$$\cdots$$b$")
        self.assertEqual(html.count('class="arithmatex"'), 3)


if __name__ == "__main__":
    unittest.main()
