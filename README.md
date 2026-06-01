# streamarkdown

Streaming markdown renderer for the terminal.

## Install with Homebrew

This repository includes a Homebrew tap formula:

```sh
brew tap kill-2/streamarkdown https://github.com/kill-2/streamarkdown
brew install streamarkdown
```

To install the latest `main` branch instead of the pinned release revision:

```sh
brew install --HEAD streamarkdown
```

## Usage

Pipe markdown into `streamarkdown`:

```sh
cat README.md | streamarkdown
```

## Updating the Homebrew formula

When cutting a new release:

1. Bump `version` in `pyproject.toml`.
2. Commit the release and note the commit SHA.
3. Update `Formula/streamarkdown.rb` with the new `version` and Git `revision`.
4. If dependencies changed, update the formula `resource` blocks.
5. Validate with `brew install --build-from-source kill-2/streamarkdown/streamarkdown` from a tapped checkout.
