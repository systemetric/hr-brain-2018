import base64

data = '''YWNjb3JkaW5nIHRvIGFsbCBrbm93biBsYXdzIG9mIGF2aWF0aW9uLAp0aGVyZSBpcyBubyB3YXkg
YSBiZWUgc2hvdWxkIGJlIGFibGUgdG8gZmx5LgppdHMgd2luZ3MgYXJlIHRvbyBzbWFsbCB0byBn
ZXQgaXRzIGZhdCBsaXR0bGUgYm9keSBvZmYgdGhlIGdyb3VuZC4KVGhlIGJlZSwgb2YgY291cnNl
LCBmbGllcyBhbnl3YXkKYmVjYXVzZSBiZWVzIGRvIG5vdCBjYXJlIHdoYXQgcGVvcGxlIHRoaW5r
Lg=='''

with open("new-update.zip", "w") as f:
	f.write(base64.decodestring(data))
