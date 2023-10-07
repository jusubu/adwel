#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:08:16 2023

@author: jules
"""

import os

def canonical_path(path):
    """ Resolves symlinks, and formats filepath.

    Resolves symlinks,
    formats filepath using slashes appropriate for platform.

    Args:
        path (str): Filepath being formatted

    Returns:
        str: Provided path.
    """

    path = os.path.normpath(os.path.realpath(path))

    return path

