#!/bin/bash

printf '{"stop_signal": 20, "cont_signal": 18, "click_events": true, "version": 1}' #header
printf '\n[' #start
printf '\n[{"name": "debug", "full_text": "DEBUG; CLICK ME!"}]' #block

while true; do
	IFS= read -r -t 1 line
	printf '\n,[{"name": "debug", "full_text": "DEBUG; CLICK ME!"}]' #block
	if [[ ${#line} -gt 0 ]]; then
		printf '***%s***%s***\n' "$(date)" "$line" >> '/home/manuel/.config/i3status/log'
	fi
done
