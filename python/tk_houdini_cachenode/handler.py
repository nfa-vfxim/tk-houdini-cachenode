# built-in packages
import base64
import os
import sys
import zlib

from sgtk.util import pickle

# houdini
import hou

# toolkit
import sgtk

class TkCacheNodeHandler(object):
    # handle all callbacks and operations for the file cache node app

    # the name of the output path parameter on the node
    NODE_OUTPUT_PATH_PARM = "path"

    def __init__(self, app):

        # initialize the handler

        self._app = app

    # returns a list of menu items for the current node
    def get_output_path_menu_items(self):

        menu = ["sgtk"]
        current_node = hou.pwd()

        # attempt to compute the output path and add it as an item in the menu
        try:
            menu.append(self._compute_output_path(current_node))
        except sgtk.TankError as e:
            error_msg = "Unable to construct the output path menu items: " "%s - %s" % (
                current_node.name(),
                e,
            )
            self._app.log_error(error_msg)
            menu.append("ERROR: %s" % (error_msg,))

        return menu

    # apply the selected profile in the session
    def set_profile(self, node=None):

        if not node:
            node = hou.pwd()

        output_profile = self._get_output_profile(node)

        self._app.log_debug(
            "Applying tk alembic node profile: %s" % (output_profile["name"],)
        )

        # apply the supplied settings to the node
        settings = output_profile["settings"]
        if settings:
            self._app.log_debug("Populating format settings: %s" % (settings,))
            node.setParms(settings)

        # set the node color
        color = output_profile["color"]
        if color:
            node.setColor(hou.Color(color))

        self.refresh_output_path(node)

    # refresh the output profile path
    def refresh_output_path(self, node):

        output_path_parm = node.parm(self.NODE_OUTPUT_PATH_PARM)
        output_path_parm.set(output_path_parm.eval())

    # called when the node is created.
    def setup_node(self, node):

        default_name = self._app.get_setting("default_node_name")
        node.setName(default_name, unique_name=True)

        # apply the default profile
        self.set_profile(node)

        try:
            self._app.log_metric("Create", log_version=True)
        except:
            # ingore any errors. ex: metrics logging not supported
            pass

    ############################################################################
    # Private methods

    # compute the output path based on the current work file and cache template
    def _compute_output_path(self, node):

        # get relevant fields from the current file path
        work_file_fields = self._get_hipfile_fields()

        if not work_file_fields:
            msg = "This Houdini file is not a Shotgun Toolkit work file!"
            raise sgtk.TankError(msg)

        # Get the cache templates from the app
        output_cache_template = self._app.get_template("output_cache_template")

        # create fields dict with all the metadata
        fields = {
            "name": work_file_fields.get("name", None),
            "node": node.name(),
            "renderpass": node.name(),
            "SEQ": "FORMAT: $F",
            "version": work_file_fields.get("version", None),
        }

        fields.update(self._app.context.as_template_fields(output_cache_template))

        path = output_cache_template.apply_fields(fields)
        path = path.replace(os.path.sep, "/")

        return path

    # get the current output profile
    def _get_output_profile(self, node=None):

        if not node:
            node = hou.pwd()

        output_profile_parm = node.parm(self.TK_OUTPUT_PROFILE_PARM)
        output_profile_name = output_profile_parm.menuLabels()[
            output_profile_parm.eval()
        ]
        output_profile = self._output_profiles[output_profile_name]

        return output_profile

    # extract fields from current Houdini file using the workfile template
    def _get_hipfile_fields(self):
        current_file_path = hou.hipFile.path()

        work_fields = {}
        work_file_template = self._app.get_template("work_file_template")
        if work_file_template and work_file_template.validate(current_file_path):
            work_fields = work_file_template.get_fields(current_file_path)

        return work_fields

    # get the render path from current item in the output path parm menu
    def _get_render_path(self, node):
        output_parm = node.parm(self.NODE_OUTPUT_PATH_PARM)
        path = output_parm.menuLabels()[output_parm.eval()]
        return path

    # returns the files on disk associated with this node
    def _get_rendered_files(self, node):

        file_name = self._get_render_path(node)

        output_profile = self._get_output_profile(node)

        # get the output cache template for the current profile
        output_cache_template = self._app.get_template_by_name(
            output_profile["output_cache_template"]
        )

        if not output_cache_template.validate(file_name):
            msg = (
                "Unable to validate files on disk for node %s."
                "The path '%s' is not recognized by Shotgun." % (node.name(), file_name)
            )
            self._app.log_error(msg)
            return []

        fields = output_cache_template.get_fields(file_name)

        # get the actual file paths based on the template. Ignore any sequence
        # or eye fields
        return self._app.tank.paths_from_template(
            output_cache_template, fields, ["SEQ", "eye"]
        )


################################################################################
# Utility methods

# Copy all the input connections from this node to the target node.
def _copy_inputs(source_node, target_node):

    input_connections = source_node.inputConnections()
    num_target_inputs = len(target_node.inputConnectors())

    if len(input_connections) > num_target_inputs:
        raise hou.InvalidInput(
            "Not enough inputs on target node. Cannot copy inputs from "
            "'%s' to '%s'" % (source_node, target_node)
        )

    for connection in input_connections:
        target_node.setInput(connection.inputIndex(), connection.inputNode())


# Copy parameter values of the source node to those of the target node if a
# parameter with the same name exists.
def _copy_parm_values(source_node, target_node, excludes=None):

    if not excludes:
        excludes = []

    # build a parameter list from the source node, ignoring the excludes
    source_parms = [parm for parm in source_node.parms() if parm.name() not in excludes]

    for source_parm in source_parms:

        source_parm_template = source_parm.parmTemplate()

        # skip folder parms
        if isinstance(source_parm_template, hou.FolderSetParmTemplate):
            continue

        target_parm = target_node.parm(source_parm.name())

        # if the parm on the target node doesn't exist, skip it
        if target_parm is None:
            continue

        # if we have keys/expressions we need to copy them all.
        if source_parm.keyframes():
            for key in source_parm.keyframes():
                target_parm.setKeyframe(key)
        else:
            # if the parameter is a string, copy the raw string.
            if isinstance(source_parm_template, hou.StringParmTemplate):
                target_parm.set(source_parm.unexpandedString())
            # copy the evaluated value
            else:
                try:
                    target_parm.set(source_parm.eval())
                except TypeError:
                    # The pre- and post-script type comboboxes changed sometime around
                    # 16.5.439 to being string type parms that take the name of the language
                    # (hscript or python) instead of an integer index of the combobox item
                    # that's selected. To support both, we try the old way (which is how our
                    # otl is setup to work), and if that fails we then fall back on mapping
                    # the integer index from our otl's parm over to the string language name
                    # that the alembic node is expecting.
                    if source_parm.name().startswith(
                        "lpre"
                    ) or source_parm.name().startswith("lpost"):
                        value_map = ["hscript", "python"]
                        target_parm.set(value_map[source_parm.eval()])
                    else:
                        raise


# return the menu label for the supplied parameter
def _get_output_menu_label(parm):
    if parm.menuItems()[parm.eval()] == "sgtk":
        # evaluated sgtk path from item
        return parm.menuLabels()[parm.eval()]
    else:
        # output path from menu label
        return parm.menuItems()[parm.eval()]


# move all the output connections from the source node to the target node
def _move_outputs(source_node, target_node):

    for connection in source_node.outputConnections():
        output_node = connection.outputNode()
        output_node.setInput(connection.inputIndex(), target_node)


# saves output connections into user data of target node. Needed when target
# node doesn't have outputs.
def _save_outputs_to_user_data(source_node, target_node):

    output_connections = source_node.outputConnections()
    if not output_connections:
        return

    outputs = []
    for connection in output_connections:
        output_dict = {
            "node": connection.outputNode().path(),
            "input": connection.inputIndex(),
        }
        outputs.append(output_dict)

    # get the current encoder for the handler
    handler_cls = TkAlembicNodeHandler
    codecs = handler_cls.TK_OUTPUT_CONNECTION_CODECS
    encoder = codecs[handler_cls.TK_OUTPUT_CONNECTION_CODEC]["encode"]

    # encode and prepend the current codec name
    data_str = handler_cls.TK_OUTPUT_CONNECTION_CODEC + ":" + encoder(outputs)

    # set the encoded data string on the input node
    target_node.setUserData(handler_cls.TK_OUTPUT_CONNECTIONS_KEY, data_str)


# restore output connections from this node to the target node.
def _restore_outputs_from_user_data(source_node, target_node):

    data_str = source_node.userData(TkAlembicNodeHandler.TK_OUTPUT_CONNECTIONS_KEY)

    if not data_str:
        return

    # parse the data str to determine the codec used
    sep_index = data_str.find(":")
    codec_name = data_str[:sep_index]
    data_str = data_str[sep_index + 1 :]

    # get the matching decoder based on the codec name
    handler_cls = TkAlembicNodeHandler
    codecs = handler_cls.TK_OUTPUT_CONNECTION_CODECS
    decoder = codecs[codec_name]["decode"]

    # decode the data str back into original python objects
    outputs = decoder(data_str)

    if not outputs:
        return

    for connection in outputs:
        output_node = hou.node(connection["node"])
        output_node.setInput(connection["input"], target_node)