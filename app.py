"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

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
