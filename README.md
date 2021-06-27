# image-uploader

Yep. Hosts images. One of the more well-coded and graceful scripts I’ve written. Takes advantage of the multiple-upload HTML5 element. Each uploaded image is hashed to it’s CRC32 hash, and then stored in one of 16 directories created via UUID’s. The UUID is generated and then a prefix is applied for each element of the hexadecimal elements (regex [0-9a-f]). This way, we get a more or less uniform distribution of files across 16 directories to reduce the stress on the filesystem if you had them all stuffed in one directory. Should be good for at least several hundred thousand files per instance of the script. The script also tries to be as dynamic and self-healing as possible. If it detects missing data directories it simply recreates it. If you upload a file that already exists it will overwrite the current file. Thumbnails are generated at upload using the PHP ImageMagick PECL library. HTML, phpBB, and direct URL codes are given when images are uploaded.

***

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
