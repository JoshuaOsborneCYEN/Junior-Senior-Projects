#!/bin/bash

newTime=`nc time-c.timefreq.bldrdoc.gov 13 | sed '/^$/d'`
echo "$newTime"
