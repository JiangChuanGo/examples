#encoding=utf-8
import time

start=time.time()

def solve(nHeads, nFoots):
    for rabbit in range(nHeads + 1):
        chick = nHeads - rabbit
        foots = 4 * rabbit + 2 * chick
        if foots == nFoots:
            return {"rabbit": rabbit, "chick": chick, "foots": nFoots, "heads" : nHeads}
        
    return None
        
result = solve(35, 94)

print("兔： %d, 鸡：%d, 足: %d" % (result["rabbit"], result["chick"], result["foots"]))

end=time.time()
print('Running time: %s Seconds'%(end-start))