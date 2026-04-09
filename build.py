#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Christopher Odom <christopher.r.odom@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Builds a webpage, depends on python-markdown
"""

import markdown
import subprocess
import os
import glob
import json
import re
import time


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    process_resume()

    blog_posts = []
    glob_path = "./blog/*"

    for file in glob.glob(glob_path):
        if os.path.isfile(file) and file[-3:] == ".md":
            meta = process_markdown(file)
            blog_posts.append(meta)

        if os.path.isfile(file) and file[-4:] == ".png":
            subprocess.run(["cp", file, "./public/"])

    # Sort by date descending
    blog_posts.sort(key=lambda x: x["date"], reverse=True)

    os.makedirs("./src/data/blog/", exist_ok=True)
    with open("src/data/blog/index.json", "w") as f:
        json.dump(blog_posts, f, indent=2)


def process_markdown(file_path: str):
    with open(file_path, "r", encoding="utf-8") as in_file:
        text = in_file.read()

    body_content = markdown.markdown(
        text, extensions=["markdown.extensions.fenced_code"]
    )
    # Extract date from <!-- date: YYYY-MM-DD --> comment if present,
    # otherwise fall back to the file's modification time.
    date_match = re.search(r"<!--\s*date:\s*(\d{4}-\d{2}-\d{2})\s*-->", text)
    if date_match:
        date = date_match.group(1)
    else:
        date = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(file_path)))

    # Extract title from first markdown heading
    title = "Untitled"
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()

    html = markdown.markdown(text, extensions=["markdown.extensions.fenced_code"])

    basename = os.path.basename(file_path)
    slug = basename[:-3]
    out_page = f"src/data/blog/{slug}.html"
    page_title = file_path.split("/")[-1][:-3].replace("_", " ").title()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #fafafa;
            color: #18181b;
            line-height: 1.75;
            margin: 0;
            padding: 0;
        }}
        article {{
            max-width: 48rem;
            margin: 0 auto;
            padding: 4rem 1.5rem;
        }}
        h1, h2, h3, h4 {{
            font-weight: 600;
            color: #18181b;
            margin-top: 2em;
            margin-bottom: 0.75em;
            line-height: 1.3;
        }}
        h1 {{ font-size: 2rem; }}
        h2 {{ font-size: 1.5rem; }}
        h3 {{ font-size: 1.25rem; }}
        p {{
            margin-bottom: 1.5em;
            color: #52525b;
        }}
        a {{
            color: #18181b;
            text-decoration: underline;
            text-underline-offset: 2px;
        }}
        a:hover {{ color: #3b82f6; }}
        code {{
            background-color: rgba(0, 0, 0, 0.05);
            padding: 0.125rem 0.375rem;
            border-radius: 0.25rem;
            font-size: 0.875em;
            font-family: 'JetBrains Mono', ui-monospace, monospace;
        }}
        pre {{
            background-color: #f4f4f5;
            border: 1px solid #e4e4e7;
            border-radius: 0.75rem;
            padding: 1.25rem;
            overflow-x: auto;
            margin: 1.5em 0;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        ul, ol {{
            margin: 1em 0;
            padding-left: 1.5em;
            color: #52525b;
        }}
        li {{ margin-bottom: 0.5em; }}
        blockquote {{
            border-left: 4px solid #e4e4e7;
            padding-left: 1em;
            margin: 1.5em 0;
            font-style: italic;
            color: #71717a;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e4e4e7;
            margin: 2em 0;
        }}
        img {{
            max-width: 100%;
            border-radius: 0.5rem;
            margin: 1.5em 0;
        }}
        ::selection {{
            background-color: #e4e4e7;
        }}
    </style>
</head>
<body>
    <article>
        {body_content}
    </article>
</body>
</html>"""

    print(f"outputting to {out_page}")
    os.makedirs("./src/data/blog/", exist_ok=True)
    with open(out_page, "w", encoding="utf-8") as out_file:
        out_file.write(html)

    return {"id": slug, "title": page_title, "path": f"/blog/{slug}", "date": date}


def process_resume():
    print("Compiling resume...")
    try:
        with open("resume/master_resume_2025.md", "r", encoding="utf-8") as in_file:
            text = in_file.read()

        metadata = {}
        content = text

        if text.startswith("---"):
            try:
                first_sep = text.find("---", 3)
                if first_sep != -1:
                    yaml_text = text[3:first_sep].strip()
                    content = text[first_sep + 3:].strip()

                    import yaml
                    metadata = yaml.safe_load(yaml_text) or {}
            except Exception as e:
                print(f"Warning: Could not parse YAML front matter: {e}")

        html = markdown.markdown(content, extensions=["markdown.extensions.fenced_code"])

        name = metadata.get("name", "")
        subheading = metadata.get("subheading", "")
        left_column = metadata.get("left-column", [])
        right_column = metadata.get("right-column", [])

        left_html = "".join(f"<p>{markdown.markdown(item).replace('<p>', '').replace('</p>', '')}</p>" for item in left_column)
        right_html = "".join(f"<p>{markdown.markdown(item).replace('<p>', '').replace('</p>', '')}</p>" for item in right_column)

        header_html = f"""<header class="resume-header">
            <div class="name-section">
                <h1>{name}</h1>
                <p class="subheading">{subheading}</p>
            </div>
            <div class="contact-section">
                <div class="left-column">{left_html}</div>
                <div class="right-column">{right_html}</div>
            </div>
        </header>"""

        full_html = header_html + html

        with open("src/data/resume.html", "w", encoding="utf-8") as out_file:
            out_file.write(full_html)
        print("done")
    except FileNotFoundError:
        print("Error: resume/master_resume_2025.md not found.")


if __name__ == "__main__":
    main()
