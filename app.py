"""
File Cache node App for use with Toolkit's Houdini engine.
"""

import sgtk

class TkCacheNodeApp(sgtk.platform.Application):
    def init_app(self):
        """Initialize the app."""

        tk_houdini_cachenode = self.import_module("tk_houdini_cachenode")
        self.handler = tk_houdini_cachenode.TkCacheNodeHandler(self)

    def get_nodes(self):
        """
        Returns a list of hou.node objects for each tk cache node.
        Example usage::
        >>> import sgtk
        >>> eng = sgtk.platform.current_engine()
        >>> app = eng.apps["tk-houdini-cache"]
        >>> tk_cache_nodes = app.get_nodes()
        """

        self.log_debug("Retrieving tk-houdini-cache nodes...")
        tk_houdini_cache = self.import_module("tk_houdini_cachenode")
        nodes = tk_houdini_cache.TkCacheNodeHandler.get_nodes()
        self.log_debug("Found %s tk-houdini-cache nodes." % (len(nodes),))
        return nodes

    def get_output_path(self, node):
        """
        Returns the evaluated output path for the supplied node.
        Example usage::
        >>> import sgtk
        >>> eng = sgtk.platform.current_engine()
        >>> app = eng.apps["tk-houdini-cachenode"]
        >>> output_path = app.get_output_path(tk_cache_node)
        """

        self.log_debug("Retrieving output path for %s" % (node,))
        tk_houdini_cache = self.import_module("tk_houdini_cachenode")
        output_path = tk_houdini_cache.TkCacheNodeHandler.get_output_path(node)
        self.log_debug("Retrieved output path: %s" % (output_path,))
        return output_path

    def get_work_file_template(self):
        """
        Returns the configured work file template for the app.
        """

        return self.get_template("output_cache_template")

    def get_publish_file_template(self):
        """
        Returns the configured publish file template for the app.
        """

        return self.get_template("output_publish_template")