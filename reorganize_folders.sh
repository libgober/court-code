for year in `seq 1800 2000`; do cd $year; for f in *.txt; do mkdir "${f%????}"; mv "$f" "${f%????}"; done; cd ..; done;
