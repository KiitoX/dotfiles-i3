#!/bin/bash

# syntax
# selector.sh <file> <output_file>

read -r -a colors <<< $(python /home/manuel/Applications/_SCRIPTS/ColorCube.py $1 | tr -d ' ][')

for var in "${!colors[@]}"; do
	colors_[$var]=$(color ${colors[$var]} . "██")
	colors__[$var]=$(color ${colors[$var]} . "${colors[$var]}")
	echo ${colors_[$var]} [$var] ${colors__[$var]}
done

echo -n 'Input key: '
read key
echo You chose ${colors_[$key]}
echo ${colors[$key]} > $2
exit
#sleep 3
