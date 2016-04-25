#!/bin/bash

UPD_ID=700
VOL_ID=701
BRIGHT_ID=702

case $1 in
check-update)
	notify-send -a 'i3' -r $UPD_ID -t 0 'Update' 'checking...'
	u=$(dnf check-update > /dev/null; echo $?)
	if [[ $u = 100 ]];
	then t="Updates available [return:$u]\nTo update now press Win+Ctrl+Shift+U"
	else t="No updates found [return:$u]"
	fi
	notify-send -a 'i3' -r $UPD_ID -t 0 -u 'critical' 'Update' "$t"
	;;
do-update)
	$0 xterm-f -T _FLOATING_ -e $0 $1_
	#notify-send -a 'i3' -r $UPD_ID -t 0 'Update' 'You might want to update the grub config\n"sudo grub2-mkconfig -o /boot/grub2/grub.cfg"'
	;;
do-update_)
	notify-send -a 'i3' -r $UPD_ID -t 10 -u 'critical' 'Update' "Updating..."
	echo -e "[\e[38;5;244m$(date +%H:%M)\e[0m \e[38;5;64m\$cript \e[38;5;37m~\e[0m]$ sudo dnf upgrade"
	sudo dnf upgrade
	printf "[\e[38;5;244m$(date +%H:%M)\e[0m \e[38;5;64m\$cript \e[38;5;37m~\e[0m]$\n> sudo grub2-mkconfig -o /boot/grub2/grub.cfg\n"
	printf "[\e[38;5;244m$(date +%H:%M)\e[0m \e[38;5;64m\$cript \e[38;5;37m~\e[0m]$\n> [\e[31me\e[38;5;244mxit\e[0m/\e[38;5;37ms\e[38;5;244mhell\e[0m]: "
	read cmd
	case $cmd in
	e)
		exit
		;;
	s)
		bash
		;;
	esac
	;;
transparent)
	i3-input -F \
'exec echo $(compton-trans "%s" & '\
'echo $(sleep 0.01 && '\
'[[ $(xdotool getmouselocation) =~ x:([0-9]+)\ y:([0-9]+) ]] && '\
'xdotool mousemove ${BASH_REMATCH[1]} ${BASH_REMATCH[2]} click 1 && '\
'xdotool mousemove ${BASH_REMATCH[1]} ${BASH_REMATCH[2]} click 1))' \
-P 'Transparency(a): ' #TODO: check if window in focus maybe or something similar...
	;;
transparent_i)
	i3-input -F 'exec compton-trans "%s"' -P 'Transparency: '
	;;
maximize)
	n=$(i3-msg -t get_workspaces | jq '.[] | select(.visible == true).name')
	p=~/.config/i3/__border/__"${n:1:-1}"
	if [[ ! -f $p ]];
	then echo "$2" > "$p";
	fi
	if [[ $(cat "$p") = 0 ]];
	then v="$2"
	else v=0
	fi
	echo "$v" > "$p";
	i3 "gaps inner current set $(cat $p)"
	;;
notify_help)
	notify-send 'Dunst help' '+M    - Close last\n++M - Close all\n+N    - Reopen last\n+B    - Open context menu'
	;;
dunstify_shell)
	shift
	var=$(dunstify $@)
	if [[ ${#var} -gt 0 ]]; then
		if ! [[ $var =~ ^[0-9]+$ ]]; then
			$($var)
		fi
	fi
	;;
bright_up)
	$0 bright_ +$2
	;;
bright_dn)
	$0 bright_ -$2
	;;
bright_)
	m=$(cat /sys/class/backlight/radeon_bl0/brightness)
	$0 bright $[$m $2]
	;;
bright)
	echo $2 > /sys/class/backlight/radeon_bl0/brightness
	$0 update_status
	m=$(cat /sys/class/backlight/radeon_bl0/brightness)
	notify-send "Brightness $m" -a 'i3status' -t 1 -r $BRIGHT_ID
	;;
vol_up)
	$0 vol volume +$2%
	;;
vol_dn)
	$0 vol volume -$2%
	;;
vol_mt)
	$0 vol mute toggle
	;;
vol)
	pactl set-sink-$2 @DEFAULT_SINK@ $3
	$0 update_status
	full=$(pacmd list-sinks)
	sink=$(pacmd stat | awk -F": " '/^Default sink name: /{print $2}')
	m=$(echo -e "$full" | awk '/^\s+name: /{indefault = $2 == "<'$sink'>"}/^\s+muted: / && indefault {print $2; exit}')
	v=$(echo -e "$full" | awk '/^\s+name: /{indefault = $2 == "<'$sink'>"}/^\s+volume: / && indefault {print $5; exit}')
	notify-send "Volume $v (muted: $m)" -a 'i3status' -t 1 -r $VOL_ID
	;;
shutdown_menu)
	#/lib/systemd/system-sleep/i3sleep-tweaks.sh
	i3-nagbar -t warning -m 'Power off:' \
		-b 'Sleep (RAM)' 		"systemctl suspend" \
		-b 'Sleep (HDD)' 		"systemctl hibernate" \
		-b 'Sleep (RAM & HDD)' 	"systemctl hybrid-sleep" \
		-b 'Exit i3' 			"i3-msg exit" \
		-b 'Reboot' 			"systemctl reboot" \
		-b 'Shutdown' 			"systemctl poweroff"
	;;
update_status)
	kill -SIGUSR1 $(ps aux | grep /bar_0.py | grep -v grep | awk '{ print $2 }')
	;;
xterm-f)
	shift # -fn 7x13 -fa "Dejavu Sans Mono:size=9:antialias=true"
	xterm -u8 -rv -rightbar -fn 7x13 -fa "Dejavu Sans Mono" -fs 9 -w 0 $@
	;;
st-f)
	shift
	st -f "Dejavu Sans Mono" $@
	;;
st-c-f)
	shift
	st-c -f "Dejavu Sans Mono" $@
	;;
*)
	i3-nagbar -t warning -m "do.sh, unknown command: '$*' ($1)"
	;;
esac
