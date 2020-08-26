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
        super().process_current_session(settings, parent_item)

        self.collect_tk_houdini_cachenodes()

    def collect_tk_houdini_cachenodes(self):
        """
        Collect all instances of the tk-houdini-cachenodes.
        """

        publisher = self.parent
        engine = publisher.engine
        app = engine.apps.get("tk-houdini-cachenode")

        if not app:
            self.logger.debug("tk-houdini-cachenode does not seem to be installed")
            return

        try:
            nodes = app.get_nodes()
        except:
            self.logger.warning("could not get any instances of tk-houdini-cachenode")

        work_template = app.get_work_file_template()

        for node in nodes:
            out_path = app.get_output_path(node)

            if not os.path.exists(out_path):
                continue
            
            self.logger.info("processing sgtk_cachenode: %s" % (node.path()))
            
