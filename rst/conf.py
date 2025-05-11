# pylint: skip-file

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# imports -------------------------------------------------------------------------------------
import sys
from pathlib import Path

import sphinx.application

from bubop.logging import logger
from bubop.version import get_version_from_git

# document the source code with autodoc
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
source_code = Path(__file__).resolve().parent.parent
if not source_code.exists():
    raise FileNotFoundError(f"Path to the source code is not valid -> {source_code}")

sys.path.insert(0, str(source_code))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "bubop"
copyright = "2025, Nikos Koukis"
author = "Nikos Koukis"

version = str(get_version_from_git())
release = version

logger.info(f"Determined version from git: {version!r}")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinxcontrib.spelling",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    # "logo_only": False,
    "prev_next_buttons_location": "both",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 3,
}

# -- spelliing -----------------------------------------------------------------
spelling_lang = "en_US"
# Refer to https://github.com/pyenchant/pyenchant/blob/master/website/content/tutorial.rst#personal-word-lists
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_show_suggestions = True
spelling_ignore_acronyms = True


# -- setup function ------------------------------------------------------------
def setup(app: sphinx.application.Sphinx) -> None:
    app.add_css_file("custom.css")
