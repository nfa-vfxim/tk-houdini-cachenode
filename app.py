# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Alembic Output App for Houdini
"""

import os
import sgtk

import hou


class AlembicOutputNode(sgtk.platform.Application):

    def init_app(self):
        """
        Called as the application is being initialized
        """

        # Register all our OTL files with the Houdini engine
        otl_path = os.path.join(self.disk_location, 'otls')
        for filename in os.listdir(otl_path):
            if os.path.splitext(filename)[-1] == '.otl':
                path = os.path.join(otl_path, filename)
                self.engine.register_otl(path)
