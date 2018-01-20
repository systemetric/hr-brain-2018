import base64

with open("test.txt", "rb") as f:
    with open("data-small.txt", "w") as d:
        # d.write(str(list(f.read())))
        d.write(base64.encodestring(f.read()))
