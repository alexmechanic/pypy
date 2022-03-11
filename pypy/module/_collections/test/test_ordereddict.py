
class AppTestBasic:
    spaceconfig = dict(usemodules=['_collections'])

    def test_ordereddict_present(self):
        from _collections import OrderedDict
        assert issubclass(OrderedDict, dict)
        assert hasattr(OrderedDict, 'move_to_end')

    def test_recursive_repr(self):
        from _collections import OrderedDict
        d = OrderedDict()
        d[1] = d
        assert repr(d) == 'OrderedDict([(1, ...)])'

    def test_subclass(self):
        from _collections import OrderedDict
        class MyODict(OrderedDict):
            def __setitem__(self, key, value):
                super().__setitem__(key, 42)
        d = MyODict(x=1)
        assert d['x'] == 42
        d.update({'y': 2})
        assert d['y'] == 42

    def test_reversed(self):
        import sys
        from _collections import OrderedDict

        pairs = [('c', 1), ('b', 2), ('a', 3), ('d', 4), ('e', 5), ('f', 6)]
        od = OrderedDict(pairs)
        if '__pypy__' in sys.builtin_module_names:
            # dict ordering is wrong when testing interpreted on top of CPython
            pairs = list(dict(od).items())
        assert list(reversed(od)) == [t[0] for t in reversed(pairs)]
        assert list(reversed(od.keys())) == [t[0] for t in reversed(pairs)]
        assert list(reversed(od.values())) == [t[1] for t in reversed(pairs)]
        assert list(reversed(od.items())) == list(reversed(pairs))

    def test_call_key_first(self):
        from _collections import OrderedDict

        calls = []
        class Spam:
            def keys(self):
                calls.append('keys')
                return ()
            def items(self):
                calls.append('items')
                return ()

        OrderedDict(Spam())
        assert calls == ['keys']

    def test_generic_alias(self):
        import _collections
        ga = _collections.OrderedDict[int]
        assert ga.__origin__ is _collections.OrderedDict
        assert ga.__args__ == (int, )

    def test_or(self):
        from _collections import OrderedDict
        d1 = OrderedDict({1: 2, 3: 4})
        d2 = OrderedDict({1: 4, 5: 6})
        assert type(d1 | d2) is OrderedDict
        assert d1 | d2 == {1: 4, 3: 4, 5: 6}
        assert type(dict(d1) | d2) is OrderedDict
        assert d1 | d2 == {1: 4, 3: 4, 5: 6}

    def test_ior(self):
        from _collections import OrderedDict
        orig = d = OrderedDict({'spam': 1, 'eggs': 2, 'cheese': 3})
        e = {'cheese': 'cheddar', 'aardvark': 'Ethel'}
        d |= e
        assert orig == {'spam': 1, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}

