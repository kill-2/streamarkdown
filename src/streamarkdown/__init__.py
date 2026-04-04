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


class Stream:
    def __init__(self) -> None:
        self.current_block = ""
        self.tokens_len = 0
        self.markdown_parser = MarkdownIt("js-default")
        self.console = Console(
            theme=Theme(
                {
                    "markdown.block_quote": "violet",
                    "markdown.hr": "medium_purple4",
                    "markdown.link_url": "sky_blue1",
                }
            )
        )
        self.live = None

    def __call__(self, strings) -> None:
        if strings is None:
            self.__stop_live()
            return

        if not self.live:
            self.__start_live()

        def flatten_strings(strings):
            for string in strings:
                for char in string:
                    yield char

        def block_recognized():
            for char in flatten_strings(strings):
                self.current_block += char
                tokens = self.markdown_parser.parse(self.current_block)
                new_block = (
                    self.tokens_len != len(tokens)
                    and self.current_block[-3:][:2] == "\n\n"
                    and char not in "-*123456789|"
                )
                self.tokens_len = len(tokens)
                yield (char, new_block)

        for char, new_block in block_recognized():
            if new_block:
                self.__stop_live()
                self.current_block = char
                self.console.print("")
                self.__start_live()

            self.live.update(Markdown(self.current_block))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__stop_live()
        return False

    def __stop_live(self) -> None:
        if self.live:
            self.live.stop()
        self.live = None
        self.current_block = ""

    def __start_live(self) -> None:
        live = Live(console=self.console, refresh_per_second=10)
        live.start()
        self.live = live


def main() -> None:
    with Stream() as stream:
        stream(sys.stdin)
