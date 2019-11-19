"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config
"""

# pylint: disable=import-error, invalid-name, redefined-builtin

import datetime as dt
from sphinx.writers.html import HTMLTranslator

#

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'OLCF User Documentation'
copyright = '%s, OLCF' % dt.datetime.now().year
author = 'OLCF'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/theme_overrides.css',
]

html_js_files = [
    'js/custom.js',
]

html_context = {
    'vcs_pageview_mode': 'edit',
    'display_github': True,
    'github_user': 'olcf', # Username
    'github_repo': 'olcf-user-docs', # Repo name
    'github_version': 'master', # Version
    'conf_py_path': '/', # Path in the checkout to the docs root
}

# see https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
    'canonical_url': 'https://docs.olcf.ornl.gov',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'style_external_links': True,
}


# pylint: disable=too-few-public-methods
class PatchedHTMLTranslator(HTMLTranslator):
    '''HTMLTranslator patched to open external links in new tabs.

    Taken from: 'http://jack.rosenth.al/hacking-docutils.html#sphinx-hacks'
    '''
    def visit_reference(self, node):
        '''Sets link target to '_blank' (new page tab) if link node is
        external to the site.
        '''
        if (node.get('newtab')
                or not (node.get('target')
                        or node.get('internal')
                        or 'refuri' not in node)):
            node['target'] = '_blank'
        super().visit_reference(node)


def mk_tbl(tbl, hdrs):
    ''' Create a text table from the dictionary.

        tbl  : {str:[str]} = a mapping of column headers to lists of entries
        hdrs : [str] = a selection of columns you would like to pull from tbl

        returns a string containing the grid-formatted table
    '''
    cols = [[h.title()] + tbl[h] for h in hdrs] # select cols
    widths = [max(map(len, col)) for col in cols]
    brk = '+-' + '-+-'.join(['-'*w for w in widths]) + '-+'
    lines = [brk]
    for i in range(len(cols[0])):
        lines.append('| ' + ' | '.join(
                   '{0: <{1}}'.format(c[i], w)
                      for w, c in zip(widths,cols)) + ' |')
        if i == 0:
            lines.append('+=' + '=+='.join(['='*w for w in widths]) + '=+')
        else:
            lines.append(brk)
    return '\n'.join(lines) + '\n'

import yaml

with open("systems.yaml") as f:
    x = yaml.load(f, Loader=yaml.FullLoader)
    attrs = x[0].keys()
    Filesystems = dict((h, [y[h] for y in x]) for h in attrs)

rst_context = {
        'Filesystems': Filesystems,
        'mk_tbl': mk_tbl,
        }
def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    if app.builder.format != 'html':
        return
    src = source[0]
    rendered = app.builder.templates.render_string(
        src, rst_context
    )
    source[0] = rendered

def setup(app):
    '''Function to setup sphinx customizations.'''
    app.set_translator('html', PatchedHTMLTranslator)
    app.connect("source-read", rstjinja)

# globally-available substitutions

rst_prolog = r"""
.. |R| replace:: \ :sup:`®`
"""
