""" 
Import other packages.
"""

import sgtk
import hou
import os

HookBaseClass = sgtk.get_hook_base_class()

class TKHoudiniCacheNodeCollector(HookBaseClass):
    
    @property
    def settings(self):
        """
        Retrieve settings from parented class and (if necessary) update them.
        """

        current_settings = super().settings()

        return current_settings

    def process_current_session(self, settings, parent_item):
        """
        Process the current session to collect all tk-houdini-cachenodes.
        """

        # process all other items of houdini first
        super().process_current_session()

        self.collect_tk_houdini_cachenodes()

    def collect_tk_houdini_cachenodes(self):
        """
        Collect all instances of the tk-houdini-cachenodes.
        """