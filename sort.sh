#!/usr/bin/bash

MATCH="2023022"

mkdir -p sorted/

ls files/* | while read -r f; do
	# not an actual loop, but used as a hack to use break as soon as correct date is found
	while [[ True ]] ; do
		dt=""
		t=""
		d=""
		#####################################################################
		# filename like 20230301_235959 (or with seperators in between)
		regex='(20[012][0-9])[ _-]?(0[1-9]|10|11|12)[ _-]?(0[1-9]|[12][0-9]|30|31).*([01][0-9]|2[0-3])([0-5][0-9])([0-5][0-9])'
		if [[ $f =~ $regex ]]; then 
			d=${BASH_REMATCH[1]}${BASH_REMATCH[2]}${BASH_REMATCH[3]}
			t=${BASH_REMATCH[4]}${BASH_REMATCH[5]}${BASH_REMATCH[6]}
			dt=${d}"_"${t}
			break;
		fi
		#####################################################################
		# filename like 235959_20230301 (or with seperators in between)
		regex='([01][0-9]|2[0-3])([0-5][0-9])([0-5][0-9]).*(20[012][0-9])[ _-]?(0[1-9]|10|11|12)[ _-]?(0[1-9]|[12][0-9]|30|31)'
		if [[ $f =~ $regex ]]; then 
			t=${BASH_REMATCH[1]}${BASH_REMATCH[2]}${BASH_REMATCH[3]}
			d=${BASH_REMATCH[4]}${BASH_REMATCH[5]}${BASH_REMATCH[6]}
			dt=${d}"_"${t}
			break;
		fi
		#####################################################################
		# exifdata "createdate"
		e=$(exiftool -T -CreateDate -d "%Y%m%d_%H%M%S" "$f")
		if [[ $e =~ ^202.*$ ]]; then
			dt="$e"
			d=$(exiftool -T -CreateDate -d "%Y%m%d" "$f")
			t=$(exiftool -T -CreateDate -d "%H%M%S" "$f")
			break;
		fi
		#####################################################################
		# exifdata "creationdate"
		e=$(exiftool -T -CreationDate -d "%Y%m%d_%H%M%S" "$f")
		if [[ $e =~ ^202.*$ ]]; then
			dt="$e"
			d=$(exiftool -T -CreationDate -d "%Y%m%d" "$f")
			t=$(exiftool -T -CreationDate -d "%H%M%S" "$f")
			break;
		fi
		#####################################################################
		# filename like single date 20230301
		regex='(20[012][0-9])[ _-]?(0[1-9]|10|11|12)[ _-]?(0[1-9]|[12][0-9]|30|31)'
		if [[ $f =~ $regex ]]; then 
			d=${BASH_REMATCH[1]}${BASH_REMATCH[2]}${BASH_REMATCH[3]}
			break;
		fi
		#####################################################################
		break
	done
	nicef="${f##files/}"
	nicef="${nicef// /_}"
	if [[ $dt != "" ]]; then
		echo cp -v "$f" sorted/"${dt}_${nicef}"
		cp -v "$f" sorted/"${dt}_${nicef}"
	elif [[ $d != "" ]]; then
		echo cp -v "$f" sorted/"${d}_XXXXXX_${nicef}"
		cp -v "$f" sorted/"${d}_XXXXXX_${nicef}"
	else
		echo cp -v "$f" sorted/202XXXXX_XXXXXX_"${nicef}"
		cp -v "$f" sorted/202XXXXX_XXXXXX_"${nicef}"
	fi
done

