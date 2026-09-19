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
tools/check-adoption
tools/check-floor
```

The first enforces what PEP 1 requires of a proposal and what the reference
publisher requires of the prose. The second holds this repository's own Python
to the standard [EEP 6](eeps/eep-0006.md) adopts, and skips if `pylint` is not
installed. The third checks the series' adoptions, as [EEP 8](eeps/eep-0008.md)
defines them: that EEP 1's substitution table still covers the PEP 1 revision it
pins, that every pinned file still resolves at its revision, and that a working
copy has not diverged from its upstream without saying so. It needs a network
and says so without one. The fourth decides this repository against the floor
[EEP 7](eeps/eep-0007.md) binds every repository to, and takes a path, so it
decides any other repository the same way. It needs `tools/floor` installed:

```sh
pip install -e tools/floor
```

Every rule in every check names the source it comes from, and a check that
cannot decide says which rule it could not run rather than reporting no
findings. `tests/run-fixtures` proves each of the 26 file-level rules can fail;
the seven repository-level rules and the three adoption rules have no fixture
and were provoked by hand. `tests/run-floor-fixtures` builds a repository for
each floor rule to fail on, and proves that a rule with no facts says nothing
rather than passing.

## The standard

[the standard](standard/STANDARD.md) is what building for Edison requires: the
rules that are in force, with no argument around them. It is generated from the
EEPs the council has accepted, so it is never edited directly.

Read an EEP when you want to know why a rule exists, or what was rejected on the
way to it. Read the standard when you want to know what to do.

## Where things are

- `eeps/` is the series: what was proposed, argued and decided.
- `standard/` is generated from it. Never edit it; change the EEP instead.
- `tools/` holds the checks, and `tools/pylintrc` the configuration EEP 6
  adopts. `pylint` run on its own will not find that file, so run
  `tools/check-python`, or pass `--rcfile=tools/pylintrc` yourself.
- `tools/floor/` holds EEP 7's floor as rules, and is the only part of the
  checks that has to be installed. It is a plugin to `repo-review`, which
  supplies the running and the reporting.
- `tests/` holds one fixture per file-level rule and the runners that prove
  each rule can fail.
- [DEPENDENCIES.md](DEPENDENCIES.md) records what this repository relies on
  that it did not write, and why.

## The series

The series is the files in [`eeps/`](eeps/). The header at the top of each file
is the truth about its status, type and author. This README does not repeat
them.

## Proposing something

EEP 1 says how. Most changes do not need a proposal.

## Code of conduct

[EEP 5](eeps/eep-0005.md) adopts one, by pin.
[CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md) says where to find it and where
a report goes.

## License

Public domain, or CC0-1.0-Universal, whichever is more permissive. That covers
the whole repository, the tools and this file included, and not only the EEPs.
[LICENSE](LICENSE) carries the text; each EEP repeats the notice in its own
Copyright section, as the adopted process requires.
