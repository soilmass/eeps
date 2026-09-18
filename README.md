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
```

The checker enforces what PEP 1 requires of a proposal and what the reference
publisher requires of the prose. Every rule in it names the source it comes
from. `tests/run-fixtures` proves each rule can fail.

## The series

The series is the files in [`eeps/`](eeps/). The header at the top of each file
is the truth about its status, type and author. This README does not repeat
them.

## Proposing something

EEP 1 says how. Most changes do not need a proposal.

## License

See the Copyright section of each EEP.
