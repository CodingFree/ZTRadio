#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/student/Exercises/blocks/gr-multiplier/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/student/Exercises/blocks/gr-multiplier/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/student/Exercises/blocks/gr-multiplier/swig:$PYTHONPATH
/usr/bin/python2 /home/student/Exercises/blocks/gr-multiplier/python/qa_my_multiplier.py 
