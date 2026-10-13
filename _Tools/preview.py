import sys, glob, os
from PIL import Image
def contact(paths, out, zoom=2, bg=(90,120,80,255), maxw=1800):
    ims=[Image.open(p).convert('RGBA') for p in paths]
    W=max(i.width for i in ims); H=sum(i.height+2 for i in ims)
    sheet=Image.new('RGBA',(W,H),bg); y=0
    for i in ims:
        sheet.alpha_composite(i,(0,y)); y+=i.height+2
    sheet=sheet.resize((sheet.width*zoom,sheet.height*zoom),Image.NEAREST)
    sheet.save(out)
    print(sheet.size)
if __name__=='__main__':
    pat=sys.argv[1]; out=sys.argv[2]; zoom=int(sys.argv[3]) if len(sys.argv)>3 else 2
    paths=sorted(glob.glob(pat,recursive=True))
    print(len(paths),'files'); contact(paths,out,zoom)
