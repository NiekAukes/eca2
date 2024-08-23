import unittest
from neca.events import Manager, Context, Ruleset, event, condition, create_context

class TestEventsBasic(unittest.TestCase):
    def setUp(self) -> None:
        Manager.global_ruleset = Ruleset()
        Manager.global_context = create_context(ruleset=Manager.global_ruleset)
        return super().setUp()

    def test_init_event(self):
        @event('init')
        def init_event():
            pass

        @event('init')
        def init_event2(ctx):
            pass

        # test that the event is registered
        f = Manager.global_context.ruleset.functions

        self.assertIn(init_event, f)
        self.assertIn(init_event2, f)

        self.assertIn("init", f[init_event].keys)
        self.assertIn("init", f[init_event2].keys)

    def test_event(self):
        @event('test')
        @event('test2')
        def test_event():
            pass

        # test that the event is registered
        f = Manager.global_context.ruleset.functions

        self.assertIn(test_event, f)
        self.assertIn("test", f[test_event].keys)
        self.assertIn("test2", f[test_event].keys)

        # test that the event can be fired
        Manager.global_context.fire('test')

    def test_event_with_args(self):
        @event('test')
        def test_event(ctx, data):
            self.assertEqual(data, "test123")

        @event('test2')
        def test_event2(ctx, data1, data2, data3):
            self.assertEqual(data1, "test")
            self.assertEqual(data2, "123")
            self.assertEqual(data3, "456")

        @event('test3')
        def optional_args(ctx, data1, data2=None):
            self.assertEqual(data1, "test")
            self.assertEqual(data2, None)

        # fire the events
        Manager.global_context.fire('test', "test123")
        Manager.global_context.fire('test2', "test", "123", "456")
        Manager.global_context.fire('test3', "test")
        Manager.global_context.fire('test3', "test", None)
        Manager.global_context.fire('test3', "test", data2=None)

        # run the event loop
        Manager.eventLoop(True)

    def test_delayed_event(self):
        # get the current time
        import time

        t1 = time.time()

        @event('test')
        def test_event():
            t2 = time.time()
            self.assertGreater(t2-t1, 1)
            
        # fire the event
        Manager.global_context.fire('test', delay=1)
        
        
        # run the event loop
        Manager.eventLoop(True)

    def test_condition_event(self):
        @event("test")
        @condition(lambda ctx, data: data == "test123")
        def test_event(ctx, data):
            self.assertEqual(data, "test123")

        @event("test2")
        @condition(lambda ctx, data1, data2: True)
        def test_event2(ctx, data1, data2):
            pass

        Manager.global_context.fire('test', "test123")
        Manager.global_context.fire('test', "test1234")

        Manager.global_context.fire('test2', "test123", "test1234")

        Manager.eventLoop(True)

    def test_events_with_same_key(self):
        @event('test')
        def test_event(ctx, data):
            self.assertEqual(data, "test123")

        @event('test')
        def test_event2(ctx, data):
            self.assertEqual(data, "test123")

        # test that the event is registered
        f = Manager.global_context.ruleset.functions

        self.assertIn(test_event, f)
        self.assertIn(test_event2, f)

        self.assertIn("test", f[test_event].keys)
        self.assertIn("test", f[test_event2].keys)

        # test that the event can be fired
        Manager.global_context.fire('test', "test123")

        # run the event loop
        Manager.eventLoop(True)

        
class TestEventsWrong(unittest.TestCase):
    """
    Test wrong uses of the event decorator
    and fire function.
    """

    def setUp(self) -> None:
        Manager.global_ruleset = Ruleset()
        Manager.global_context = create_context(ruleset=Manager.global_ruleset)
        return super().setUp()
    
    def test_event_with_no_args(self):
        """
        Test that an event with no arguments
        cannot be fired with arguments.
        """
        @event('test')
        def test_event():
            pass
        
        with self.assertRaises(ValueError):
            # this fire should fail
            Manager.global_context.fire('test', 'test123')

    def test_event_with_args(self):
        """
        Test that an event with arguments
        cannot be fired without arguments.
        """
        @event('test')
        def test_event(ctx, data):
            pass
        
        with self.assertRaises(ValueError):
            # this fire should fail
            Manager.global_context.fire('test')

    def test_event_with_wrong_args(self):
        """
        Test that an event with arguments
        cannot be fired with wrong arguments.
        """
        @event('test')
        def test_event(ctx, data):
            pass
        
        with self.assertRaises(ValueError):
            # this fire should fail
            Manager.global_context.fire('test', data1='test123')

    def test_event_with_args_too_many_args(self):
        """
        Test that an event with arguments
        cannot be fired with too many arguments.
        """
        @event('test')
        def test_event(ctx, data):
            pass
        
        with self.assertRaises(ValueError):
            # this fire should fail
            Manager.global_context.fire('test', 'test123', 'test123')

    def test_event_with_args_too_few_args(self):
        """
        Test that an event with arguments
        cannot be fired with too few arguments.
        """
        @event('test')
        def test_event(ctx, data1, data2):
            pass
        
        with self.assertRaises(ValueError):
            # this fire should fail
            Manager.global_context.fire('test', 'test123')

    def test_event_with_incompatible_condition(self):
        """
        Test that an event with incompatible condition
        cannot be fired.
        """
        
        with self.assertRaises(ValueError):
            @event('test')
            @condition(lambda ctx: False)
            def test_event(ctx, data):
                pass

        with self.assertRaises(ValueError):
            @event('test2')
            @condition(lambda ctx, data: False)
            def test_event2():
                pass
    
    def test_events_with_same_key_different_signature(self):
        """
        Test that events with the same key but different signatures
        cannot be defined.
        """
        @event('test')
        def test_event(ctx, data):
            pass
        
        with self.assertRaises(ValueError):
            @event('test')
            def test_event2(ctx, data1, data2):
                pass
