# Import other packages.
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