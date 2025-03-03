# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime


# -- Project information -----------------------------------------------------

project = 'GMT Examples'
year = datetime.date.today().year
copyright = f"2022-{year}, The GMT Examples Authors"
author = 'GMT Examples Contributors'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx_design",
    "sphinx_gmt.gmtplot",
    'sphinx.ext.intersphinx',
    'sphinxcontrib.youtube'
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# configure links to GMT docs
extlinks = {
    "gmt-module": ("https://docs.generic-mapping-tools.org/latest/%s", "%s"),
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_baseurl="https://www.generic-mapping-tools.org/gmt-examples/"
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'sticky_navigation': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_css_files = ["style.css"]

# Adjust highlight language for sphinx_gmt examples
highlight_language = "bash"