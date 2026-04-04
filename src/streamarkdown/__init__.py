import sys

from markdown_it import MarkdownIt
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown, TextElement
from rich.text import Text
from rich.theme import Theme


class MyHeading(TextElement):
    @classmethod
    def create(cls, _, token):
        return cls(token.tag)

    def on_enter(self, context) -> None:
        self.text = Text()
        context.enter_style("bold")

    def __init__(self, tag) -> None:
        self.tag = tag
        super().__init__()

    def __rich_console__(self, _console, _options):
        text = Text("".join("#" for _ in range(int(self.tag[1:]))))
        text.stylize("yellow")
        text.stylize("bold")
        text.append(" ")
        text.append_text(self.text)
        yield text


Markdown.elements["heading_open"] = MyHeading

console = Console(
    theme=Theme(
        {
            "markdown.block_quote": "violet",
            "markdown.hr": "medium_purple4",
            "markdown.link_url": "sky_blue1",
        }
    )
)


def full(string):
    console.print(Markdown(string))


def stream(strings) -> str:
    whole_string = ""
    current_block = ""

    def flatten_strings(strings):
        for string in strings:
            for char in string:
                yield char

    def block_recognized():
        nonlocal current_block
        md = MarkdownIt("js-default")
        tokens_len = 0
        for char in flatten_strings(strings):
            current_block += char
            tokens = md.parse(current_block)
            new_block = (
                tokens_len != len(tokens)
                and current_block[-3:][:2] == "\n\n"
                and char not in "-*123456789|"
            )
            tokens_len = len(tokens)
            yield (char, new_block)

    def new_live() -> Live:
        live = Live(console=console, refresh_per_second=10)
        live.start()
        return live

    live = new_live()

    for char, new_block in block_recognized():
        if new_block:
            current_block = char
            live.stop()
            console.print("")
            live = new_live()

        whole_string += char
        live.update(Markdown(current_block))

    live.stop()

    return whole_string


def main() -> None:
    stream(sys.stdin)
