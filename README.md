# Simply enjoy your pictures.
**Jeroboam** is a photo gallery creator, leaving your pictures where they are.
No need to upload them and make a redondant copy as usual gallery software do.
With a single script, create your own gallery in one call.
It should work flawlessly under Linux and Mac OS, use Windows at your own risks.
It has been successfully tested with Python 2.7 and 3.4. 


# Usage
Call:

	./jeroboam.py

from its installation directory. It asks you for a directory where your pictures are.
It will use the associated theme file `theme.tpl` file to start a webservice.
Go to the `http://0.0.0.0:8080` address in your browser. And voilà, it's done!


# Like it? Hate it? Don't care?
Jeroboam is at very early develoment stage.
Feel free to enjoy at, ask for or complain about anything through
[Github issues](https://github.com/stephanepechard/jeroboam/issues).


# Technical details
Jeroboam creates its own [virtualenv](http://virtualenv.readthedocs.org/)
and relaunches itself with it. Thus, you need either the `virtualenv` or
the `pyvenv` command available. As pillow is installed, you'll also need
the Python headers. I should probably work on this cumbersome dependency one day...


# Thanks
Jeroboam uses some tools:

- [Bottle](http://bottlepy.org/), to serve the service easily ;
- [exifread](https://pypi.python.org/pypi/ExifRead), to extract information about picture files ;
- [Pillow](https://pillow.readthedocs.org/), to create thumbnails ; 
- [Lightbox2](https://github.com/lokesh/lightbox2), to enjoy fullscreen pictures ;
- [Google Fonts](https://www.google.com/fonts), to style stuff a bit.
