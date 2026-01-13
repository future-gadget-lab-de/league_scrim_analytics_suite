# docs/conf.py
from __future__ import annotations

import os
import sys
from datetime import datetime

# Falls Main.py im Root liegt und Sie es auch dokumentieren wollen:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath("_ext"))

project = "lsas"
author = "Future Gadget Lab"
copyright = f"{datetime.now().year}, {author}"


extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    "myst_parser",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "import_graph",
    "sphinx_uml",
    'sphinx_tabs.tabs'
]


depgraph_hierarchie_size = 2
depgraph_root_package = "src"     # <-- set this
depgraph_internal_depth = 5     # tweak for readability
depgraph_include_external_packages = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

autosummary_generate = True

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

# Autodoc-Verhalten (robuste Defaults)
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": False,
    "show-inheritance": True,
}
autodoc_typehints = "description"  # Typen in die Beschreibung statt Signatur (oft lesbarer)
autodoc_mock_imports = ["PySide6"]

# Theme (beliebt, solide)
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "navigation_depth": 4,      # >= 3, oft 4 sinnvoll
    "collapse_navigation": False,
    "titles_only": False,
}

graphviz_output_format = "dot"

# Optional: Markdown support (wenn myst-parser installiert ist)
# extensions.append("myst_parser")
# source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
