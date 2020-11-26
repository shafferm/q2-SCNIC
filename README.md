[![Build Status](https://travis-ci.com/shafferm/q2-SCNIC.svg?branch=master)](https://travis-ci.com/shafferm/q2-SCNIC) [![Coverage Status](https://coveralls.io/repos/github/shafferm/q2-SCNIC/badge.svg?branch=master)](https://coveralls.io/github/shafferm/q2-SCNIC?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/8269a44ae11f48399bf56eedd2dd7ad6)](https://www.codacy.com/app/shafferm/q2-SCNIC?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shafferm/q2-SCNIC&amp;utm_campaign=Badge_Grade)

# NOTE

The most up to date version of the q2-SCNIC repo is [here](https://github.com/lozuponelab/q2-SCNIC)! This repo is being deprecated and will not be the main source of q2-SCNIC.

# q2-SCNIC

A package for accessing the primary methods of [SCNIC](https://www.github.com/lozuponelab/SCNIC) via QIIME2.

# Installation

First, make sure you have SCNIC installed:

```
conda install -q scnic
```

OR

```
pip install scnic
```

Next to install the plugin:

```
pip install git+https://github.com/lozuponelab/q2-SCNIC.git
qiime dev refresh-cache
```

Finally to see what functions are available, you can use:

```
qiime SCNIC --help
```
