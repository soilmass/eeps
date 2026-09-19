"""EEP 7's floor, as checks any repository can be measured against.

Every check here traces to one section of EEP 7, named in the class
docstring and linked from the ``url`` member, which is what EEP 7 asks
for: "Every rule the command enforces names the source it comes from, in
a comment above the rule or in the docstring of the function that holds
it.  A rule with no source does not belong in it."

Three of EEP 7's obligations have no check here, deliberately.  That a
rule names its source, that a rule was seen failing, and that what is
taken from outside is pinned rather than copied cannot be decided by
reading a repository from outside it.  A check that passed on them would
claim to have decided something it had not, which is the failure EEP 6
records about a green run without pylint.

A fixture gathers facts and returns None when it cannot.  A check
decides, and returns None when the facts it needs are absent.  EEP 7:
"Where a check cannot decide, because something it needs is absent, it
says which and does not claim to have decided."

Run through ``tools/check-floor``, which turns an undecided rule into a
distinct exit status.  ``repo-review`` alone exits 0 when a rule is
skipped, which claims a decision it did not make.
"""

import os
import pathlib
import re
import subprocess

try:
    import yaml
except ImportError:                                 # pragma: no cover
    yaml = None

EEP7 = "https://github.com/soilmass/eeps/blob/main/eeps/eep-0007.md"

# EEP 7, "The entry point": the README is the entry point, so it is the
# one path a file of instructions may name.
ENTRY_POINT = "README.md"

# Files whose job is to tell an agent how to work in the repository.
# EEP 7 binds them without listing them; these are the names in use.
AGENT_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    "GEMINI.md",
    os.path.join(".github", "copilot-instructions.md"),
)

# A tracked path that a tool produced by running.  The same list
# tools/check-eeps rule R007 refuses for this repository, which EEP 7
# generalises to every repository.
ARTEFACT_SUFFIXES = (".pyc", ".pyo")
ARTEFACT_PARTS = ("__pycache__/", ".ruff_cache/", ".mypy_cache/",
                  ".pytest_cache/")

# A token in an instruction file that looks like a path.  Backticks are
# how this series writes one.
PATH_TOKEN = re.compile(r"`([^`\s]+/[^`\s]*|[^`\s]+\.[A-Za-z0-9]{1,5})`")


# --- fixtures ----------------------------------------------------------


def repo(package):
    """The repository being checked, as a path on disk."""
    return pathlib.Path(str(package))


def tracked(repo):
    """Every path git tracks, or None when git cannot be asked.

    Returning None rather than an empty list is what keeps a check from
    reading "nothing is tracked" out of "this is not a repository".
    """
    # pylint: disable=redefined-outer-name
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "ls-files"],
            capture_output=True, text=True, check=False)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return [x for x in proc.stdout.split("\n") if x.strip()]


def default_branch(repo):
    """The repository's principal branch, or None when there is none.

    EEP 7 says "the main branch", meaning the one a change has to reach,
    not a branch that must be named main.  This rule read the name
    literally at first and skipped a real repository whose branch is
    master, reporting that it could not find a main branch when there
    was a default branch in front of it.
    """
    # pylint: disable=redefined-outer-name
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "symbolic-ref", "--short",
             "refs/remotes/origin/HEAD"],
            capture_output=True, text=True, check=False)
    except OSError:
        return None
    name = proc.stdout.strip()
    if proc.returncode == 0 and name:
        return name.split("/", 1)[-1]
    for candidate in ("main", "master"):
        shown = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", candidate],
            capture_output=True, text=True, check=False)
        if shown.returncode == 0:
            return candidate
    return None


def workflows(repo):
    """Every parsed workflow, or None when none can be read."""
    # pylint: disable=redefined-outer-name
    if yaml is None:
        return None
    directory = repo / ".github" / "workflows"
    if not directory.is_dir():
        return None
    parsed = []
    for path in sorted(directory.iterdir()):
        if path.suffix not in (".yml", ".yaml"):
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle)
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(loaded, dict):
            parsed.append(loaded)
    return parsed or None


def workflow_commands(workflows):
    """Every command a workflow runs, or None when none can be read."""
    # pylint: disable=redefined-outer-name
    if workflows is None:
        return None
    commands = []
    for flow in workflows:
        jobs = flow.get("jobs")
        if not isinstance(jobs, dict):
            continue
        for job in jobs.values():
            if not isinstance(job, dict):
                continue
            for step in job.get("steps") or []:
                if isinstance(step, dict) and "run" in step:
                    commands.append(str(step["run"]))
    return commands or None


def workflow_triggers(workflows):
    """What the workflows trigger on, or None when none can be read.

    YAML 1.1 reads a bare ``on`` as the boolean true, so the key this
    reaches for is True and not the string.  Checked against this
    repository's own workflow rather than assumed.
    """
    # pylint: disable=redefined-outer-name
    if workflows is None:
        return None
    triggers = set()
    for flow in workflows:
        raw = flow.get(True, flow.get("on"))
        if isinstance(raw, dict):
            triggers.update(str(k) for k in raw)
        elif isinstance(raw, list):
            triggers.update(str(k) for k in raw)
        elif raw is not None:
            triggers.add(str(raw))
    return triggers or None


# --- checks ------------------------------------------------------------


class Floor:
    """Shared family for every rule EEP 7's floor states."""

    family = "floor"


class F001(Floor):
    """EEP 7, "The entry point": a README.md in the root."""

    url = EEP7

    @staticmethod
    def check(repo):
        """EEP 7: "Every repository has a `README.md` in its root"."""
        # pylint: disable=redefined-outer-name
        return (repo / ENTRY_POINT).is_file()


class F002(Floor):
    """EEP 7, "The license": a LICENSE in the root."""

    url = EEP7

    @staticmethod
    def check(repo):
        """EEP 7: "Every repository has a `LICENSE` file in its root"."""
        # pylint: disable=redefined-outer-name
        return (repo / "LICENSE").is_file()


class F003(Floor):
    """EEP 7, "Written and generated are kept apart": no artefact."""

    url = EEP7

    @staticmethod
    def check(tracked):
        """EEP 7: what a tool produces is not tracked."""
        # pylint: disable=redefined-outer-name
        if tracked is None:
            return None
        for name in tracked:
            if name.endswith(ARTEFACT_SUFFIXES):
                return False
            if any(part in name for part in ARTEFACT_PARTS):
                return False
        return True


class F004(Floor):
    """EEP 7, "The checks": a command exists, and it can be run."""

    url = EEP7

    @staticmethod
    def check(repo, workflow_commands):
        """EEP 7: a command that decides the repository, run locally.

        A command need not be a file in the repository.  This rule was
        written believing it must, because that is how this repository
        happens to work, and it then failed a real repository whose
        checks run as `uv run pytest`.  EEP 7 requires a command, not a
        script, so what is decided here is narrower and true: that the
        host runs something, and that anything it runs which is a file
        here can actually be run.  Whether a command decides the
        repository or merely installs its dependencies cannot be told
        apart from outside, and is not guessed at.
        """
        # pylint: disable=redefined-outer-name
        if not workflow_commands:
            return None
        for command in workflow_commands:
            first = command.split()[0] if command.split() else ""
            candidate = repo / first
            if candidate.is_file() and not os.access(candidate, os.X_OK):
                return False
        return True


class F005(Floor):
    """EEP 7, "The checks": wired to run on push and pull request."""

    url = EEP7

    @staticmethod
    def check(workflow_triggers):
        """EEP 7: "for every push and every pull request"."""
        # pylint: disable=redefined-outer-name
        if workflow_triggers is None:
            return None
        return {"push", "pull_request"} <= workflow_triggers


class F006(Floor):
    """EEP 7, "How a change reaches the main branch": by pull request."""

    url = EEP7

    @staticmethod
    def check(repo, default_branch):
        """EEP 7: "Nothing is pushed to the main branch directly".

        EEP 7 gives the evidence itself: `git log main --first-parent
        --no-merges` returns only the initial import.  That command is
        run here rather than restated, so the rule and the law cannot
        drift apart, with the branch resolved rather than assumed.
        """
        # pylint: disable=redefined-outer-name
        if default_branch is None:
            return None
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo), "log", default_branch,
                 "--first-parent", "--no-merges", "--format=%H"],
                capture_output=True, text=True, check=False)
        except OSError:
            return None
        if proc.returncode != 0:
            return None
        return len([x for x in proc.stdout.split() if x.strip()]) <= 1


class F007(Floor):
    """EEP 7, "The entry point": instructions name no other path."""

    url = EEP7

    @staticmethod
    def check(repo):
        """EEP 7: an instruction file "names no path inside the
        repository other than the entry point".

        A token is only counted when it resolves to a file in this
        repository.  EEP 7 allows a path outside it, and says so of this
        repository's own two Google style guides.
        """
        # pylint: disable=redefined-outer-name
        seen = False
        for name in AGENT_FILES:
            path = repo / name
            if not path.is_file():
                continue
            seen = True
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            for token in PATH_TOKEN.findall(text):
                if token == ENTRY_POINT:
                    continue
                if (repo / token).exists():
                    return False
        return True if seen else None


def reasons(path):
    """Why each undecidable rule could not be decided, by rule name.

    repo-review prints that a check was skipped and has nowhere to put
    why: its ``skip_reason`` is filled only from a user's ignore list,
    not from a check that returned None.  EEP 7 wants the reason, so it
    is derived here from the same fixtures the checks use, and spoken by
    tools/check-floor.
    """
    root = pathlib.Path(path)
    out = {}
    if tracked(root) is None:
        out["F003"] = ("git ls-files failed, so the tracked file list "
                       "could not be read")
    found = workflows(root)
    if found is None:
        why = ("PyYAML is not installed, so no workflow could be parsed"
               if yaml is None else
               "no workflow in .github/workflows could be read")
        out["F004"] = why
        out["F005"] = why
    elif not workflow_commands(found):
        out["F004"] = ("no workflow runs a command, so there was none "
                       "to look for here")
    if default_branch(root) is None:
        out["F006"] = ("git found no default branch here, so no history "
                       "was examined")
    if not any((root / n).is_file() for n in AGENT_FILES):
        out["F007"] = ("the repository has no file that tells an agent "
                       "how to work in it")
    return out


def repo_review_checks():
    """Every check this plugin contributes, by name."""
    return {cls.__name__: cls()
            for cls in (F001, F002, F003, F004, F005, F006, F007)}


def repo_review_families(package):
    """The one family these checks belong to."""
    # pylint: disable=unused-argument
    return {"floor": {"name": "EEP 7, the floor every repository owes"}}
