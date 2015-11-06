protoDir = beam_interactive/proto

protoc:
	@protoc -I=$(protoDir) --python_out=$(protoDir) $(protoDir)/tetris.proto

test:
	@python -m unittest tests/test*.py

pep8:
	@pep8 beam_interactive --exclude=tetris_pb2.py,varint.py
