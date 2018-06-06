"""Contains the Pdb class and functions for opening them."""

import datetime
from ..models.molecules import Model

class Pdb:
    """A Pdb is used to represent a fully processed PDB file."""

    def __init__(self):
        self._models = []
        self._code, self._deposition_date = None, None
        self._title = None
        self._resolution = None
        self._organism = None
        self._expression_system = None
        self._technique = None
        self._classification = None
        self._rfactor = None
        self._keywords = []


    def __repr__(self):
        num = len(self._models)
        return "<Pdb {}({} model{})>".format(
         self._code + " " if self._code else "", num, "" if num == 1 else "s"
        )


    @property
    def models(self):
        """Returns the :py:class:`.Model` objects that the Pdb contains.

        :rtype: ``tuple``"""

        return tuple(self._models)


    @property
    def model(self):
        """Returns the first :py:class:`.Model` that the Pdb file contains."""

        return self._models[0] if self._models else None


    @property
    def code(self):
        """The Pdb's 4-letter code.

        :rtype: ``str``"""

        return self._code


    @code.setter
    def code(self, code):
        self._code = code


    @property
    def deposition_date(self):
        """The Pdb's desposition date.

        :rtype: ``datetime.date``"""

        return self._deposition_date


    @deposition_date.setter
    def deposition_date(self, deposition_date):
        self._deposition_date = deposition_date


    @property
    def title(self):
        """The Pdb's title.

        :rtype: ``str``"""

        return self._title


    @title.setter
    def title(self, title):
        self._title = title



    @property
    def resolution(self):
        """The Pdb's resolution.

        :rtype: ``float``"""

        return self._resolution


    @resolution.setter
    def resolution(self, resolution):
        self._resolution = resolution



    @property
    def rfactor(self):
        """The Pdb's R-factor.

        :rtype: ``float``"""

        return self._rfactor


    @rfactor.setter
    def rfactor(self, rfactor):
        self._rfactor = rfactor


    @property
    def organism(self):
        """The Pdb's source organism.

        :rtype: ``str``"""

        return self._organism


    @organism.setter
    def organism(self, organism):
        self._organism = organism


    @property
    def expression_system(self):
        """The Pdb's expression organism.

        :rtype: ``str``"""

        return self._expression_system


    @expression_system.setter
    def expression_system(self, expression_system):
        self._expression_system = expression_system


    @property
    def technique(self):
        """The Pdb's experimental technique.

        :rtype: ``str``"""

        return self._technique


    @technique.setter
    def technique(self, technique):
        self._technique = technique


    @property
    def classification(self):
        """The Pdb's classification.

        :rtype: ``str``"""

        return self._classification


    @classification.setter
    def classification(self, classification):
        self._classification = classification


    @property
    def keywords(self):
        """The Pdb's keywords.

        :rtype: ``list``"""

        return self._keywords


    def to_file_string(self):
        """Returns the file text that represents this Pdb.

        :rtype: ``str``"""

        from ..files.pdb2pdbdict import pdb_to_pdb_dict
        from ..files.pdbdict2pdbstring import pdb_dict_to_pdb_string
        pdb_dict = pdb_to_pdb_dict(self)
        return pdb_dict_to_pdb_string(pdb_dict)


    def save(self, path):
        """Saves the Pdb as a .pdb file.

        :param str path: The path to save to."""

        from ..files.utilities import string_to_file
        string_to_file(self.to_file_string(), path)
