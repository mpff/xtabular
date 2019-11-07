#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import xtabular



class LayoutTest(unittest.TestCase):

    def test_can_extract_cells_nrows_and_ncols(self):
        simple_table = r"""
            \begin{tabular}{ l | c || r }
            1 & 2 & 3 \\ 
            4 & 5 & 6 \\
            7 & 8 & 9 
            \end{tabular}
        """
        table = xtabular.LatexTable(simple_table)
        self.assertEqual(table.nrows,3)
        self.assertEqual(table.ncols,3)
        self.assertEqual(table.cells,[['1','2','3'],['4','5','6'],['7','8','9']])
        

    def test_no_env_fails_gracefully(self):
        table_no_env = """\\begin{tabular}{ l c r }
            1 & 2 & 3 \\\\
            4 & 5 & 6 \\\\
            7 & 8 & 9"""
        with self.assertRaises(Exception) as error:
            xtabular.LatexTable(table_no_env)
        self.assertEqual(str(error.exception), 'Table has no tabular environment.')

        
    def test_wrong_pos_argument_fails_gracefully(self):
        table_wrong_pos_argument = """\\begin{tabular}{ l c banana }
            1 & 2 & 3 \\\\
            4 & 5 & 6 \\\\
            7 & 8 & 9
            \end{tabular}"""
        with self.assertRaises(Exception) as error:
            xtabular.LatexTable(table_wrong_pos_argument)
        self.assertEqual(str(error.exception), 'Table has no or invalid positional arguments. Valid positional arguments are: c r l | ||.')


    def test_missing_delimiters_fails_gracefully(self):
        table_missing_delimiters = """\\begin{tabular}{ l c r }
            1 & 2   3 \\\\
            4 & 5 & 6 \\\\
            7 & 8 & 9
            \end{tabular}"""
        with self.assertRaises(Exception) as error:
            xtabular.LatexTable(table_missing_delimiters)
        self.assertEqual(str(error.exception), "Number of cell delimiters ('&') does not match number of columns specified by positional arguments.")


    def test_missing_breaks_fails_gracefully(self):
        table_missing_breaks = """\\begin{tabular}{ l c r }
            1 & 2 & 3 \\\\
            4 & 5 & 6 
            7 & 8 & 9
            \end{tabular}"""
        with self.assertRaises(Exception) as error:
            xtabular.LatexTable(table_missing_breaks)
        self.assertEqual(str(error.exception), "Number of cell delimiters ('&') does not match number of columns specified by positional arguments.")



class ColorizeTest(unittest.TestCase):

    indices = [(1,1), (2,2), (3,3)]
    colors = ["#FF0000", "#00FF00", "#0000FF"]

    def setUp(self):
        simple_table = r"""
            \begin{tabular}{ l | c || r }
            1 & 2 & 3 \\ 
            4 & 5 & 6 \\
            7 & 8 & 9 
            \end{tabular}
        """
        self.table = xtabular.LatexTable(simple_table)


    def test_can_colorize_a_cell(self):
        self.table.colorize(0,0,'red')
        self.assertEqual(r'\cellcolor{red}1', self.table.cells[0][0])


    def test_indices_outside_of_table_fails_gracefully(self):
        indices_fail = [(4,1), (2,4), (4,4)]
        return True


    def test_noninteger_indices_fails_gracefully(self):
        indices_fail = [(4.1,1), (2,4), "banana"]
        return True


    def test_nonhex_colors_fails_gracefully(self):
        colors_fail = ["banana", "#FF00000", "FF0000"]
        return True



if __name__ == '__main__':
    unittest.main()
