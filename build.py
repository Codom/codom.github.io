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

    html = "".join([
        markdown.markdown(text, extensions=['markdown.extensions.fenced_code']),
    ])

    out_page = f"public/{page[:-3]}.html" # Get rid of .md and replace with .html
    print(f"outputting to {out_page}")
    with open(out_page, "w", encoding="utf-8") as out_file:
        out_file.write(html)

def process_resume():
    latex_env = os.environ | {"TEXINPUTS": ".:./resume:"}
    print(latex_env)
    print("Compiling resume...")
    subprocess.run(["pdflatex", "resume/resume.tex"], env=latex_env)
    subprocess.run(["mv", "resume.pdf", "public/"])
    subprocess.run(["rm", "resume.aux", "resume.log", "resume.out"])
    print("done")

if __name__ == "__main__":
    main()
