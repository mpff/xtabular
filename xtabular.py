#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Manuel Pfeuffer"

import sys
import argparse
import re


class LatexTable():

    def __init__(self, table):
        '''
        Breaks down input table into positonal arguments (pos_args)and cell
        contents (cells).Also extracts number of rows (nrows) and number of
        columns (ncols).
        '''

        table = self._flatten(table)

        self._has_tabular_environment(table)  # Raises if not
        table = self._strip_env(table)

        self.pos_args = self._get_pos_arguments(table)
        table = self._strip_pos_args(table)

        self.ncols = len([arg for arg in self.pos_args if arg not in ['|','||']])

        self._delimiters_match_pos_args(table)  # Raises if not

        table = re.split(r"\\\\", table)
        table = [row for row in table if row != '']  # Remove '' generated by re.split

        self.nrows = len(table)

        self.cells = [re.split(r"&", row) for row in table]


    def colorize(self, row, col, color):
        '''Adds \cellcolor{color} to specified cell.'''

        if row > self.nrows or col > self.ncols:
            raise Exception("Cell index out of range.")

        self.cells[row][col] = r'\cellcolor{' + color + '}' + self.cells[row][col]

        return None

    
    def colorize_row(self, row, color):
        '''Adds \\rowcolor{color} to start of specified row.'''

        if row > self.nrows:
            raise Exception("Row index out of range.")
        
        self.cells[row][0] = r'\rowcolor{' + color + '}' + self.cells[row][0]

        return None


    def colorize_column(self, col, color):
        '''Adds >{\columncolor{color}} to specified column.'''

        if col > self.ncols:
            raise Exception("Column index out of range.")

        pargs = [[i,arg] for i,arg in enumerate(self.pos_args) if arg not in ['|','||']]
        parg = pargs[col]
        self.pos_args[parg[0]] = r'>{\columncolor{' + color + '}}' + self.pos_args[parg[0]]

        return None


    def to_tex(self):
        '''Returns LatexTable as LaTeX tabular table.'''

        # Begin tabular environment and add positional arguments.
        table = r"\begin{tabular}{ "
        for arg in self.pos_args:
            table = table + arg + " "
        table = table + "}\n"

        # Add the table content cellwise.
        for row in self.cells:
            table = table + "\t"
            for cell in row:
                table = table + cell + " & "                
            table = table[:-3]
            table = table + r" \\" + "\n"
        
        # Close tabular environment.
        table = table[:-4] + "\n"
        table = table + r"\end{tabular}"

        return table


    def _flatten(self, table):
        table = table.strip()
        table = table.replace("\t", "")
        table = table.replace("\n", "")
        table = table.replace(" ", "")
        return table


    def _strip_env(self, table):
        table = table.replace("\\begin{tabular}", "") 
        table = table.replace("\end{tabular}", "")
        table = table.strip()
        return table


    def _strip_pos_args(self, table):
        stripper = '{'
        for arg in self.pos_args:
            stripper += arg
        stripper += '}'
        return table[len(stripper):]


    def _has_tabular_environment(self, table):
        match = re.search(r"^\\begin{tabular}.*\\end{tabular}$", table)
        if not match:
            raise Exception('Table has no tabular environment.')
        return None


    def _get_pos_arguments(self, table):
        match = re.search(r"^\{[lcr|]*\}", table)
        if not match:
            raise Exception('Table has no or invalid positional arguments. Valid positional arguments are: c r l | ||.')
        match = match.group(0)  # should only have one match!
        match = match.replace("{", "")
        match = match.replace("}", "")
        match = re.findall(r"\|{2}|[lcr|]", match)
        return(match)


    def _delimiters_match_pos_args(self, table):
        """TODO: This is garbage code. Refactor! (But it seems to work)"""
        match = re.findall(r"&|\\{2}", table)
        for i,d in enumerate(match):
            if d == r'\\' and (i+1)%self.ncols != 0:
                raise Exception("Number of cell delimiters ('&') does not match number of columns specified by positional arguments.")
        if not len(match)%self.ncols == (self.ncols-1):
            raise Exception("Number of cell delimiters ('&') does not match number of columns specified by positional arguments.")
        return None



def main():

    parser = argparse.ArgumentParser(
        description=("This is a simple python script to colorize LaTex tables. "
                     "It uses the xcolor and colortbl LaTeX packages. Import "
                     "them by adding '\\usepackage{xcolor, colortbl}' to your "
                     "LaTeX document. "
                     "You can use this script to color whole rows, whole "
                     "columns or a single cell, by specifying either the row "
                     "'-r', the column '-c' or both arguments.")
    )
                     
    

    parser.add_argument(
            '-f','--file',
            help='Input file name',
            required=True
    )

    parser.add_argument(
            '-c', '--column', type=int,
            help='Colum index (starts at 0)',
            required=False
    )

    parser.add_argument(
            '-r', '--row', type=int,
            help='Row index (starts at 0)',
            required=False
    )

    parser.add_argument(
            '-col', '--color',
            help='Color name',
            required=True
    )

    args = parser.parse_args()

    if args.row is None and args.column is None:
        parser.error("At least one of --column and --row is required.")

    with open(args.file, 'r') as file:
        tex_table = file.read()

    table = LatexTable(tex_table)

    if args.row is None:
        table.colorize_column(args.column,args.color)
    elif args.column is None:
        table.colorize_row(args.row,args.color)
    else:
        table.colorize(args.row,args.column,args.color)

    sys.stdout.write(table.to_tex())



if __name__ == "__main__":
    main()
