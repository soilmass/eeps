# Dependencies

What this repository relies on that it did not write, and why. One entry
per direct dependency. A transitive dependency arrives with its parent
and gets no entry of its own.

The form is the one EEP 9 proposes: a field for each step of the
decision, so that a step whose result was never written down cannot pass
for one that was taken.

**EEP 9 is a draft and binds nothing.** It is open as a pull request at
`https://github.com/soilmass/eeps/pull/21` and the council has not
decided it. This file is written to its form anyway, because EEP 9 names
exactly this as what it is waiting for: "the first dependency decided
under this document and recorded". If the council rejects EEP 9, this
file goes with it.

One field of that form, the gate, has no content here. EEP 9 leaves the
gate vacant deliberately, and says what that costs: until an adoption
fills it, eligibility rests on the judgment of whoever is building. That
is what happened below, and it is written down rather than dressed up.

## repo-review

**What it is, what it is needed for, and why it could not be avoided.**
`repo-review` is a framework for running checks against a repository,
published by the Scientific Python project under BSD-3-Clause. It is
needed because EEP 7 binds every repository Edison owns to a floor and
nothing measured any repository against it. It could not be avoided by
anything this repository already depends on: before this change the
repository had no installed dependency at all, and its one checker,
`tools/check-eeps`, derives the repository from its own file location,
so it can only ever check the repository it lives in.

**What was considered, and the judgment.** Thirty-seven candidates were
surveyed across repository policy linters, general policy engines,
platform configuration and hook frameworks. The closest by description,
`repolinter`, is archived: its last commit is titled "Archiving
Repolinter". Of six candidates verified against their sources, the best
could express two of the obligations it was measured against. Two
constraints did the
killing. EEP 7 requires that "every rule the command enforces names the
source it comes from", and Scorecard, Allstar and CLOMonitor have no
field anywhere that can hold a citation. EEP 7's evidence for its own
last obligation is the output of `git log main --first-parent
--no-merges`, and no surveyed tool can run an arbitrary command.

`repo-review` was the only candidate that met all four constraints, and
it was verified by running it rather than by reading about it: `url` is a
documented optional member of its `Check` protocol and survives into
JSON output on a pass as well as a failure; `None` is a documented skip,
distinct from a pass; it takes the repository as an argument, so it needs
no network, no token and no public repository; and it exits 0 on success
and 3 on failure, so it can itself be the command EEP 7 asks every
repository to have.

The gate was vacant, so this judgment is the builder's and rests on
nothing written. That is EEP 9's stated weakness and this entry is an
instance of it.

**The decision.** Used, not written. Two defects were found and are
carried rather than hidden. `pip install repo-review` produces an entry
point that cannot start, because `rich` is in the `cli` extra and not in
the base requirement, so `tools/floor` depends on `repo-review[cli]`.
And `repo-review` exits 0 when a rule is skipped, which claims a decision
it did not make; `tools/check-floor` says which rules were not decided
and why, because `repo-review` has nowhere to record a reason.

What Edison writes is `tools/floor`: the rules themselves, which are
claims about Edison's law rather than about anyone's open-source
hygiene, and which nothing ships or ever will.

**How it serves the one idea.** EEP 2 asks that what every project gets
is written once and that nothing be added that is of no use. The floor
was written once, in EEP 7, and until now no repository could be held to
it. This is the smallest thing that makes the rule enforceable, and the
part of it Edison maintains is only the part that states Edison's rules.
