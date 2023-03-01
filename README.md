# image-uploader

I use this to collect pictures from family and friends after some event.
I just create a secret directory named ```party-on-202X-XX-XX``` on a public webserver with PHP and send people the link to it.
They then upload their images (or other files) and can also preview images.

It also prevents duplicates to be uploaded.
After everyone has uploaded his/her files, I rename them and sort files with ```./sort.sh```.
Afterwards, I send the ZIP link around in WhatsApp and everyone can download it.

## Origin

The HTML and the PHP code is very loosely based on [pengc99/image-uploader](https://github.com/pengc99/image-uploader) simple image hoster. Thanks!
