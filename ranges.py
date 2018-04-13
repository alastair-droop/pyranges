#!/usr/bin/env python3

def prettyRange(x, start=1, end=None, emptyChar="-", filledChar="█", appendDesc=True):
    """
    Return a pretty representation of a range.
    The range is shown as a run of filledChar characters on a background line of emptyChar characters.
    The length of the background line is determined by start and end.
    """
    if x.empty is True:
        if end is None: raiseValueError("end must be specified for empty ranges")
        output_str = emptyChar * (end - start + 1)
    else:
        if end is None: end = x.span.end
        if start > x.span.start: raise ValueError("start is after range start")
        if end < x.span.end: raise ValueError("end is before range end")
        values = [emptyChar for i in range(0, end)]
        for r in x.ranges:
            for i in r:
                values[i - 1] = filledChar
        output_str = "".join(values)
    if appendDesc is True: output_str = "{} : {}".format(output_str, str(x))
    return output_str

class ARange(object):
    """
    The ARange class represents a consecutive range of positive integers defined by a start and end value.
    Both start and end value are included in the range, so ARange(5, 15) represents the integers 5--15 inclusive.
    Empty ARanges are represented as ranges where both start and end are None.
    """
    def __init__(self, start=None, end=None):
        """Initialize an ARange object from the given start and end values. If start is None, then an empty ARange is returned."""
        super().__init__()
        self.setRange(start, end)
        
    def setRange(self, start=None, end=None):
        """Set the start and end of an ARanges object."""
        if (end is None): end = start
        if (start is None):
            self._start = None
            self._end = None        
        else:
            values = sorted([int(start), int(end)])
            if values[0] <= 0: raise ValueError('ARange values must be positive')
            self._start = values[0]
            self._end = values[1]  
        
    def setStart(self, start):
        """Set the start of an ARanges object."""
        self.setRange(start, self.end)
        
    def setEnd(self, end):
        """Set the end of an ARanges object."""
        self.setRange(self.start, end)
        
    def getStart(self):
        """Return the start of an ARanges object."""
        return self._start
        
    def getEnd(self):
        """Return the end of an ARanges object."""
        return self._end
        
    def isEmpty(self):
        """Test if the ARanges object is empty."""
        return(self.start is None)
        
    def getRanges(self):
        """Return the atomic ranges covered by this object as a list."""
        return [self.span]
        
    def getSpan(self):
        """Return the total span of the object (i.e. the lowest value to the highest value it contains)."""
        return self.copy()
        
    def copy(self):
        """Return a copy of the ARange object."""
        return ARange(start=self.start, end=self.end)
        
    def asList(self):
        """Return the integers contained in the ARanges object as a list."""
        if self.empty is True: return []
        return list(range(self.start, self.end + 1))
    
    def asSet(self):
        """Return the integers contained in the ARanges object as a set."""
        return set(self.asList())

    def translate(self, n):
        """
        Return a new ARanges object translated by n.
        A positive value of n will shift the whole range to the right, whilst a negative value will shift to the left.
        """
        if self.empty: return ARange()
        return ARange(self.start + n, self.end + n)
        
    def expand(self, start, end=None):
        """Expand an ARanges object, optionally by differeng amounts left and right."""
        if (end is None): end = start
        assert isinstance(start, int)
        new_start = self.start - start
        new_end = self.end + end
        if new_end < new_start: return ARange()
        return ARange(new_start, new_end)
        
    def split(self, n):
        """
        Split an ARange into a two at a given position, returning a tuple of two ARanges (possibly empty).
        The given value is included in the second ARange.
        """
        if self.empty is True: return (ARange(), ARange())
        n = int(n)
        if n <= self.start: return (ARange(), self.copy())
        if n > self.end: return (self.copy(), ARange())
        return (ARange(self.start, n - 1), ARange(n, self.end))
        
    def removeAtomic(self, other):
        """Remove an ARange from another, shifting the right-hand overlaps left."""
        assert isinstance(other, ARange)
        left = self.leftOverhang(other)
        right = self.rightOverhang(other)
        return left | right.translate(-len(other))
        
    def insertAtomic(self, other):
        """Insert an ARange into another."""
        assert isinstance(other, ARange)
        left, right = self.split(other.start)
        return left | other | right.translate(len(other))
        
    def __eq__(self, other):
        """Test two ranges for equality."""
        return (isinstance(other, ARange)) and (self.start == other.start) and (self.end == other.end)
        
    def __ne__(self, other):
        """Test two ranges for inequality."""
        return not self.__eq__(other)

    def __le__(self, other):
        """Test if self is a subset of other."""
        if self.empty is True: return True
        if isinstance(other, ARange):
            if other.empty is True: return False
            if (self.start < other.start) or (self.end > other.end): return False
            return True
        return NotImplemented
    
    def __lt__(self, other):
        """Test if self is a proper subset of other."""
        return (self <= other) and (self != other)

    def __ge__(self, other):
        """Test if other is a subset of self."""
        if isinstance(other, ARange):
            if other.empty is True: return True
            if self.empty is True: return False
            if (other.start < self.start) or (other.end > self.end): return False
            return True
        return NotImplemented
    
    def __gt__(self, other):
        """Test if self is a proper superset of other."""
        return (self >= other) and (self != other)
    
    def __and__(self, other):
        """Return the intersection of two ARanges."""
        if (self.empty is True) or (other.empty is True): return ARange()
        elif isinstance(other, ARange):
            if self.distance(other) >= 0: return ARange()
            return ARange(max(self.start, other.start), min(self.end, other.end))
        return NotImplemented
        
    def __or__(self, other):
        """Return the union of two ARanges."""
        if self.empty is True: return other.copy()
        if other.empty is True: return self.copy()
        elif isinstance(other, ARange):
            if self.distance(other) > 0: return SRange([self, other])
            return ARange(min(self.start, other.start), max(self.end, other.end))
        return NotImplemented
        
    def __sub__(self, other):
        """Return the difference between two ARanges."""
        if self.empty is True: return ARange()
        if isinstance(other, ARange):
            if other.empty is True: return self.copy()
            if self.distance(other) > 0: return self.copy()
            elif (self.start >= other.start) and (self.end <= other.end): return ARange() # self is entirely within the other
            elif (self.start <= other.start) and (self.end <= other.end): return ARange(self.start, other.start - 1) # Self overhangs the left only
            elif (self.start >= other.start) and (self.end > other.end): return ARange(other.end + 1, self.end) # Self overhangs the right only
            else: return SRange([ARange(self.start, other.start - 1), ARange(other.end + 1, self.end)]) #OK, so it overhangs both ends
        return NotImplemented
        
    def __xor__(self, other):
        """Return the exclusive disjunction between two ARanges."""
        return (self | other) - (self & other)
        
    def distance(self, other):
        """
        Return the minimum distance between to ARanges.
        For overlapping ARanges, this returns -1.
        """
        if self.empty or other.empty: return None
        if (self.end < other.start): return other.start - self.end - 1
        if (self.start > other.end): return self.start - other.end - 1
        return -1
        
    def overlaps(self, other):
        """Test if two ARanges overlap."""
        return not (self & other).empty
        
    def leftOverhang(self, other):
        """Return the values from self that are less than the start of other."""
        assert isinstance(other, ARange)
        if other.start <= self.start: return ARange()
        return self & ARange(self.start, other.start - 1)
        
    def rightOverhang(self, other):
        """Return the values from self that are greater than the end of other."""
        assert isinstance(other, ARange)
        if other.end >= self.end: return ARange()
        return self & ARange(other.end + 1, self.end)
        
    def __iter__(self):
        """Iterate over the values contained in an ARange."""
        self._current_i = self.start
        return self
        
    def __next__(self):
        """Return the next value in an ARange."""
        if self.empty is True: raise StopIteration
        self._current_i += 1
        if self._current_i - 1 > self.end: raise StopIteration
        return self._current_i - 1
        
    def __bool__(self):
        """Test if an ARange is not empty."""
        return not self.empty
        
    def __len__(self):
        """Return the length of an ARange (i.e. the number of values it contains)."""
        if self.empty: return 0
        return (self.end - self.start) + 1
        
    def __str__(self):
        """Return a string representation of an ARange."""
        if self.empty is True: return '-'
        if len(self) == 1: return str(self.start)
        return '{}-{}'.format(self.start, self.end)
        
    def __repr__(self):
        """Show the code that would regenerate the ARange."""
        if self.empty is True: return 'ARange()'
        if len(self) == 1: return('ARange({})'.format(self.start))
        return 'ARange({}, {})'.format(self.start, self.end)
        
    start = property(getStart, setStart, doc='The first value in the ARange.')
    end = property(getEnd, setEnd, doc='The last value in the ARange.')
    empty = property(isEmpty, None, doc='Is the ARange empty?')
    span = property(getSpan, None, doc='The span of the ARange.')
    ranges = property(getRanges, None, doc='The ranges of the ARange as a list.')

class SRange(object):
    """
    The SRange class represents a set of possible non-consecutive positive integer values.
    SRanges are defined as a set of consecutive ranges (i.e. ARange objects).
    Empty SRange objects are represented as an empty set of ARange objects.
    """
    @classmethod
    def fromSet(cls, l):
        """Initialize an SRange object from the values contained in the given set."""
        output = SRange()
        for i in l: output |= ARange(i)
        return output
        
    def __init__(self, ranges=[]):
        """Initialize an SRange object from the given list of ARange objects. If the ranges list is empty, then an empty SRange is returned."""
        super().__init__()
        self.ranges = ranges
        
    def setRanges(self, ranges):
        """Set the list of ARange objects contained in the SRange object."""
        self._ranges = []
        for new in ranges:
            assert isinstance(new, ARange)
            self._ranges.append(new.copy())
        self.consolidate()
        
    def addRange(self, new):
        """Add a single ARange object to the list of ranges."""
        if isinstance(new, ARange) or isinstance(new, SRange):
            for r in new.ranges:
                if (r.empty is True) or (new in self.ranges): continue
                self._ranges.append(r.copy())
            self.consolidate()
        else: raise NotImplementedError
        
    def sort(self):
        """Sort the list of atomic ranges by their start positions."""
        self._ranges = sorted(self._ranges, key=lambda x: x.start)
        
    def consolidate(self):
        """Consolidate the list of atomic ranges by merging those that overlap."""
        self.sort()
        i = 0
        while True:
            if i >= (len(self._ranges) - 1): break
            j = i + 1
            if self._ranges[i].distance(self._ranges[j]) < 1:
                self._ranges[i] = self._ranges[i] | self._ranges[j]
                self._ranges.pop(j)
            else: i += 1
        
    def isEmpty(self):
        """Test if the SRange object is empty."""
        return len(self) == 0
        
    def isDisjoint(self):
        """Test if the SRange object is disjoint (i.e. can not be described as a single atomic range)."""
        return len(self._ranges) > 1
        
    def getRanges(self):
        """Return the ARange objects contained in the SRange as a list."""
        return self._ranges
        
    def getSpan(self):
        """Return the span of the SRange object."""
        if self.empty: return ARange()
        return ARange(min(r.start for r in self), max(r.end for r in self))
        
    def copy(self):
        """Return a copy of the object."""
        return SRange(self.ranges)
        
    def asList(self):
        """Return all integer values covered by the SRange object as a list."""
        output = []
        for r in self: output.extend(r.asList())
        return output
    
    def asSet(self):
        """Return all integer values covered by the SRange object as a set."""
        return set(self.asList())
        
    def translate(self, n):
        """
        Return a new SRange object translated by n.
        A positive value of n will shift the whole range to the right, whilst a negative value will shift to the left.
        """
        output = SRange()
        for r in self.ranges:
            output.addRange(r.translate(n))
        return output
        
    def expand(self, start, end=None):
        """Expand an SRanges object, optionally by differeng amounts left and right."""
        if (end is None): end = start
        assert isinstance(start, int)
        output = self.copy()
        if start > 0: output = output | ARange(self.span.start, self.span.start - start)
        elif start < 0: output = output - ARange(self.span.start, self.span.start - start - 1)
        if end > 0: output = output | ARange(self.span.end, self.span.end + end)
        elif end < 0: output = output - ARange(self.span.end + end + 1, self.span.end)
        return output
        
    def split(self, n):
        """Split an SRange into a two at a given position, returning a tuple of two SRanges (possibly empty).
        The given value is included in the second SRange."""
        n = int(n)
        left = SRange()
        right = SRange()
        for r in self._ranges:
            r_split = r.split(n)
            left = left | r_split[0]
            right = right | r_split[1]
        return (left, right)
        
    def removeAtomic(self, other):
        """Remove an ARange from the self, shifting the right-hand overlap left."""
        assert(isinstance(other, ARange))
        left = self.leftOverhang(other)
        right = self.rightOverhang(other)
        return left | right.translate(-len(other))
        
    def remove(self, other):
        """Remove an (S|A)Range from self, shifting the right-hand overlaps left."""
        if other.empty is True: return self.copy()
        elif isinstance(other, ARange): return self.removeAtomic(other)
        elif isinstance(other, SRange):
            output = self.copy()
            for i in reversed(other.ranges): output = output.removeAtomic(i)
            return output
        else: raise NotImplementedError()
        
    def insertAtomic(self, other):
        """Insert an ARange into self, shifting the right-hand overlaps right."""
        assert(isinstance(other, ARange))
        left, right = self.split(other.start)
        return left | other | right.translate(len(other))
        
    def insert(self, other):
        """Insert an (S|A)Range into self, shifting the right-hand overlaps right."""
        if other.empty is True: return self.copy()
        elif isinstance(other, ARange): return self.insertAtomic(other)
        elif isinstance(other, SRange):
            output = self.copy()
            for i in reversed(other.ranges): output = output.insertAtomic(i)
            return output
        else: raise NotImplementedError()
        
    def __eq__(self, other):
        """Test two ranges for equality."""
        return self.asSet() == other.asSet()
        
    def __ne__(self, other):
        """Test two ranges for inequality."""
        return self.asSet() != other.asSet()
    
    def __le__(self, other):
        """Test if self is a subset of other."""
        return self.asSet() <= other.asSet()
    
    def __lt__(self, other):
        """Test if self is a proper subset of other."""
        return (self <= other) and (self != other)

    def __ge__(self, other):
        """Test if other is a subset of self."""
        return self.asSet() >= other.asSet()
    
    def __gt__(self, other):
        """Test if self is a proper superset of other."""
        return (self >= other) and (self != other)
    
    def __and__(self, other):
        """Return the intersection of self with another (S|A)Range object."""
        if (self.empty is True) or (other.empty is True): return SRange()
        if isinstance(other, ARange) or isinstance(other, SRange):
            return SRange.fromSet(self.asSet() & other.asSet())
        else: return NotImplemented
        
    def __rand__(self, other):
        """Return the intersection of another (S|A)Range object with self."""
        return self.__and__(other)
        
    def __or__(self, other):
        """Return the union of self with another (S|A)Range object."""
        output = self.copy()
        if isinstance(other, ARange) or isinstance(other, SRange): output.addRange(other)
        else: return NotImplemented
        return output
        
    def __ror__(self, other):
        """Return the union of another (S|A)Range object with self."""
        return self.__or__(other)
        
    def __sub__(self, other):
        """Return the difference of self with another (S|A)Range object."""
        if self.empty is True: return SRange()
        if other.empty is True: return self.copy()
        if isinstance(other, ARange) or isinstance(other, SRange): return SRange.fromSet(self.asSet() - other.asSet())
        else: return NotImplemented
        
    def __rsub__(self, other):
        """Return the difference of another (S|A)Range object with self."""
        return self.__sub__(other)
        
    def __xor__(self, other):
        """Return the exclusive disjunction between self and another (S|A)Range."""
        if isinstance(other, SRange) or (isinstance(other, ARange)): return SRange.fromSet(self.asSet() ^ other.asSet())
        return NotImplemented
        
    def __rxor__(self, other):
        """Return the exclusive disjunction between another (S|A)Range and self."""
        if isinstance(other, ARange): return SRange.fromSet(other.asSet() ^ self.asSet())
        return NotImplemented
    
    def distance(self, other):
        """
        Return the minimum distance between two SRanges.
        For overlapping ARanges, this returns -1.
        """
        return self.span.distance(other.span)
    
    def leftOverhang(self, other):
        """Return the values from self that are less than the start of other."""
        assert isinstance(other, ARange) or isinstance(other, SRange)
        if self.empty: return SRange()
        if other.empty: return self.copy()
        if other.span.start <= self.span.start: return SRange()
        return self & ARange(self.span.start, other.span.start - 1)
        
    def rightOverhang(self, other):
        """Return the values from self that are greater than the end of other."""
        assert isinstance(other, ARange) or isinstance(other, SRange)
        if self.empty: return SRange()
        if other.empty: return self.copy()
        if other.span.end >= self.span.end: return SRange()
        return self & ARange(other.span.end + 1, self.span.end)
        
    def __getitem__(self, key):
        """Return a single atomic range by its index."""
        return self._ranges[key]
        
    def __setitem__(self, key, value):
        """Set a single atomic range by its index."""
        assert isinstance(value, ARange)
        self._ranges[key] = value
        self.consolidate()
        
    def __iter__(self):
        """Iterate over the ARange objects contained in the SRange."""
        self._current_i = 0
        return self
        
    def __next__(self):
        """Return the next ARange object contained in the SRange."""
        self._current_i += 1
        if self._current_i - 1 >= len(self._ranges): raise StopIteration
        return self._ranges[self._current_i - 1]
        
    def __bool__(self):
        """Test if an ARange is not empty."""
        return not self.empty
        
    def __len__(self):
        """Return the length of an SRange (i.e. the number of values it contains)."""
        return sum([len(r) for r in self])
        
    def __str__(self):
        """Return a string representation of an SRange."""
        if self.empty: return '-'
        if not self.disjoint: return str(self._ranges[0])
        return '{{{}}}'.format(', '.join([str(i) for i in self._ranges]))
        
    def __repr__(self):
        """Show the code that would regenerate the SRange."""
        if self.empty is True: return 'SRange()'
        output = []
        for i in self.ranges: output.append(repr(i))
        return('SRange([{}])'.format(', '.join(output)))
        
    ranges = property(getRanges, setRanges, doc='The ranges of the SRange as a list.')
    empty = property(isEmpty, None, doc='Is the SRange empty?')
    disjoint = property(isDisjoint, None, doc='Is the SRange disjoint?')
    span = property(getSpan, None, doc='The complete span of the SRange.')
