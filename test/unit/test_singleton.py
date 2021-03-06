from mrt.utils.singleton import Singleton


class FooSingleton(metaclass=Singleton):
    """
    Simple test class for Singleton
    """
    def __init__(self, val):
        self.val = val


class TestSingleton:

    def test_singleton(self):
        """
        Test the behavior of a constructor of a Singleton
        """
        f1 = FooSingleton(4)
        assert f1.val == 4

        f2 = FooSingleton(5)
        assert f2.val == 4

        assert f1.val == 4
        assert id(f1) == id(f2)

        f1.val = 6
        assert f2.val == 6
