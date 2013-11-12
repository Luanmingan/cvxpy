"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from ... import utilities as u
from ... import interface as intf
from ...expressions import types
from ...expressions.variables import Variable
from elementwise import Elementwise
import numpy as np

class max(Elementwise):
    """ Elementwise maximum. """
    # Returns the elementwise maximum.
    @Elementwise.numpy_numeric
    def numeric(self, values):
        return reduce(np.maximum, values)

    # Verify that all the shapes are the same
    # or can be promoted.
    def validate_arguments(self):
        shape = self.args[0].shape
        for arg in self.args[1:]:
            shape = shape + arg.shape

    """
    Reduces the list of argument signs according to the following rules:
        POSITIVE, ANYTHING = POSITIVE
        ZERO, UNKNOWN = POSITIVE
        ZERO, ZERO = ZERO
        ZERO, NEGATIVE = ZERO
        UNKNOWN, NEGATIVE = UNKNOWN
        NEGATIVE, NEGATIVE = NEGATIVE
    """
    def sign_from_args(self):
        neg_mat = self.args[0].sign.neg_mat
        pos_mat = self.args[0].sign.pos_mat
        for arg in self.args[1:]:
            neg_mat = neg_mat & arg.sign.neg_mat
            pos_mat = pos_mat | arg.sign.pos_mat
        return u.Sign(neg_mat, pos_mat)

    # Default curvature.
    def func_curvature(self):
        return u.Curvature.CONVEX

    def monotonicity(self):
        return len(self.args)*[u.Monotonicity.INCREASING]

    def graph_implementation(self, arg_objs):
        t = Variable(*size)
        constraints = [x <= t for x in arg_objs]
        return (t, constraints)