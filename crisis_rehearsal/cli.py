# -*- coding: utf-8 -*-
"""The ``crh`` command line interface.

    crh --version
    crh verify [--repo PATH] [--write]
    crh stats  [--repo PATH] [--json] [--bootstrap N] [--seed N]
    crh report --event ID [--repo PATH] [--out PATH]
    crh demo   [--repo PATH] [--out DIR]
    crh pack init --id ID --name NAME [--sector enterprise|government|finance|other]
                 [--out PATH] [--force]
    crh pack validate PATH [--repo PATH]
    crh site   [--repo PATH] [--out DIR]

Exit codes: 0 success, 1 a check failed (evidence drift, invalid pack, demo aborted
because the pack drifted), 2 bad input / missing files / no repository found.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from . import scenariopack
from .data import DataError
from .demo import DemoFailed, _display_path, run as run_demo
from .evidence import verify as verify_evidence
from .evidence import write_manifest, as_text as verify_text
from .paths import RepoNotFound, find_repo, rel
from .report import ReportError, build_context, write_dossier
from .scripts_bridge import ScriptUnavailable
from .scenariopack import PackError
from .site import generate as generate_site
from .stats import StatsUnavailable, as_json, as_text, compute as compute_stats


def _configure_streams() -> None:
    """Make console output crash-proof on legacy Windows code pages.

    The CLI prints Chinese event names and file paths. On a GBK console an
    unrepresentable character would otherwise raise UnicodeEncodeError; replacing
    it keeps the command usable. For byte-exact UTF-8 output, redirect to a file
    or run under ``chcp 65001`` (documented in docs/cli.md).
    """
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None or stream is not getattr(sys, "__" + name, None):
            continue
        try:
            stream.reconfigure(errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError, OSError):
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crh",
        description="Crisis Rehearsal Engine — offline evidence workstation for the "
                    "public 30-event crisis backtest. Standard library only, no API "
                    "key, no network.",
        epilog="Every number this tool prints is recomputable from the evidence pack "
               "shipped in this repository. Start with `crh demo`.",
    )
    parser.add_argument("--version", action="version",
                        version=f"crh {__version__}",
                        help="print the CLI version and exit")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # --- verify -------------------------------------------------------------
    verify = sub.add_parser(
        "verify", help="check data/ against data/evidence.sha256",
        description="Check every file under data/ against the sha256 manifest. "
                    "Reports OK / MODIFIED / MISSING / UNLISTED per file and exits 1 "
                    "on any drift. --write regenerates the manifest (the only command "
                    "that writes into data/; it rewrites that one file only).")
    verify.add_argument("--repo", metavar="PATH", default=None,
                        help="repository root (default: search from the current "
                             "directory, then $CR_ROOT)")
    verify.add_argument("--write", action="store_true",
                        help="regenerate data/evidence.sha256 from the files on disk")
    verify.add_argument("--quiet", action="store_true",
                        help="only print the summary line")
    verify.set_defaults(func=cmd_verify)

    # --- stats --------------------------------------------------------------
    stats = sub.add_parser(
        "stats", help="recompute the published v0.2 numbers",
        description="Recompute the published numbers by importing "
                    "scripts/ci_stats.py and scripts/sta_stats.py from the checkout: "
                    "82.2% top-3 hit rate (t CI 78.5-85.9%, bootstrap 78.7-85.6%), "
                    "within-event SD 0.26/3, 5/30 identical, STA 58 (failed).")
    stats.add_argument("--repo", metavar="PATH", default=None)
    stats.add_argument("--json", action="store_true",
                       help="machine-readable JSON (includes per-event rows)")
    stats.add_argument("--bootstrap", type=int, default=10000, metavar="N",
                       help="bootstrap resamples, 0 disables (default: 10000)")
    stats.add_argument("--seed", type=int, default=None,
                       help="bootstrap RNG seed (default: the published seed)")
    stats.set_defaults(func=cmd_stats)

    # --- report -------------------------------------------------------------
    report = sub.add_parser(
        "report", help="render one self-contained HTML rehearsal dossier",
        description="Render one event as a single self-contained HTML file: event "
                    "dossier (real outcome, marked as hindsight), T-72h information "
                    "pack, simulation configuration, Top-3 risks vs the outcome, "
                    "three-run scores and stability, sha256 provenance, honest "
                    "limitations. Events 1, 6, 25 and 28 include the verbatim "
                    "rehearsal report; the other events have no report body and the "
                    "page says so.")
    report.add_argument("--event", "-e", metavar="ID", required=True,
                        help="event id, 1-30 (e.g. 6)")
    report.add_argument("--repo", metavar="PATH", default=None)
    report.add_argument("--out", metavar="PATH", default=None,
                        help="output file (.html) or directory "
                             "(default: <repo>/reports/event-ID.html)")
    report.set_defaults(func=cmd_report)

    # --- demo ---------------------------------------------------------------
    demo = sub.add_parser(
        "demo", help="one command: verify + stats + 4 dossiers + index (<10s)",
        description="Offline demo, no API key: verify the evidence pack, recompute "
                    "the published numbers, render the four dossiers whose rehearsal "
                    "report is shipped, and write an index page. Fails rather than "
                    "present numbers from a drifted evidence pack.")
    demo.add_argument("--repo", metavar="PATH", default=None)
    demo.add_argument("--out", metavar="DIR", default=None,
                      help="output directory (default: <repo>/demo_out)")
    demo.set_defaults(func=cmd_demo)

    # --- pack ---------------------------------------------------------------
    pack = sub.add_parser(
        "pack", help="scenario pack scaffolding and validation",
        description="Create or validate a scenario pack: the portable input "
                    "contract for a rehearsal (timeline, stakeholders, regulatory "
                    "triggers, escalation ladder, KPIs, decisions, evidence, "
                    "provenance).")
    pack_sub = pack.add_subparsers(dest="pack_command", metavar="ACTION")

    init = pack_sub.add_parser(
        "init", help="write a valid, clearly-marked template pack",
        description="Write a schema-valid template pack. Every content field is "
                    "marked [TEMPLATE]/TODO: a scaffold is not evidence and must not "
                    "be presented as a delivered case.")
    init.add_argument("--id", required=True, metavar="ID",
                      help="lower-case pack id, e.g. my-scenario-2026")
    init.add_argument("--name", required=True, metavar="NAME",
                      help="human-readable scenario name")
    init.add_argument("--sector", default="enterprise",
                      choices=list(scenariopack.SECTORS),
                      help="sector template (default: enterprise)")
    init.add_argument("--jurisdiction", default="CN", metavar="CODE",
                      help="default jurisdiction (default: CN)")
    init.add_argument("--classification", default="internal",
                      choices=list(scenariopack.CLASSIFICATIONS),
                      help="data classification (default: internal)")
    init.add_argument("--lang", default="zh", metavar="TAG",
                      help="language of the free-text fields (default: zh)")
    init.add_argument("--out", metavar="PATH", default=None,
                      help="output file or directory "
                           "(default: <repo>/scenario_packs/<id>.json)")
    init.add_argument("--force", action="store_true",
                      help="overwrite an existing file")
    init.set_defaults(func=cmd_pack_init)

    validate = pack_sub.add_parser(
        "validate", help="validate a pack against schema/scenario_pack.schema.json",
        description="Validate a scenario pack with the standard-library JSON-Schema "
                    "subset validator (no jsonschema dependency). Exit 1 when invalid.")
    validate.add_argument("path", metavar="PATH",
                          help="pack file, or a directory containing scenario_pack.json")
    validate.add_argument("--repo", metavar="PATH", default=None,
                          help="repository root, used to locate the schema")
    validate.set_defaults(func=cmd_pack_validate)

    # --- site ---------------------------------------------------------------
    site = sub.add_parser(
        "site", help="static dossier site for all 30 events",
        description="Render the index plus one self-contained dossier per event into "
                    "a directory that can be served from an intranet or GitHub Pages. "
                    "No JavaScript, no external assets.")
    site.add_argument("--repo", metavar="PATH", default=None)
    site.add_argument("--out", metavar="DIR", default=None,
                      help="output directory (default: <repo>/site)")
    site.set_defaults(func=cmd_site)

    return parser


# ------------------------------------------------------------------ handlers --
def cmd_verify(args: argparse.Namespace) -> int:
    repo = find_repo(args.repo)
    if args.write:
        target = write_manifest(repo)
        entries = sum(1 for line in target.read_text(encoding="utf-8").splitlines()
                      if line and not line.startswith("#"))
        print(f"evidence manifest written: {rel(repo, target)} ({entries} files)")
        if args.quiet:
            return 0
    result = verify_evidence(repo)
    print(verify_text(result, repo, verbose=not args.quiet))
    return 0 if result["ok"] else 1


def cmd_stats(args: argparse.Namespace) -> int:
    repo = find_repo(args.repo)
    result = compute_stats(repo, bootstrap=args.bootstrap, seed=args.seed)
    if args.json:
        print(as_json(result))
    else:
        print(as_text(result))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    repo = find_repo(args.repo)
    raw = str(args.event).strip()
    if raw.lower().lstrip("#").isdigit():
        eid = str(int(raw.lower().lstrip("#")))
    else:
        eid = raw
    context = build_context(repo)
    path = write_dossier(repo, eid, out=args.out, context=context)
    shipped = context["shipped"].get(eid) or {}
    per_event = context["stats"]["per_event"].get(eid, {})
    name = context["events"][eid].title
    print(f"event    : #{eid} {name}")
    print(f"report   : {rel(repo, path)} ({path.stat().st_size / 1024:.1f} KB, "
          "self-contained HTML: inline CSS, no JS, no external assets)")
    if shipped.get("present"):
        print(f"body     : shipped report included verbatim "
              f"({shipped['rel']}, sha256 {shipped['sha256'][:16]})")
    else:
        print("body     : none — no rehearsal report is shipped for this event; the "
              "page contains")
        print("           the T-72h seed, the real outcome and the three judge records "
              "only.")
    print(f"numbers  : event mean {per_event.get('mean', 0):.2f}/3 "
          f"({per_event.get('hit_rate_pct', 0):.1f}%), "
          f"STA {(per_event.get('sta') or {}).get('value', 0):.0f}/100 "
          f"({(per_event.get('sta') or {}).get('reading', 'n/a')})")
    print(f"open     : {path}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    try:
        run_demo(repo=args.repo, out=args.out)
    except DemoFailed:
        return 1
    return 0


def cmd_pack_init(args: argparse.Namespace) -> int:
    repo = None
    out = args.out
    if out is None:
        repo = find_repo(None)
        out = str(Path(repo) / "scenario_packs")
    else:
        try:
            repo = find_repo(None)
        except RepoNotFound:
            repo = None
    pack = scenariopack.skeleton(
        args.id, args.name, sector=args.sector,
        jurisdiction=args.jurisdiction, classification=args.classification,
        lang=args.lang)
    # Self-check: never write a scaffold that the published schema rejects.
    schema = scenariopack.load_schema(repo)
    errors = scenariopack.validate_pack(pack, schema)
    if errors:
        raise PackError("generated scaffold failed its own schema check:\n  - "
                        + "\n  - ".join(errors))
    out_path = Path(out)
    if out_path.suffix.lower() != ".json":
        out_path = out_path / f"{args.id}.json"
    target = scenariopack.write_pack(pack, out_path, force=args.force)
    print("scenario pack written")
    print(f"file    : {_display_path(target)}")
    print(f"schema  : {_display_path(scenariopack.schema_path(repo))}")
    print("template: YES — every [TEMPLATE]/TODO placeholder must be replaced before "
          "a rehearsal.")
    print("          A scaffold is not evidence and must not be presented as a "
          "delivered case.")
    print(f"validate: crh pack validate {_display_path(target)}")
    return 0


def cmd_pack_validate(args: argparse.Namespace) -> int:
    repo = None
    try:
        repo = find_repo(args.repo)
    except RepoNotFound:
        repo = None
    data, resolved, errors, schema = scenariopack.validate_file(Path(args.path), repo)
    print("scenario pack validation")
    print("=" * 74)
    print(f"file    : {_display_path(resolved)}")
    print(f"schema  : {_display_path(schema)}")
    if errors:
        print(f"result  : INVALID — {len(errors)} error(s)")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("result  : VALID")
    print(f"pack    : {scenariopack.summary_line(data)}")
    if data.get("template"):
        print("note    : template=true — this is a scaffold, not a delivered case.")
    return 0


def cmd_site(args: argparse.Namespace) -> int:
    generate_site(repo=args.repo, out=args.out)
    return 0


# ---------------------------------------------------------------------- main --
def main(argv=None) -> int:
    _configure_streams()
    parser = build_parser()
    args = parser.parse_args(argv)
    command = getattr(args, "command", None)
    if not command:
        parser.print_help()
        return 0
    if command == "pack" and not getattr(args, "pack_command", None):
        print("usage: crh pack {init,validate} ...", file=sys.stderr)
        return 2
    try:
        return int(args.func(args) or 0)
    except (RepoNotFound, DataError, StatsUnavailable, ReportError, PackError,
            ScriptUnavailable, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except DemoFailed as exc:
        print(f"demo aborted: {exc}", file=sys.stderr)
        return 1
    except BrokenPipeError:  # pragma: no cover - piping into head
        return 0
    except KeyboardInterrupt:  # pragma: no cover
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
