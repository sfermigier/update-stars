#!/usr/bin/env python

import io
import os
import re

from github import Github
from dotenv import load_dotenv

load_dotenv()


GH_USER = os.getenv("GH_USER")
GH_PASSWD = os.getenv("GH_PASSWD")
GH_TOKEN = os.getenv("GH_TOKEN")
PAT = re.compile(r"\(https://github.com/(.+?)/(.+?)/?\) ★([0-9]+)")


def main():
    g = Github(GH_TOKEN)

    output = io.StringIO()

    for line in open("README.md").readlines():
        line = line.rstrip()
        m = re.search(PAT, line)
        if m:
            print(m.groups())
            org = m.group(1)
            repo_name = m.group(2)
            print(org, repo_name)
            repo = g.get_repo(f"{org}/{repo_name}")
            stars = repo.stargazers_count
            updated = f"(https://github.com/{org}/{repo_name}) ★{stars}"
            line = line[0 : m.start()] + updated + line[m.end() :]

        output.write(line + "\n")

    open("README.md", "w").write(output.getvalue())
    # print(output.getvalue())


if __name__ == "__main__":
    main()
