#!/usr/bin/env python2
import urllib2, bs4, argparse, sys, os, PIL.Image, PIL.ExifTags


def get_tags(url):
    page_content = urllib2.urlopen(url).read()
    page_elements = bs4.BeautifulSoup(page_content, "lxml")
    imgs = page_elements.findAll('img')
    return imgs


def dl_images(tag, url):
    try:
        if "http" in tag['src']:
            src = tag['src']
        else:
            src = url + tag['src']
        contents = urllib2.urlopen(src).read()
        fName = os.path.basename(urllib2.urlparse.urlsplit(src)[2])
        oFile = open(fName, 'wb')
        oFile.write(contents)
        oFile.close()
        print("[.] Downloaded: %s" % fName)
        return fName
    except Exception, e:
        print(str(e))
        pass


def getExif(fName, mode=0):
    try:
        exif = {}
        imgFile = PIL.Image.open(fName)
        info = imgFile._getexif()
        if info:
            for (t, v) in info.items():
                D = PIL.ExifTags.TAGS.get(t, t)
                if D == "GPSInfo":
                    gps = {}
                    for x in v:
                        DD = PIL.ExifTags.GPSTAGS.get(x,x)
                        gps[DD] = v[x]
                    exif[D] = gps
                else:
                    exif[D] = v
        if "GPSInfo" in exif:
            print("[+] %s contains GPS exif data" % fName)
        else:
            if mode == 1:
                os.remove(fName)
        return exif
    except Exception, e:
        # print(str(e))
        pass


def getCoords(exif):
    la = None
    lo = None
    if "GPSInfo" in exif:
        gps = exif["GPSInfo"]
        g_lat = getRet(gps, "GPSLatitude")
        g_lon = getRet(gps, "GPSLongitude")
        g_lat_direction = getRet(gps, "GPSLatitudeRef")
        g_lon_direction = getRet(gps, "GPSLongitudeRef")
        if g_lat != None and g_lon != None and g_lat_direction != None and g_lon_direction != None:
            la = convert_to_dec(g_lat)
            lo = convert_to_dec(g_lon)
            if g_lat_direction == "S":
                la = 0 - lat
            if g_lon_direction == "W":
                lo = 0 - lon
    return la, lo


def getRet(dic, key):
    if key in dic:
        return dic[key]
    else:
        return None


def convert_to_dec(v):
    vals = []
    for x in range(0,3):
        tmp = []
        for y in range(0,2):
            tmp.append(v[x][y])
        vals.append(float(tmp[0]) / float(tmp[1]))
    return(vals[0] + (vals[1] / 60.0) + (vals[2] / 3600.0))


def enum_images(fN, mode=0):
    if fN != None:
        try:
            exif = {}
            exif = getExif(fN, mode)
            if exif != None:
                lat, lon = getCoords(exif)
                if lat != None and lon != None:
                    print("[!!] Lat, Lon: %s, %s" % (lat, lon))
            else:
                if mode == 1:
                    os.remove(fN)
        except Exception, e:
            print(str(e))
            pass


def getargs():
    ap = argparse.ArgumentParser(description="Forensic page scraping tool for images, EXIF dump")
    ap.add_argument('-u', '--url', type=str, default=None, help="URL to scrape")
    ap.add_argument('-l', '--localdir', type=str, default=None, help="Check against local images dir")
    args, l = ap.parse_known_args()
    if (args.url == None and args.localdir == None):
        ap.print_help()
        sys.exit()
    return args.url, args.localdir


def main():
    url, localdir = getargs()
    if url:
        tags = get_tags(url)
        for tag in tags:
            fN = dl_images(tag, url)
            enum_images(fN, 1)
        print("\n[!] Done.  Keeping files that had GPS metadata")
    if localdir:
        for f in os.listdir(localdir):
            enum_images(f, 0)


if __name__=="__main__":
    main()
