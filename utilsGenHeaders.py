import base64

message = "ycarro9@gmail.com:db26135789f64e9f64eb"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)
