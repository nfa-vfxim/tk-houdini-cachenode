![Version Label](https://img.shields.io/badge/version-0.3.2-blue)
***

# tk-houdini-cachenode

>Dutch

Dit is een fork van de originele [tk-houdini-alembicnode](https://github.com/shotgunsoftware/tk-houdini-alembicnode) app. Deze app implementeert een node in Houdini waarmee naar Shotgun normale file caches kunnen worden gepublished.

>English

This is a fork of the original [tk-houdini-alembicnode](https://github.com/shotgunsoftware/tk-houdini-alembicnode) app. This app implements a node in Houdini with which you can publish normale file caches to Shotgun.

## Installation

### Forking / Cloning Pre-configured _sgtk_ configuration

The `tk-houdini-cachenode` is dependent on several other forks. We plan to refactor these forks into _sgtk_ hooks at one point, but for now you will have to use these forks as dependencies. 

The best way to install and use the app is to clone our pre-configured _sgtk_ [configuration](https://github.com/nfa-vfxim/nfa-shotgun-configuration).

### Manual Installation

If you'd still like to manually install the app, the following dependencies need to be configured in your _sgtk_ configuration.

#### Dependencies

- [tk-houdini](https://github.com/nfa-vfxim/tk-houdini)
- [tk-multi-publish2](https://github.com/nfa-vfxim/tk-multi-publish2)
- [tk-multi-loader2](https://github.com/nfa-vfxim/tk-multi-loader2)
- [tk-multi-breakdown](https://github.com/nfa-vfxim/tk-multi-breakdown)