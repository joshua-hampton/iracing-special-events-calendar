#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python ${SCRIPT_DIR}/../src/create_calendar.py ${SCRIPT_DIR}/../calendars/iracing_special_events.ics $(find ${SCRIPT_DIR}/../events -type f)