from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
# read the public key in:
public_key = RSA.importKey(open('public-key.pem', 'r').read())
n = public_key.n
e = public_key.e

# Throw into factordb.com and factor n, got p, q
p = 1634733645809253848443133883865090859841783670033092312181110852389333100104508151212118167511579
q = 1900871281664822113126851573935413975471896789968515493666638539088027103802104498957191261465571

assert(p*q == n)

phi = (p-1) * (q-1)
d = inverse(e, phi)

c = int.from_bytes(open('flag.txt', 'rb').read(), 'big')
m = pow(c, d, n)
# print(bytes.fromhex( hex(m)[5:] ))
print(m.to_bytes(90, 'big'))
