[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/nfa-vfxim/tk-houdini-cachenode?include_prereleases)](https://github.com/nfa-vfxim/tk-houdini-cachenode) 
[![GitHub issues](https://img.shields.io/github/issues/nfa-vfxim/tk-houdini-cachenode)](https://github.com/nfa-vfxim/tk-houdini-cachenode/issues) 


# File Cache Node

Support for the Toolkit File Cache node in Houdini.

> Supported engines: tk-houdini

## Requirements

| ShotGrid version | Core version | Engine version |
|------------------|--------------|----------------|
| -                | v0.12.5      | v1.7.1         |

## Configuration

### Templates

| Name                      | Description                                                                                                                                     | Default value | Fields                    |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------------------------|
| `work_file_template`      | A reference to a template which locates a Houdini work file on disk. This is used to drive the version and optionally the name of output files. |               | context, version, [name]  |
| `output_cache_template`   | A reference to a template which defines where the bgeo cache will be written to disk.                                                           |               | context, version, name, * |
| `output_publish_template` | A reference to a template which defines where the published bgeo cache will be copied to.                                                       |               | context, version, name, * |


