# beam-interactive-python [![Build Status](https://travis-ci.org/WatchBeam/beam-interactive-python.svg)](https://travis-ci.org/WatchBeam/beam-interactive-python)


This is a base implementation of a Beam Interactive robot. Documentation for the protocol and Tetrisd in general can be found at the [Beam Interactive Documentation](http://watchbeam.github.io/beam-interactive-node/).

```python
import asyncio
import start from beam_interactive
import beam_interactive.proto


def on_error(e):
    print('Oh no, there was an error!')
    print(e)


def on_report(report, conn):
    print('We got a report:')
    print(report)

    # Let's send some silly progress update! See:
    # https://developers.google.com/protocol-buffers/docs/pythontutorial
    # for working with protocol buffers in Python
    report = proto.ProgressUpdate()
    prog = report.progress.add()
    prog.target = proto.ProgressUpdate.TargetType.TACTILE
    prog.code = 42
    prog.progress = 0.3241

    conn.send(report)


loop = asyncio.get_event_loop()


@asyncio.coroutine
def connect():
    conn = yield from start('127.0.0.1:3442', 42, 'asdf', loop)
    handlers = {
        proto.id.error: on_error,
        proto.id.report: on_report
    }

    while (yield from conn.wait_message()):
        decoded, bytes = conn.get_packet()
        id = proto.id.get_packet_id(decoded)

        if decoded is None:
            print('We got a bunch of unknown bytes')
            print(bytes)
        elif id in handlers:
            handlers[id](packet)
        else:
            print("we got packet %d but didn't handle it!" % id)

    conn.close()

loop.run_until_complete(connect())

try:
    loop.run_forever()
finally:
    loop.close()

```
