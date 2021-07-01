import os
import random

folder = "LOGOS.TXT"
art_list= []

def splash():
    if (os.path.isfile(folder)):
        fd = open(folder,"r",encoding="utf16")
        data = fd.readlines()
        line = ""
        last_char = ""
        art = ""
        i=0
        for line in data:
            if len(line) > 1:
                art+= line
            else:
                if art != "":
                    art_list.append(art)
                art= ""
        art_list.append(art)
        n = random.randrange(0,len(art_list))
        print (art_list[n])
    else:
        print("LOGO.TXT missing")