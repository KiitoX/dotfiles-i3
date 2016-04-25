#!/bin/bash

# draw_bar <percentage> <full_length_in_char>
function draw_bar() {
	value=$[$1*100]
	return_value=''
	one_block_is=$[10000/$2]
	more_than_full_blocks=$[$value%$one_block_is]
	full_block_count=$[($value-$more_than_full_blocks)/$one_block_is]
	for (( i = 0; i < $2; i++ )); do
		if [[ $i -lt $full_block_count ]]; then
			return_value="$return_value█"
		else if [[ $i -eq $full_block_count ]]; then
			if [[ $more_than_full_blocks -eq 0 ]]; then
				val=0x0020
			else
				val=$[0x258F-($more_than_full_blocks*8)/$one_block_is]
				#echo -n $val

				#val=$[$val+]
				#Full block: U+2588
				#goes down in ⅛ steps
				#One eighth: U+258F
			fi
			return_value="$return_value$(printf "\u$(printf "%x" $val)")"
		else
			return_value="$return_value "
		fi; fi
	done
	echo -n "$return_value"
}

box_r=-1
r_bar=''
rd=''
rx=''

box_g=-1
g_bar=''
gd=''
gx=''

box_b=-1
b_bar=''
bd=''
bx=''

name_=$(printf "\e[4mCOLOUR\e[0m")

# draw_box <r> <g> <b> <r_bar> <g_bar> <b_bar>
function draw_box() {
	if [[ $1 -ne $box_r ]]; then
		box_r=$1
		r_bar="$(draw_bar $[(10000/255*$1)/100] 10)"
		rd=$(printf "%03d" $1)
		rx=$(printf "#%02x" $1)
	fi
	r_bar____=$(printf "\e[38;2;255;0;0;$4m$r_bar\e[0m")
	if [[ $2 -ne $box_g ]]; then
		box_g=$2
		g_bar="$(draw_bar $[(10000/255*$2)/100] 10)"
		gd=$(printf "%03d" $2)
		gx=$(printf "#%02x" $2)
	fi
	g_bar____=$(printf "\e[38;2;0;255;0;$5m$g_bar\e[0m")
	if [[ $3 -ne $box_b ]]; then
		box_b=$3
		b_bar="$(draw_bar $[(10000/255*$3)/100] 10)"
		bd=$(printf "%03d" $3)
		bx=$(printf "#%02x" $3)
	fi
	b_bar____=$(printf "\e[38;2;0;0;255;$6m$b_bar\e[0m")
	hexcl=$(printf "%02x%02x%02x" $1 $2 $3)
	block="$(color $1,$2,$3 . ██████)"
	echo "┏━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
	echo "┃ $name_ │               ┌DEC┬┬HEX┐ ┃"
	echo "┃▕$block▏│ R:▕$r_bar____▏│$rd││$rx│ ┃"
	echo "┃▕$block▏│               ╞═══╡╞═══╡ ┃"
	echo "┃▕$block▏│ G:▕$g_bar____▏│$gd││$gx│ ┃"
	echo "┃▕$block▏│               ╞═══╡╞═══╡ ┃"
	echo "┃▕$block▏│ B:▕$b_bar____▏│$bd││$bx│ ┃"
	echo "┃ ▔▔▔▔▔▔ │               └───┴┴───┘ ┃"
	echo "┠────────╆━━━━━━━━━━━━━━┯━━━━━━━━━━━┫"
	echo "┃ $hexcl ┃  x  -  exit  │   r g b   ┃"
	echo "┗━━━━━━━━┻━━━━━━━━━━━━━━┷━━━━━━━━━━━┛"
}

sel=0
inc=1
if [ $# -eq 0 ]; then
	color[0]="128"
	color[1]="128"
	color[2]="128"
else
	color[0]=$1
	color[1]=$2
	color[2]=$3
fi
bar[0]=48\;2\;20\;20\;20
bar[1]=49
bar[2]=49
echo -e '\033[?47h'
clear
draw_box ${color[0]} ${color[1]} ${color[2]} ${bar[0]} ${bar[1]} ${bar[2]}

while : ; do

	read -t 1 -sn 1 key

	case $key in
	'') ;; #ignore none
	i)
		printf "\e[2K\rInput increase value (currently: $inc): "
		read inc
		;&
	r)
		clear
		draw_box ${color[0]} ${color[1]} ${color[2]} ${bar[0]} ${bar[1]} ${bar[2]}
		;;
	x)
		;&
	$'\e')
		printf "\e[2K\rExiting... (c to cancel)"
		read -t 1 -sn 1 esc_key
		case $esc_key in
		[)
			read -t 1 -sn 1 arrow_key
			case $arrow_key in
			'') break; break;; #only esc to exit
			A)
				printf "\e[2K\rup"
				bar[$sel]=49
				sel=$[($sel-1)%3]
				bar[$sel]=48\;2\;20\;20\;20
				;;&
			B)
				printf "\e[2K\rdown"
				bar[$sel]=49
				sel=$[($sel+1)%3]
				bar[$sel]=48\;2\;20\;20\;20
				;;&
			C)
				printf "\e[2K\rright"
				color[$sel]=$[(${color[$sel]}+$inc)%256]
				;;&
			D)
				printf "\e[2K\rleft"
				color[$sel]=$[(${color[$sel]}-$inc)%256]
				;;&
			*)
				clear
				draw_box ${color[0]} ${color[1]} ${color[2]} ${bar[0]} ${bar[1]} ${bar[2]}
				;;
			esac
			;;
		c)
			clear
			draw_box ${color[0]} ${color[1]} ${color[2]} ${bar[0]} ${bar[1]} ${bar[2]}
			;;
		*)
			break; break
			;;
		esac
		;;
	*)
		printf "\e[2K\r$key"
		;;
	esac

	# if [[ $[$(date +%s)%1] -eq 0 ]]; then
	# 	clear
	# 	draw_box ${color[0]} ${color[1]} ${color[2]} ${bar[0]} ${bar[1]} ${bar[2]}
	# fi
done

clear
echo -e '\033[?47l'
