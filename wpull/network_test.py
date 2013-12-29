import tornado.testing

from wpull.errors import DNSNotFound
from wpull.network import Resolver
import wpull.util


class MockFaultyResolver(Resolver):
    @tornado.gen.coroutine
    def _resolve_tornado(self, host, port, family):
        yield wpull.util.sleep(5)
        yield Resolver._resolve_tornado(self, host, port, family)


class TestNetwork(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_resolver(self):
        resolver = Resolver()
        address = yield resolver.resolve('google.com', 80)
        self.assertTrue(address)

    @tornado.testing.gen_test
    def test_resolver_timeout(self):
        resolver = MockFaultyResolver(timeout=0.1)
        try:
            address = yield resolver.resolve('test.invalid', 80)
        except DNSNotFound:
            pass
        else:
            self.assertFalse(address)
            self.assertTrue(False)