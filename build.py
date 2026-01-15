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
import time

def main():
    process_resume()

    blog_posts = []
    glob_path = './blog/*'
    
    # Pre-defined dates for existing posts
    known_dates = {
        'vue_port': '2023-11-16',
        'static_website': '2022-09-28'
    }

    for file in glob.glob(glob_path):
        if os.path.isfile(file) and file[-3:] == ".md":
            meta = process_markdown(file)
            slug = meta['id']
            if slug in known_dates:
                meta['date'] = known_dates[slug]
            else:
                meta['date'] = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(file)))
            blog_posts.append(meta)

        if os.path.isfile(file) and file[-4:] == ".png":
            subprocess.run(["cp", file, "./public/" ])

    # Sort by date descending
    blog_posts.sort(key=lambda x: x['date'], reverse=True)
    
    os.makedirs('./public/blog/', exist_ok=True)
    with open('public/blog/index.json', 'w') as f:
        json.dump(blog_posts, f, indent=2)

def process_markdown(file_path: str):
    with open(file_path, "r", encoding="utf-8") as in_file:
        lines = in_file.readlines()
    
    title = "Untitled"
    if lines and lines[0].startswith('# '):
        title = lines[0][2:].strip()
        
    text = "".join(lines)
    html = "".join([
        markdown.markdown(text, extensions=['markdown.extensions.fenced_code']),
    ])

    basename = os.path.basename(file_path)
    slug = basename[:-3]
    out_page = f"public/blog/{slug}.html" # Get rid of .md and replace with .html
    print(f"outputting to {out_page}")
    os.makedirs('./public/blog/', exist_ok=True)
    with open(out_page, "w", encoding="utf-8") as out_file:
        out_file.write(html)
    
    return {
        "id": slug,
        "title": title,
        "path": f"/blog/{slug}"
    }

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
