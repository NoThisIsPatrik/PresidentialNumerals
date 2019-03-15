#!/usr/bin/env python3
try:
    from bs4 import BeautifulSoup as bs
    import requests
    NODL = False
except Exception as e:
    print("Missing bs4 (BeautifulSoup) and/or Requests")
    print("But that's Ok though - if all the files came with it's all good")
    NODL = True
    
from PIL import Image, ImageDraw, ImageFont

import os
import time
from sys import argv
DIR = "./pics"                 # Where to look for/store pictures
FONT = "./AbrahamLincoln.ttf"  # Font for writing on images (optional)
WIDTH = 1000                   # Output image width

    # Download numbers, names and pictures from wikipedia
    # cache in "pres.csv" and "./pic/*.jpg".
def collectData(): 
    global DIR

    try:
        db = { int(a.split(',',1)[0]):a.split(',',2)[1:] for a in open("pres.csv").read().splitlines() }
        if db and all(os.path.isfile(db[k][1]) for k in db):
            return db
    except Exception as e:
        print(e)
        print("Can't find the support files (pres.csv, pic/*.jpg), trying to download them")
        if NODL:
            print("Oh yeah, actually I can't - no bs4 and/or requests. Do 'python3 -mpip install bs4 requests',")
            print("or reclone me, run me where I can find my stuff, or whatevers")
            quit()

    s = requests.session()
    if not os.path.isfile('presidents.html'):
        r = s.get("https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States")
        open('presidents.html','w').write(r.text)
        pg = r.content
    else:
        pg = open('presidents.html').read()

    sou = bs(pg,"lxml")
    tb = [a for a in sou('table') if a('big')]
    if len(tb)!=1:
        print("(The page is strange now, so this may not work)")
    tb = tb[0]

    pz = tb('big')
    urls = [a['src'] for a in tb('img')]
    pzl = [(a[0]+1,a[1][0].text,a[1][1]) for a in list(enumerate(zip(pz,urls)))]

    if not os.path.isdir("./pics"):
        os.mkdir(DIR)

    p = 1
    final_dict = {}
    for (num,name,u) in pzl:
        ur = f"https:{u}"
        fn = f"{DIR}/p{p}.jpg"
        p += 1
        if os.path.isfile(fn):
            final_dict[num] = (name,fn)
            continue

        print(f"Getting {name} ({ur})")
        rt = 3
        while rt:
            try:
                r = s.get(ur)
                break
            except Exception as e:
                print(f"Error: {e}")
                rt -= 1
                if rt:
                    print(f"Trying again (up to {rt} more times)")
                else:
                    print("Not working, quitting")
                    exit(1)
        print(f"Done, {len(r.content)} bytes. Saving as {fn}")
        open(fn,'wb').write(r.content)

        final_dict[num] = (name,fn)
        time.sleep(0.5)
    open("pres.csv","w").write('\n'.join(f"{a[0]},{a[1][0]},{a[1][1]}" for a in final_dict.items())) 
    return final_dict

def main():
    global db

    num = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420198" # Default, Pi
    lim = 100  # default length
    opts = 0   # default no writing ( bit 1 == add names, bit 2 == add numbers )

    if len(argv)==1:
        print("Usage: [output image] [-n number] [-f file] [-l limit] [-new]\n")
        print("   -n <123>   Number to represent")
        print("   -f <file>  File to load number from")
        print("   -l <n>     Limit the number of digits to use (default is some)")

        # print("   -new       Use presidents from as recently as possible") 
            # TODO: There are too many clever guidance things, probably "initally avoid reuse", like 34,3,4 
            # instead of 34,34 or 3,4,3,4 would be first. Old/new might be nice too. There were fewer options
            # than I thought.

        print("   -name      Add in name as a caption")
        print("   -numb      Add in number as a caption")
        print("\nDefaulting..")
        outfn = "piday.jpg"
    else:
        if argv[1][0]!='-':
            outfn = argv[1]
        else:
            outfn = "piday.jpg"

        if (not outfn.endswith(".jpeg") and
            not outfn.endswith(".jpg")):
            outfn += ".jpg"

        for i in range(len(argv)):
            if argv[i] == '-name':
                opts |= 1
            if argv[i] == '-numb':
                opts |= 2
            if argv[i] == '-n':
                num = argv[i+1]
            if argv[i] == '-f':
                num = ''.join(a for a in open(argv[i+1]).read() if a.isdigit() or a=='.')
            if argv[i] == '-l':
                lim = int(argv[i+1])
            #if argv[i] == '-new':
            #    newopt = 1

    if '.' in num:
        dotpos = [i for i in range(len(num)) if num[i]=='.'] # TODO: Draw this in perhaps?
        num = num.replace('.','')
        
    if len(num)>lim:
        num = num[:lim]
    else:
        lim = len(num)

    print(f"Number: {num}..")

    db = collectData()

    if not db:
        print("Failed to load stuff in some mysterious way that didn't crash")
        return
    p = 0 
    spl = []
    while p<len(num):
        if num[p]!='0' and int(num[p:p+2]) in db:
            spl.append(int(num[p:p+2]))
            p += 2
        elif int(num[p:p+1]) in db:
            spl.append(int(num[p:p+1]))
            p += 1
        else:
            break

    if p<len(num):
        print(f"I can only do {p} digits. There's no {num[p]}:th or {num[p-1:p+1]}th president :-(.")
    if not spl:
        print(".. which is to say, I can't do any of it.")
        return
    print("")

    npr = len(spl)
    print(f"{npr} presidents total")
    r = 1
    c = int(npr / r)
    w = int(WIDTH / c)

    while w<100:
        r += 1
        c = int(npr/r)
        if c*r < npr:
            c += 1
        w = int(WIDTH / c)

    h = int(w*200/165)
    tw = w*c
    th = h*r

    print(f"Each will be {w} wide, {r} rows, {c} in each")
    fI = Image.new("RGB",(tw,th))
    
    print(f"So here's how it's going to go:")
    for a in spl:
        print(f"  {a:2d}  {db[a][0]}")
    print("")
    p = 0
    ox,oy = 0,0
    fsz = 26
    while p<len(spl):
        cp = spl[p]
        p += 1
        fn = db[cp][1]
        I = Image.open(fn).convert("RGBA")
        I.thumbnail((w,h))
        tx,ty = I.size

        if ox+tx >= tw:
            ox = 0
            oy += ty

        if opts & 1 or opts & 2: # Cheat-add name caption / number
            d = ImageDraw.Draw(I)

            if opts & 2:
                #print("DoingNumb")
                fnt = ImageFont.truetype(FONT, size=40)
                scp = f"{cp}"
                if len(scp)==1:
                    d1 = scp[0]
                    ntx,nty = int(tx/2)-7, 5
                    d.text( (ntx, nty), d1, font=fnt , fill=(200,255,255,0) )
                else:
                    d1 = scp[0]
                    d2 = scp[1]
                    ntx,nty = (int(tx/4)-7, 8)
                    d.text( (ntx, nty), d1, font=fnt, fill=(255,200,200,0) )
                    ntx,nty = (int((tx*3)/4)-7, 8)
                    d.text( (ntx, nty), d2, font=fnt, fill=(255,200,200,0) )
                 
                # 14(per) x 20
                #quit()

            if opts & 1:
                # print("DoingText")
                while(1):
                    fnt = ImageFont.truetype(FONT, size=fsz)
                    txt_w, txt_h = d.textsize(db[cp][0], font=fnt)

                    if txt_w > int(tx*0.90):
                        # print(f"{fsz} is too large - {txt_w} text {tx} img")
                        fsz -= 1
                    elif txt_w < int(tx*0.80):
                        # print(f"{fsz} is too small - {txt_w} text {tx} img")
                        fsz += 1
                    else:
                        # print(f"{fsz} is just right - {txt_w} text {tx} img")
                        break

                mx = int((tx-txt_w)/2)
                d.text( (mx, (ty-txt_h-10)), db[cp][0], font=fnt) #, fill=(255,255,255,0) )

        fI.paste(I,(ox,oy))
        ox += tx
    fI.save(outfn)    
    print(f"Done. It's in {outfn}")

if __name__=="__main__":
    main()

# font from https://befonts.com/presidential-dollars.html by Behance.
