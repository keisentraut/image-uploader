#!/usr/bin/python

import sys
from pathlib import Path
import os
import sys
import PIL.Image
import PIL.ExifTags

INDEX_HTML="""
<!DOCTYPE html>
<html>
<head>
    <title>CAPTION (NUMBERIMAGES images)</title>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <script src="img.js"></script>
    <link rel="stylesheet" href="img.css">
</head>
<body>
<a href="REL_BEFORE" id="before"></a>
<a href="REL_AFTER"  id="after"></a>
<h1>CAPTION (NUMBERIMAGES images)</h1>
FILEINDEXES
</body>
</html>
"""

IMG_JS="""
function before() {
    window.location.href = document.getElementById("before");
}
function after() {
    window.location.href = document.getElementById("after");
}
//  detect arrow keys
function checkKey(e) {
    e = e || window.event;
    if (e.keyCode == '38') {
        // up arrow
        before();
    }
    else if (e.keyCode == '40') {
        // down arrow
        after();
    }
    else if (e.keyCode == '37') {
       // left arrow
        before();
    }
    else if (e.keyCode == '39') {
       // right arrow
        after();
    }
}
document.onkeydown = checkKey;

// detect swipes
// https://stackoverflow.com/a/56663695
let touchstartX = 0
let touchendX = 0
let MINDIST = 400;
function handleGesture() {
    if (touchendX + MINDIST < touchstartX) after();
    if (touchendX - MINDIST > touchstartX) before();
}
document.addEventListener('touchstart', e => {
touchstartX = e.changedTouches[0].screenX
})
document.addEventListener('touchend', e => {
touchendX = e.changedTouches[0].screenX
handleGesture()
})
"""

IMG_CSS="""
.thumb {
    margin:10px;
}
"""

IMG_HTML="""
<!DOCTYPE html>
<html>
    <title>TITLE</title>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <script src="REL_IMGJS"></script>
<head>
</head>
<body>
<a href="REL_BEFORE" id="before"></a>
<a href="REL_AFTER"  id="after"></a>
</datalist>
<h1>TITLE</h1>
<div style="position:absolute; top:0px; left:0px; width:100%; height:100%; background:url(REL_IMAGE); background-size:contain; background-repeat:no-repeat; background-position:center; overflow:auto;">
</div>
</body></html>
"""

def usage():
    print("create_gallery.py IMAGEDIR [OUTPUTDIR]")
    print("")
    print("  creates a simple desktop- and mobile-friendly HTML gallery")
    print("  for a given directory of image files")
    sys.exit(1)

makedir_cache=set()

def get_names(indir, outdir, infile):
    # indir  = /a/b/c/
    # outdir = /a/b/html_c/
    # infile = /a/b/c/dir1/dir2/test.png
    rel = infile.relative_to(indir)
    # rel    = dir1/dir2 A
    outname = str(rel).removesuffix(rel.suffix)
    localfile_image   = outdir / (outname + ".jpg")
    localfile_thumb = outdir / (outname + "_thumb.jpg")
    localfile_html = outdir / (outname + ".html")
    if localfile_html.parent not in makedir_cache:
        os.makedirs(localfile_html.parent, exist_ok=True)
        makedir_cache.add(localfile_html.parent)
    return rel, outname, localfile_image, localfile_thumb, localfile_html 

def create_thumbnail(original_image, localfile_image, localfile_thumb):
    i = PIL.Image.open(original_image)
    # fix orientation, https://stackoverflow.com/a/26928142
    for orientation in PIL.ExifTags.TAGS.keys():
        if PIL.ExifTags.TAGS[orientation]=='Orientation':
            break
    if orientation: 
        exif = i._getexif()
        if exif and orientation in exif:
            if exif[orientation] == 3:
                i=i.rotate(180, expand=True)
            elif exif[orientation] == 6:
                i=i.rotate(270, expand=True)
            elif exif[orientation] == 8:
                i=i.rotate(90, expand=True)
    t = i.copy()
    t.thumbnail((300,300), resample=PIL.Image.Resampling.LANCZOS)
    assert(not localfile_thumb.exists())
    t.save(localfile_thumb, quality = 75)
    i.thumbnail((1920,1080), resample=PIL.Image.Resampling.LANCZOS)
    assert(not localfile_image.exists())
    i.save(localfile_image, quality = 75)

def create_img_html(localfile_html, title, rel_image, rel_before, rel_after, rel_imgjs):
    #print(f"create_img_html({localfile_html=}, {title=}, {rel_image=}, {rel_before=}, {rel_after=}, {rel_imgjs=})")
    with open(localfile_html, "w") as f:
        f.write(IMG_HTML.replace("TITLE", title)
                        .replace("REL_IMAGE", rel_image)
                        .replace("REL_BEFORE", rel_before)
                        .replace("REL_AFTER", rel_after)
                        .replace("REL_IMGJS", rel_imgjs))

def create(indir, outdir):
    files = [i for i in indir.rglob('*') if i.is_file() and i.name]
    # filter for image extensions
    files = [i for i in files if i.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".heic", ".webp"]]
    assert(len(files) > 0)
    files = sorted(files)
    os.mkdir(outdir)
    # index.html
    localfile_index_html = outdir / "index.html"
    sys.stdout.write("processing ... ")
    sys.stdout.flush()
    with open(localfile_index_html, "w") as f:
        fileindexes = ""
        for infile in files:
            rel, outname, localfile_image, localfile_thumb, localfile_html = get_names(indir,outdir,infile)
            rel_thumb = os.path.relpath(localfile_thumb, start=outdir)
            rel_html  = os.path.relpath(localfile_html,  start=outdir)
            fileindexes += f'<a href="{rel_html}"><img src="{rel_thumb}" alt="{outname}" class="thumb"/></a>'
        before = get_names(indir, outdir, files[-1])[4]
        after =  get_names(indir, outdir, files[ 0])[4]
        rel_before = os.path.relpath(before, start=localfile_html.parent)
        rel_after  = os.path.relpath(after,  start=localfile_html.parent)
        f.write(INDEX_HTML
            .replace("CAPTION", indir.name)
            .replace("NUMBERIMAGES", str(len(files)))
            .replace("FILEINDEXES", fileindexes)
            .replace("REL_BEFORE", rel_before)
            .replace("REL_AFTER", rel_after)
            )
    # img.js
    localfile_img_js = outdir / "img.js"
    with open(localfile_img_js, "w") as f:
        f.write(IMG_JS)
    # img.css
    localfile_img_css = outdir / "img.css"
    with open(localfile_img_css, "w") as f:
        f.write(IMG_CSS)

    for index in range(len(files)):
        infile = files[index]
        rel, outname, localfile_image, localfile_thumb, localfile_html = get_names(indir,outdir,infile)
        sys.stdout.write(f"{outname} ... ")
        sys.stdout.flush()
        create_thumbnail(infile, localfile_image, localfile_thumb)
        before = get_names(indir, outdir, files[index-1])[4] if index != 0             else localfile_index_html
        after  = get_names(indir, outdir, files[index+1])[4] if index != len(files)-1  else localfile_index_html
        rel_before = os.path.relpath(before, start=localfile_html.parent)
        rel_after  = os.path.relpath(after,  start=localfile_html.parent)
        rel_image  = os.path.relpath(localfile_image, start=localfile_html.parent)
        rel_imgjs  = os.path.relpath(outdir / "img.js", start=localfile_html.parent)
        create_img_html(localfile_html, outname, str(rel_image), str(rel_before), str(rel_after), str(rel_imgjs))
    sys.stdout.write("done.\n")

if __name__ == "__main__":
    indir = None
    if len(sys.argv) == 2:
        indir = Path(sys.argv[1])
        assert(indir.parent)
        assert(indir.name)
        outdir = indir.parent / ("html_" + indir.name)
    elif len(sys.argv) == 3:
        indir = Path(sys.argv[1])
        outdir = Path(sys.argv[2])
    else:
        usage()
    assert(indir.is_dir())
    assert(not outdir.exists())
    print(f"creating gallery for {indir} in {outdir}")
    create(indir,outdir)
