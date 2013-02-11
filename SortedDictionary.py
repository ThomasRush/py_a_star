
class SortedDictionary(dict):
    """Dictionary object that allows user-defined sorting on keys or values.

    This data type provides the O(1) membership lookup of
    a dictionary and the O(n log n) sorting capabilities of a list.
    Sacrifices memory to achieve this (creates a list of key/value tuples
    based on the dictionary). Note: changing the value of an existing
    item will take O(n) time, as it must be found/replaced in the sort list.

    Different than Python 2.7's OrderedDict as the user can sort by
    key, value, or some property or function of either.

    This is done throught the user-supplied sort_function parameter. For
    examples of sort functions, see the constructor below.

    """
    def __init__(self,dictionary=None,sort_function=None, reverse=False,*args, **kw):
        """Create a SortedDictionary

        Keyword arguments:
        dictionary - supplied dictionary (optional)
        sort_function - supplied sort function (optional; default is key sort)
        reverse - boolean; sort in reverse? (optional)

        Sort Function Examples:

        1. The following function would sort by the key (don't actually do
           this, as the default is to sort on the key)

            def sort_function(item):
                return item[0] #<-- index of zero indicates key sorting

        2. The following function would sort by the value

            def sort_function(item):
                return item[1] #<-- index of one indicates value sorting

        3. This would sort by the values at index one (1) in the
           dictionary key:

            def sort_function(item):
                return item[0][1] # If the key was tuple (a,b) this sorts on b

        4. This would sort by the result of foo() in the dictionary
            value:

            def_sort_function(item):
                return item[1].foo()

        5. The following function would sort by the sort_val attribute of
            the dictionary key:

            def sort_function(item):
               return item[0].sort_val

        """
        dict.__init__(self)

        # A list of key/value tuples that will be used
        # for sorting
        self._sort_tuples = []
        self.reverse = reverse

        if sort_function == None:
            self._sort_function = self._default_sort_function
        else:
            self._sort_function = sort_function

        if dictionary == None:
            self._dictionary = {}
        else:
            self._dictionary = dictionary
            self._add_items(dictionary)
            self._sort()

    def key_at(self,index):
        """ Returns the sorted dictionary key at the specified index"""
        return self._sort_tuples[index][0]

    def value_at(self,index):
        """ Returns the sorted dictinoary value at the specified index"""
        return self._sort_tuples[index][1]

    def item_at(self,index):
        """ Returns the sorted key/value pair at the specified index"""
        return self._sort_tuples[index]

    def _default_sort_function(self,item):
        """ If sort criteria is not supplied, the key is sorted"""
        return item[0]

    def _sort(self):
        """ In-place sort based on sort function's results"""
        self._sort_tuples.sort(key=self._sort_function,reverse=self.reverse)

    def __setitem__(self, key, value):
        """ Adds item function and automatically re-sorts"""
        self._add_item(key,value)
        self._sort()

    def pop(self):
        """ Remove and return the key/value item for the lowest sorted item
        (Overrides default dict implementation which requires a key)"""
        if len(self) == 0:
            return None
        key,val = self.lowest()
        del(self[key])
        return key, val

    def lowest(self):
        """ Return the lowest sorted key/value pair """
        if len(self) == 0:
            return None
        return self._sort_tuples[0]

    def highest(self):
        """ Return the highest sorted key/value pair """
        if len(self) == 0:
            return None
        s = self._sort_tuples
        return s[len(s)-1]

    def _add_item(self,key,value):
        """ Handles the adding of a new item to the dict and sort list """
        # If a key already exists, update its entry to have the new value
        if self.has_key(key):
            super(SortedDictionary,self).__setitem__(key,value)

            # Find and replace the key/val
            for index,pair in enumerate(self._sort_tuples):
                if pair[0] == key:
                    self._sort_tuples[index] = (key,value)
                    break
        else:
            # Otherwise just add it to the dictionary and sort list
            super(SortedDictionary,self).__setitem__(key,value)
            self._sort_tuples.append((key,value))

    def _add_items(self,items):
        """ Appends dictionary items and re-sorts """
        for key,val in items.iteritems():
            self._add_item(key,val)
        self._sort()

    def clear(self):
        """ Empties the data structure """
        self._dictionary = {}
        self._sort_tuples = []

    def fromkeys(self,seq,Value=None):
        return_dict = {}
        for i in seq:
            return_dict[i] = Value
        return return_dict

    def __delitem__(self, key):
        """ Deletes an item from the dictionary/list data structure"""
        super(SortedDictionary,self).__delitem__(key)

        # No need to re-sort on deletes
        for index,pair in enumerate(self._sort_tuples):
            if pair[0] == key:
                del(self._sort_tuples[index])
                return

    def __str__(self):
        """ Return object description """

        # TODO: feel free to override this and __repr__.
        # It was used primarily for testing
        string = "{:15s}{:15s}{:15s}\n".format("Key","Value","Sorted-on value")
        string += "-" * 60 + "\n"
        for item in self._sort_tuples:
            string += "{:15s}{:15s}{:15s} \n".format(str(item[0]),str(item[1]),str(self._sort_function(item)))
        return string + ""

    def __repr__(self):
        return str(self.items())

    def update(self,*args,**kw):
        """ For appending dictionary items """
        if len(args) > 0:
            self._add_items(args[0])

        if len(kw) > 0:
            self._add_items(kw[0])

        self._sort()

