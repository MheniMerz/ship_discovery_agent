#!/bin/bash

#add environment variables to the bashrc
awk '{print "export "$0}' config/env_vars.env >> ~/.bashrc
. ~/.bashrc
