#!/usr/bin/env python

import io
import os
import re
import sys
from pathlib import Path

from github import Github
from dotenv import load_dotenv

load_dotenv()

GH_TOKEN = os.getenv("GH_TOKEN")
PAT = re.compile(
    r"- \[(.*?)( ★[0-9]+)?\]\(https://github.com/(.+?)/(.+?)/?\)( ★[0-9]+)?"
)


def main2(path: Path):
    g = Github(GH_TOKEN)

    output = io.StringIO()

    lines = path.read_text().splitlines()
    for line in lines:
        line = line.rstrip()
        m = re.search(PAT, line)
        if not m:
            output.write(line + "\n")
            continue

        name = m.group(1)
        org = m.group(3)
        repo_name = m.group(4)
        print("Updating:", org, repo_name)

        repo = g.get_repo(f"{org}/{repo_name}")
        stars = repo.stargazers_count
        updated = f"- [{name}](https://github.com/{org}/{repo_name}) ★{stars}"

        updated_line = line[0 : m.start()] + updated + line[m.end() :]
        if updated_line != line:
            print(line)
            print("->")
            print(updated_line)
            print()

        output.write(updated_line + "\n")

    path.write_text(output.getvalue())


def main():
    if len(sys.argv) == 2:
        main2(Path(sys.argv[1]))
    else:
        main2(Path("README.md"))


if __name__ == "__main__":
    main()
