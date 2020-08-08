'''
    MODIFIED BY: Thomas Weathers - May 2020
    Created by: Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

from Board import Board


x = Board(15, 15);


x.set_cell( 4, 4, 'x')

x.set_cell( 1, 3, 'B')


x.display()

y = x.cloneBoard();
y.display();
