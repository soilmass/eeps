# Edison Enhancement Proposals

This repository holds the EEP series: how anything that binds more than one
Edison project, or changes how Edison works, gets proposed, decided and
recorded.

## Start here

1. Read [EEP 1](eeps/eep-0001.md). It adopts Python's PEP 1 as Edison's process
   and says how to read it.
2. Read [EEP 2](eeps/eep-0002.md). It says what Edison is and the rule
   everything built on it follows.

If you are an agent, each of those two documents has a section called "How to
teach this". Follow both.

## Writing one

[EEP 3](eeps/eep-0003.md) holds the template. Copy the skeleton at the end of
it, fill it in, and check your work:

```sh
tools/check-eeps
tools/check-python
```

The first enforces what PEP 1 requires of a proposal and what the reference
publisher requires of the prose. The second holds this repository's own Python
to the standard [EEP 6](eeps/eep-0006.md) adopts, and skips if `pylint` is not
installed. Every rule in it names the source it comes from. `tests/run-fixtures`
proves each rule can fail.

## The series

The series is the files in [`eeps/`](eeps/). The header at the top of each file
is the truth about its status, type and author. This README does not repeat
them.

## Proposing something

EEP 1 says how. Most changes do not need a proposal.

## Code of conduct

[EEP 5](eeps/eep-0005.md) adopts one, by pin.
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) says where to find it and where a
report goes.

## License

Public domain, or CC0-1.0-Universal, whichever is more permissive. That covers
the whole repository, the tools and this file included, and not only the EEPs.
[LICENSE](LICENSE) carries the text; each EEP repeats the notice in its own
Copyright section, as the adopted process requires.
