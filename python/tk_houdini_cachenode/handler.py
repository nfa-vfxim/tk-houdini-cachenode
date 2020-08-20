import sgtk
import hou
import os

class TkCacheNodeHandler(object):

    def __init__(self, app):
        self._app = app

    def setupNode(self, node):
        
        # get parameters and computed output path
        path = node.parm("path")
        pathString = node.parm("pathString")
        outputPath = self._computeOutputPath(node)

        try:
            pathString.set(outputPath)
            path.set(outputPath)
        except:
            e = "The output path could not be calculated!"
            raise sgtk.TankError(e)

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

        if not work_file_fields:
            msg = "This Houdini file is not a Shotgun Toolkit work file!"
            raise sgtk.TankError(msg)

        # Get the cache templates from the app
        output_cache_template = self._app.get_template("output_cache_template")

        # create fields dict with all the metadata
        fields = {
            "SEQ": "FORMAT: $F",
            "version": work_file_fields.get("version", None),
        }

        # update those fields with the output template
        fields.update(self._app.context.as_template_fields(output_cache_template))

        path = output_cache_template.apply_fields(fields)
        path = path.replace(os.path.sep, "/")

        return path