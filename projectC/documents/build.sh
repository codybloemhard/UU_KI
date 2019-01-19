latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf report.tex
pkill -HUP mupdf
