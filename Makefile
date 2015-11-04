protoDir = beam_interactive/proto

protoc:
	@protoc -I=$(protoDir) --python_out=$(protoDir) $(protoDir)/tetris.proto

test: protoc
	@python -m unittest tests/test*.py
