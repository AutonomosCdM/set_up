"""
Sphinx configuration for Google Workspace Intelligent Agent documentation.
"""

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'Google Workspace Intelligent Agent'
copyright = '2025, Cline AI Solutions'
author = 'Cline AI Solutions'
release = '0.1.0'

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',   # Auto-generate documentation from docstrings
    'sphinx.ext.napoleon',  # Support for Google/NumPy style docstrings
    'sphinx.ext.viewcode', # Add source code links
    'sphinx.ext.todo',     # Support for TODO notes
    'sphinx.ext.intersphinx', # Link to other projects' documentation
    'myst_parser'          # Markdown support
]

# Configuration for extensions
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Source file parsing
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# HTML output configuration
html_theme = 'sphinx_rtd_theme'
html_title = 'Google Workspace Intelligent Agent'
html_show_sourcelink = True
html_show_sphinx = False

# Intersphinx configuration for linking to other documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'google-auth': ('https://google-auth.readthedocs.io/en/latest/', None),
    'groq': ('https://console.groq.com/docs', None)
}

# Todo configuration
todo_include_todos = True

# Additional configuration
add_module_names = False
pygments_style = 'sphinx'

# HTML context for additional customization
html_context = {
    'display_github': True,
    'github_user': 'cline-ai',
    'github_repo': 'google-workspace-agent',
    'github_version': 'main/docs/'
}

# Suppress certain warnings
suppress_warnings = [
    'misc.highlighting_failure',
    'ref.citation'
]
