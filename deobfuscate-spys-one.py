import re

def deobfuscate(cypher_string, key1, key2):
    def algorithm(p, r, o, x):
        # helper: convert integer c to base-r token string exactly like the JS version
        def y(c):
            c = int(c)
            if c < r:
                prefix = ''
            else:
                prefix = y(c // r)
            digit = c % r
            if digit > 35:
                # JS used String.fromCharCode(c + 29)
                return prefix + chr(digit + 29)
            else:
                # JS used c.toString(36) -> base36 lowercase
                if digit < 10:
                    return prefix + str(digit)
                else:
                    return prefix + chr(ord('a') + (digit - 10))
        # s will hold any remapping if the special branch ever ran (it won't for this input)
        s = {}

        # The original JS contains a branch `if (!''.replace(/^/, String)) { ... }`
        # which is false in modern JS engines for an empty-string.replace with String,
        # so we skip implementing that branch and go straight to the replacement loop.

        # Run replacements: for o-1 down to 0
        for i in range(o - 1, -1, -1):
            if i < len(x) and x[i]:
                token = y(i)
                # replace whole-word occurrences of token with x[i]
                # escape token for regex safety
                p = re.sub(r'\b' + re.escape(token) + r'\b', x[i], p)
        return p

    p = (key1) #q=D^C;t=6;m=B^E;j=0;...
    r = 60
    o = 60
    x = key2.split('^') #^^^^^^^^^^Five3Six^Seven^One^ThreeSevenEight^Six^FiveFourNine^Two3Three...

    output = algorithm(p, r, o, x)
    exec(output)
    return exec(cypher_string)