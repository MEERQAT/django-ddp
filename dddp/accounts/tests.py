"""Django DDP Accounts test suite."""
from __future__ import unicode_literals

import sys
from dddp import tests


class AccountsTestCase(tests.DDPServerTestCase):

    # gevent-websocket doesn't work with Python 3 yet
    @tests.expected_failure_if(sys.version_info.major == 3)
    def test_login_no_accounts(self):
        sockjs = self.server.sockjs('/sockjs/1/a/websocket')

        resp = sockjs.websocket.recv()
        self.assertEqual(resp, 'o')

        msgs = sockjs.recv()
        self.assertEqual(
            msgs, [
                {'server_id': '0'},
            ],
        )

        sockjs.connect('1', 'pre2', 'pre1')
        msgs = sockjs.recv()
        self.assertEqual(
            msgs, [
                {'msg': 'connected', 'session': msgs[0].get('session', None)},
            ],
        )

        id_ = sockjs.call(
            'login', {'user': 'invalid@example.com', 'password': 'foo'},
        )
        msgs = sockjs.recv()
        self.assertEqual(
            msgs, [
                {
                    'msg': 'result',
                    'error': {
                        'error': 500,
                        'reason': "(403, 'Authentication failed.')",
                    },
                    'id': id_,
                },
            ],
        )

        sockjs.close()
