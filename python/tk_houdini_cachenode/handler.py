import sgtk
import hou
import os
import re

class TkCacheNodeHandler(object):

    TK_CACHE_NODE_TYPE = "sgtk_cache"
    NODE_OUTPUT_PATH_PARM = "pathString"

    def __init__(self, app):
        self._app = app

    def setupNode(self, node):
        
        # get parameters and computed output path
        path = node.parm("path")
        pathString = node.parm("pathString")
        outputPath = self._computeOutputPath(node)
        outputLabel = os.path.split(outputPath)[1]

        try:
            pathString.set(outputPath)
            path.set(outputLabel)
        except:
            e = "The output path could not be calculated!"
            raise sgtk.TankError(e)

    @classmethod
    def get_nodes(cls):
        """
        Returns a list of all tk-houdini-cachenode instances in the current
        session.
        """

        tk_node_type = TkCacheNodeHandler.TK_CACHE_NODE_TYPE

        # get all instances of tk alembic rop/sop nodes
        
        tk_cache_nodes = []

        tk_cache_nodes.extend(
            hou.nodeType(hou.sopNodeTypeCategory(), tk_node_type).instances()
        )

        return tk_cache_nodes

    @classmethod
    def get_output_path(cls,node):
        """
        Returns the evaluated output path for the supplied node.
        """

        output_parm = node.parm(cls.NODE_OUTPUT_PATH_PARM)
        path = output_parm.eval()
        return path

    # private methods
    
    def _getHipfileFields(self):

        # get the correct fields for the current hipfile

        current_file_path = hou.hipFile.path()
        work_fields = {}
        work_file_template = self._app.get_template("work_file_template")
        
        if work_file_template and work_file_template.validate(current_file_path):
            work_fields = work_file_template.get_fields(current_file_path)

        return work_fields
    
    
    def _computeOutputPath(self, node):

        # compute the output path based on the current work file and cache template

        # get relevant fields from the current file path
        work_file_fields = self._getHipfileFields()

        # get name attribute from node
        parm = node.parm("description")
        name = parm.eval()

        if not work_file_fields:
            msg = "This Houdini file is not a Shotgun Toolkit work file! Save the file through Shotgun save and create the node again."
            hou.ui.displayMessage(msg, buttons=('OK',), severity=hou.severityType.Error)
            raise sgtk.TankError(msg)

        # Get the cache templates from the app
        output_cache_template = self._app.get_template("output_cache_template")

        # create fields dict with all the metadata
        fields = {
            "SEQ": "FORMAT: $F",
            "version": work_file_fields.get("version", None),
            "name": name,
        }

        # update those fields with the output template
        fields.update(self._app.context.as_template_fields(output_cache_template))

        path = output_cache_template.apply_fields(fields)
        path = path.replace(os.path.sep, "/")

        return path