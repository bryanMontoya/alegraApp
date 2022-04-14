import base64

message = "bmontoyaosorios@gmail.com:93654ceb0656ef4ee8d6"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)
