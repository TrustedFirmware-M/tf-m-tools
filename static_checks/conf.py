#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------#

project = 'Static Checking Framework'
html_show_copyright = False

extensions = [
    'sphinx.ext.autosectionlabel',
]

# Set up autosection with a maximum depth of 2
autosectionlabel_prefix_document=True
autosectionlabel_maxdepth=2

# Set the theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {'collapse_navigation': False}

# Set the README as the master document
master_doc = 'README'

