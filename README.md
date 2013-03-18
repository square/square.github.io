Square Open Source Portal
=========================

A simple, static portal which outlines our open source offerings. Intentionally
themed to look like a merchant page on the directory.


Development
-----------

Due to the use of absolute URLs in CSS files that are (essentially) out of our
control, the easiest way to develop is by running with Jekyll.

    jekyll --server

Repositories are listed in the `repos.json` file as a map of repository names
to a list of their categories. Invoking the `generate.py` script will update
the `index.html` page with the latest repos by using the `index.mustache` file
as a template.

Repository data is pulled via the GitHub API (e.g., website).
