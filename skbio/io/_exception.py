from __future__ import absolute_import, division, print_function

# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------


class FileFormatError(Exception):
    """Raised when a file cannot be parsed."""
    pass


class RecordError(FileFormatError):
    """Raised when a record is bad."""
    pass


class FieldError(RecordError):
    """Raised when a field within a record is bad."""
    pass


class UnrecognizedFormatError(FileFormatError):
    """Raised when a file's format is unknown, ambiguous, or unidentifiable."""
    pass


class ClustalFormatError(FileFormatError):
    """Raised when a ``clustal`` formatted file cannot be parsed."""
    pass


class DMFormatError(FileFormatError):
    """Raised when a ``dm`` formatted file cannot be parsed."""
    pass


class FASTAFormatError(FileFormatError):
    """Raised when a ``fasta`` formatted file cannot be parsed."""
    pass


class FASTAQUALFormatError(FileFormatError):
    """Raised when FASTA/QUAL formatted files cannot be parsed."""
    pass


class NewickFormatError(FileFormatError):
    """Raised when a ``newick`` formatted file cannot be parsed."""
    pass


class OrdResFormatError(FileFormatError):
    """Raised when an ``ordres`` formatted file cannot be parsed."""
    pass


class PhylipFormatError(FileFormatError):
    """Raised when a ``phylip`` formatted file cannot be parsed.

    May also be raised when an object (e.g., ``Alignment``) cannot be written
    in ``phylip`` format.

    """
    pass


class QUALFormatError(FileFormatError):
    """Raised when a ``qual`` formatted file cannot be parsed."""
    pass


class InvalidRegistrationError(Exception):
    """Raised if function doesn't meet the expected API of its registration."""
    pass


class DuplicateRegistrationError(Exception):
    """Raised when a function is already registered in skbio.io"""

    def __init__(self, name=None, fmt=None, cls=None, msg=None):
        super(DuplicateRegistrationError, self).__init__()
        if msg:
            self.args = (msg,)
        else:
            if hasattr(cls, '__name__'):
                classname = cls.__name__
            else:
                classname = 'generator'
            self.args = ("'%s' already has a %s for %s."
                         % (fmt, name, classname),)
