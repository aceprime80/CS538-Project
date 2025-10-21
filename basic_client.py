import requests
import sys
dst_arg = sys.argv[1]
dst = "http://localhost:8000/upload-image"
if dst_arg != "local":
    dst = dst_arg
path = "test_images/skyline.png"
if len(sys.argv) == 3:
    path = sys.argv[2]
file_type = path.split(".")[1]
file_binary_data = open(path, "rb").read()
response = requests.post(url=dst, headers={"Content-Type":f'image/{file_type}'}, data=file_binary_data)
print("THIS IS RESPONSE.ELAPSED", response.elapsed)
print(response.text)
