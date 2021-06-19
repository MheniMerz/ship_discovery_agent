#!/bin/bash

#add environment variables to the bashrc
cat ./config/env_vars.env >> ~/.bashrc
. ~/.bashrc
