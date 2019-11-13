# xtabular
A simple python package to colorize the cells of LaTeX tables.

```
usage: xtabular.py [-h] -f FILE [-c COLUMN] [-r ROW] -col COLOR

This is a simple python script to colorize LaTex tables. It uses the xcolor
and colortbl LaTeX packages. Import them by adding '\usepackage{xcolor,
colortbl}' to your LaTeX document. You can use this script to color whole
rows, whole columns or a single cell, by specifying either the row '-r', the
column '-c' or both arguments.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file name
  -c COLUMN, --column COLUMN
                        Colum index (starts at 0)
  -r ROW, --row ROW     Row index (starts at 0)
  -col COLOR, --color COLOR
                        Color name
```                        

#### Known Bugs: 
* doesn't support '\hline, \vline, \cline' in the input table 
* doesn't check if color input is valid
* can't handle already colored columns in the input table (rows and cells work though)
