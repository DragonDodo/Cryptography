# come on, colin, crack the bloody cipher already
# agreed. 
from random import shuffle, random, choice
from math import exp, log
KEY1 = KEY2 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

T = 1.0 #yes, I know, global variables are dangerous. 

def unpf( ct, key ):
    out = ""
    while ct:
        a = ct[0]
        b = ct[1]
        ct = ct[2:]
        ax,ay = (key.find(a) // 5, key.find(a) % 5)
        bx,by = (key.find(b) // 5, key.find(b) % 5)
        
        if ax == bx:
            Ax = Bx = ax
            Ay = (ay + 4) % 5
            By = (by + 4) % 5
        elif ay == by:
            Ay = By = ay
            Ax = (ax + 4) % 5
            Bx = (bx + 4) % 5
        else:
            Ax = bx
            Bx = ax
            Ay = ay
            By = by
        an = 5*Ax + Ay
        bn = 5*Bx + By
        if an==bn:
            for i in range(5):
                print key[i*5:i*5+5]
            print ct
            print a, b 
            print "a xy: ", ax, ay
            print "b xy: ", bx, by
            print "A xy: ", Ax, Ay
            print "B xy: ", Bx, By
            
            raise RuntimeError
        out += key[bn] + key[an]
        
    return out
    
def decrypt( ct, KEY1, KEY2 ):
    #print ct, KEY1, KEY2
    cipherText = ct.replace(" ", "")
    n = len(cipherText)
    ct1 = "".join( [cipherText[i] for i in range(n) if i % 4 < 2] )
    ct2 = "".join( [cipherText[i] for i in range(n) if i % 4 >= 2] )

    pt1 = unpf(ct1, KEY1 )
    pt2 = unpf(ct2, KEY2 )

    out = "".join([ pt1[2*(i // 4) + i % 2] if i % 4 < 2 else pt2[2*(i // 4) + i % 2] for i in range(n)])
    
    return out

def handleQuads(fn):
    from math import log
    quads = {}
    f = open(fn, 'r')
    for l in f.readlines():
        q, n = l.split(" ")
        quads[q] = log(float(n))
    return quads
    
def score(decrypt, quads, cribs = None):
    out = 0.
    for i in range(len(decrypt)-2):
        try:
            out += quads[ decrypt[i:i+2] ]
        except KeyError:
            pass
        if cribs is not None:
            for c in cribs:
                l = len(c)
                if i+l < len(decrypt):
                    if decrypt[i:i+l] == c:
                        out += 10 * l
    return out
    
def strShuffle(s):
    ind = range(25)
    shuffle(ind)
    return "".join([s[i] for i in ind])

def swapPair(s, i=None, j=None):
    if i is None:
        i = j = int( random() * 25 )
        while i == j:
            j = int (random() * 25)
    i,j = (i, j) if i < j else (j, i)
    out = s[:i] + s[j] + s[i+1:j] + s[i] + s[j+1:]
    if len(out) != len(s):
        print s, i, j
        raise RunTimeError
    return out
    
def swapCols(s, i, j):
    for k in range(5):
        s = swapPair(s, 5*k + i, 5*k+j)
    return s

def swapRows(s, i, j):
    for k in range(5):
        s = swapPair(s, 5*i + k, 5*j+k)
    return s
    
        
def testKeys(ciphers, k1, k2, quads, best, cribs):
    
    nc = len ( ciphers )
    ds = map(decrypt, ciphers, [k1 for i in range(nc)], [k2 for i in range(nc)])
    ss = sum(map(score, ds, [quads for i in range(nc)], [cribs for i in range(nc)]))
    ap = exp((best[0] - ss)/1000*T)
    if ap > random:
        best = (ss, ds, (k1, k2))
    return best
    
def climb(k1, k2, ciphers, quads, cribs = None):
    nc = len(ciphers)
    chooserlist = ['pair', 'cols', 'rows'] #random string chosen from this list to determine what swap
    global T
    T = 0.8*T
    
    ds = map(decrypt, ciphers, [k1 for i in range(nc)], [k2 for i in range(nc)])
    ss = sum(map(score, ds, [quads for i in range(nc)], [cribs for i in range(nc)]))
    best = (ss, ds, (k1, k2))
    
    action = choice(chooserlist)
    print action
    
    for ii in range(len(k1)):
        for jj in range(ii+1, len(k1)-1):
            if ii < 5 and jj < 5:
                if action == 'pair':
                    sk1 = swapPair(k1,ii,jj)
                if action == 'cols':
                    sk1 = swapCols(k1,ii,jj)
                elif action == 'rows':
                    sk1 = swapRows(k1,ii,jj)
                #redo this mess of loops later    
            
            best = testKeys(ciphers, sk1, k2, quads, best, cribs)
           # if ii < 5 and jj < 5:
               # sc1 = swapCols(k1,ii,jj)
                #sr1 = swapRows(k1,ii,jj)
               # sc2 = swapCols(k2,ii,jj)
                #sr2 = swapRows(k2,ii,jj)
                
            
                
               # best = testKeys(ciphers, sc1, k2, quads, best, cribs)                
                #best = testKeys(ciphers, k1, sc2, quads, best, cribs)            
               # best = testKeys(ciphers, sr1, k2, quads, best, cribs)                
                #best = testKeys(ciphers, k1, sr2, quads, best, cribs)   
                
            
                #print T
                
# #             for kk in range(len(k2)):
# #                 for ll in range(kk+1,len(k2)-1):
# #                     sk2 = swapPair(k2,kk,ll)
# #                     if kk == 0 and ll == 1:
# #                         best = testKeys(ciphers, k1, sk2, quads, best, cribs)
# #                             
# # 
# #                     if ii< 5 and jj < 5 and kk < 5 and ll < 5:
# #                         sc2 = swapCols(k2,kk,ll)
# #                         sr2 = swapRows(k2,kk,ll)
# 
# 
#                     best = testKeys(ciphers, sk1, sk2, quads, best, cribs)
#     
# 
#                     if ii < 5 and jj < 5 and kk < 5 and ll < 5:
#                         best = testKeys(ciphers, sc1, sc2, quads, best, cribs)
#                         best = testKeys(ciphers, sc1, sr2, quads, best, cribs)
#                         best = testKeys(ciphers, sr1, sc2, quads, best, cribs)
#                         best = testKeys(ciphers, sr1, sr2, quads, best, cribs)
    
                
                # try swap rows, cols

                     
    return best
        
def decryptTest():
    # ABCDE
    # FGHIK
    # LMNOP
    # QRSTU
    # VWXYZ
    key = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    ct = "DQQDEHDQBEXM"
    print unpf(ct, key)
    raw_input()
# decryptTest()

    
cipher1 = "DU UF BH RH RD LC NR QB TM TV TM TQ EC LE RF DM YE CO NL TM CD NL RQ RC HP DM TW RE QR SD BQ ED QR DU NQ QR DC"

cipher2 = "DU CB RQ ME NK ND SF HL RC QR DM RB EK QR CW EQ SE MN EL TM WB RI GM RL"

cipher3 = "EO TQ BT QR DV NR DU DR MY DM QK BY PD BO RY TL BD BQ RY PO DE SE LK TM XR HW NL CP BD NL MD DL YK WB AL SQ RA"

quads = handleQuads("english_bigrams.txt")
os = -100
cr = 0
record = (os, None)
good = []
KEY1 = strShuffle(KEY1)
KEY2 = strShuffle(KEY2)

#cribs = "TRESCOT", "THE", "CONFEDERATE", "WILKES", "CAROLINA", "SEWARD", "LORD", "COMPAN", "UNION", "BLOCKADE", "DAVIS", "MANASSAS", "BULLRUN", "RICHMOND", "REBEL", "BRITISH", "BRITAIN", "SHIP", "FEDERAL", "PORT", "ROYAL", "FLEET", "BATTLE", "TRENT", "IS", "DEAR", "STATE", "ION"
cribs = None
while os < 100000:
    cscore, ds, ks = climb( KEY1, KEY2, [cipher1, cipher2, cipher3], quads, cribs)
    KEY1, KEY2 = ks
    print cscore
    try:
        print "(record:)"
        print record[0] 
        print record[1][0]
        print record[1][1]
        print record[1][2]
        print
    except:
        pass
    if cscore <= os:
        print "reset"
        KEY1 = strShuffle(KEY1)
        KEY2 = strShuffle(KEY2)
        os = -100
#         KEY1 = OK1
#         KEY2 = OK2
#         cr += 1
#         if random() < 0.001:
#             
#             c = choice( good )            
#             KEY1, KEY2 = c[2]

    else:
        os = cscore
        
        cr = 0
        if os > record[0]:
            record = os, ds, (KEY1, KEY2)
        print
        print os, record[0]
        print KEY1, KEY2, record[2]
        print ds[0]
        print record[1][0]
        print ds[1]
        print record[1][1]
        print ds[2]
        print record[1][2]

    OK1 = KEY1
    OK2 = KEY2

