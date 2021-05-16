#!/usr/bin/env python3
import base64

with open("./payload.zip", "rb") as f:
    b64 = base64.urlsafe_b64encode(f.read())
    print(b64.decode())
