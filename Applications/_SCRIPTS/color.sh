#!/bin/bash

# fg: "\e[38;2;<R>;<G>;<B>m" and bg: "\e[48;2;<R>;<G>;<B>m" end with "\e[0m"

#t=$(date +%s%3N)

if [[ $1 == '-h' ]] || [[ $1 == '--help' ]] || [[ $1 == '-?' ]]; then
	echo "Usage:"
	echo "	$(basename -- "$0") foreground_color background_color [-c|--capture] text"
	echo ""
	echo "Color formats:"
	echo "	#$($0 0xff0000 x Rr)$($0 0x00ff00 x Gg)$($0 0x0000ff x Bb)		- Color in hexadecimal"
	echo "	0x$($0 0xff0000 x Rr)$($0 0x00ff00 x Gg)$($0 0x0000ff x Bb)		- Color in hexadecimal"
	echo "	$($0 0xff0000 x rrr).$($0 0x00ff00 x ggg).$($0 0x0000ff x bbb)		- Color in decimals, separator can be anything but space"
	echo "	.	 		- Don't change, can be any one character but space"
	echo ""
	echo "Options:"
	echo "	--capture -c		- Capture all further arguments as text"
	echo ""
	echo "Help:"
	echo "	--help -h -?		- Display help"
	exit
fi

fg_color="$1"
bg_color="$2"
text="$3"
if [[ $text == '-c' ]] || [[ $text == '--capture' ]]; then
	shift; shift; shift
	text=$@
fi

RETURN=''

if [[ $fg_color =~ .{2,} ]]; then
	if [[ $fg_color =~ (0x|#)([0-9a-fA-F]{6}) ]]; then
		RETURN=$RETURN'\e[38;2;'$(printf "%d;%d;%d\n" "0x${BASH_REMATCH[2]:0:2}" "0x${BASH_REMATCH[2]:2:2}" "0x${BASH_REMATCH[2]:4:2}")'m'
	else
		RETURN=$RETURN'\e[38;2;'${fg_color//[^0-9]/';'}'m'
	fi
fi
if [[ $bg_color =~ .{2,} ]]; then
	if [[ $bg_color =~ (0x|#)([0-9a-fA-F]{6}) ]]; then
		RETURN=$RETURN'\e[48;2;'$(printf "%d;%d;%d\n" "0x${BASH_REMATCH[2]:0:2}" "0x${BASH_REMATCH[2]:2:2}" "0x${BASH_REMATCH[2]:4:2}")'m'
	else
		RETURN=$RETURN'\e[48;2;'${bg_color//[^0-9]/';'}'m'
	fi
fi

RETURN=$RETURN$text'\e[0m\n'

#echo $RETURN
#printf $[$(date +%s%3N)-$t]
printf "$RETURN"

#---*---TESTING AREA---*---

#php -r 'include_once("colors.inc.php");$ex=new GetMostCommonColors();$colors=$ex->Get_Color("55496796_p2.jpg", 10, true, true, 24);print_r($colors);' | grep =
#read -r -a phpcolors <<< $(php -r 'include_once("colors.inc.php");$ex=new GetMostCommonColors();$colors=$ex->Get_Color("55496796_p2.jpg", 10, true, true, 24);print_r($colors);' | grep =) && for var in "${phpcolors[@]}"; do if [[ $var =~ \[(.*)\] ]]; then color \#"${BASH_REMATCH[1]}" . \#"${BASH_REMATCH[1]}"; fi; done

#read -r -a colors <<< $(python ColorCube.py 55496796_p2.jpg | tr -d ' ][') && for var in "${colors[@]}"; do color $var . $var; done
