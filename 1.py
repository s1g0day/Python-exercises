for i in open("url.txt").readlines():
    z = i.find(":443\n")
    x = i.find(":80\n")
    i = i.strip("\n")
    if (z!=-1):
        # i = i.replace("http","https")
        a443 = i.replace(":443","")
        print(a443)
    elif (x!=-1):
        a80 = i.replace(":80","")
        print(a80)
    elif(z==-1 and x==-1):
        print(i)
        # pass