Square Open Source Portal
=========================

A simple, static portal which outlines our open source offerings. Intentionally
themed to look like a merchant page on the directory.


Development
-----------

Due to the use of absolute URLs in CSS files that are (essentially) out of our
control, the easiest way to develop is by running with Jekyll.

    jekyll serve

Repositories are listed in the `repos.json` file as a map of repository names
to a list of their categories. Invoking the `generate.py` script will update
the `index.html` page with the latest repos by using the `index.mustache` file
as a template. Run `pip install pystache requests pygithub3` if needed to
install python dependencies.

Repository data is pulled via the GitHub API (e.g., website). By default the
script performs unauthenticated requests, so it's easy to run up against
GitHub's limit of [60 unauthenticated requests per
hour](http://developer.github.com/v3/#rate-limiting). To make authenticated
requests and work around the rate-limiting, add an entry for api.github.com to
your ~/.netrc file, preferably with a Personal Access Token from
https://github.com/settings/applications.

Images are loaded by convention from the `repo_images/` directory. Ensure the
name is the same as the repo name in the `repos.json` file and has a `.jpg`
extension. Currently all images are rotated 10 degrees counter-clockwise to
break up the overwhelming horizontal and vertical visual lines on the page.
