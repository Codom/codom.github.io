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

def main():
    process_resume()

    glob_path = './blog/*'
    for file in glob.glob(glob_path):
        if os.path.isfile(file) and file[-3:] == ".md":
            process_markdown(file)
        if os.path.isfile(file) and file[-4:] == ".png":
            subprocess.run(["cp", file, "./public/" ])

def process_markdown(page: str):
    with open(f"{page}", "r", encoding="utf-8") as in_file:
        text = in_file.read()

    body_content = markdown.markdown(text, extensions=['markdown.extensions.fenced_code'])
    
    page_title = page.split('/')[-1][:-3].replace('_', ' ').title()

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

    out_page = f"public/{page[2:-3]}.html"
    print(f"outputting to {out_page}")
    os.makedirs('./public/blog/', exist_ok=True)
    with open(out_page, "w", encoding="utf-8") as out_file:
        out_file.write(html)

def process_resume():
    latex_env = os.environ | {"TEXINPUTS": ".:./resume:"}
    print(latex_env)
    print("Compiling resume...")
    subprocess.run(["pdflatex", "resume/resume.tex"], env=latex_env, check=True)
    subprocess.run(["mv", "resume.pdf", "public/"])
    subprocess.run(["rm", "resume.aux", "resume.log", "resume.out"])
    print("done")

if __name__ == "__main__":
    main()
