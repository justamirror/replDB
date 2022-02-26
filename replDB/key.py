def encode(k):
    return k.replace('\\', '\\\\').replace("$TYPE", "$\TYPE").replace('$', '\$')
def decode(k):
    return k.replace('\$', '$').replace('\\\\', '\\').replace("$\TYPE", "$TYPE")