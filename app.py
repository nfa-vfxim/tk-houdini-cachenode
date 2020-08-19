"""
File Cache node App for use with Toolkit's Houdini engine.
"""

import sgtk

class TkCacheNodeApp(sgtk.platform.Application):
    def init_app(self):
        """Initialize the app."""

        tkHoudiniCachenode = self.import_module("tk_houdini_cachenode")
        self.handler = tkHoudiniCachenode.TkCacheNodeHandler(self)