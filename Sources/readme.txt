DisCoverArt 2.11.0.1
Get albumart/coverart for music based on artist and title or album
Copyright © 2025 by Johan Van Barel All Rights Reserved (xplorr@live.com)
2.3.0.2  Created by Johan Van Barel on 07/03/2013 (using Google)
2.4.0.1  Updated by Jerzy Siwinski  on 29/11/2013 (using Google)
2.5.0.1  Updated by Johan Van Barel on 02/06/2014 (using Google)
2.6.0.1  Updated by Johan Van Barel on 12/04/2016 (using Google)
2.7.0.1  Updated by Johan Van Barel on 09/02/2020 (using Google)
2.8.0.1  Updated by Johan Van Barel on 01/02/2021 (using Google)
2.9.0.1  Updated by Johan Van Barel on 06/07/2021 (using Google)
2.10.0.1 Updated by Johan Van Barel on 03/08/2022 (using Yandex)
2.11.0.1 Updated by Johan Van Barel on 17/02/2025 (using Google)

This software is distributed as freeware. If you keep using this software, send me an appreciation or feedback e-mail for my programming effort and sharing this tool for free. 
Or even better, buy me a coffee via Paypal: http://bit.ly/2meyx2s

Important remark since version 2.7.0.1:

Previous version 2.6.0.1 stopped working because Google changed the format of the returned html code.
We had to find a new method for retrieving the Google searchresults.
This new method also implies that Google no longer accepts multiple automated batch queries from within mp3tag (or others).
DisCoverArt will still work the first x automated queries, but your ip-address will be temporarily blocked by Google if you do continue after x+1 automated queries. You can however continue to use DisCoverArt for single albumart/coverart queries within mp3tag as long as Google detects that a human, not a program or bot, performs the queries.

Important remark since version 2.10.0.1:

DisCoverArt was rewritten using Yandex iso Google, because Google forces a "Before You Continue" page, forcing you to accept cookies.
Since Yandex image search is not as powerful as Google image search, it's best to use it in combination with the site parameter, to limit results from specific sites like discogs.com or amazon.com
Note that the "exclude a site from results" feature is not available on Yandex AFAIK.

Important remark since version 2.11.0.1:
DisCoverArt was rewritten again using Google iso Yandex
Discogs.com now mostly uses jpeg iso jpg, so please adapt your code also in mp3tag!

Disclaimer:

This software and the accompanying files are supplied "as is", without any express or implied warranty. 
In no event shall the author be liable for any damages whatsoever including direct, indirect, incidental, consequential, loss of business profits or special damages from the use of this software.
By using this software you agree with these conditions.


Introduction:

DisCoverArt is a command line tool to download albumart (coverart) for mp3 music files based on artist and title or album.
The target audience are people who have organized their music collection in a single track artist+title way iso based on albums or album directories.
This tool can be used stand-alone, but it was aimed to be used in conjunction with the great software called mp3tag (http://www.mp3tag.de/).
But feel free to write your own batch script for downloading your albumart using DisCoverArt.
Below you will find the description for using DisCoverArt together with mp3tag to auto batch find and import albumart based on artist and title.
It was tested with mp3tag 2.64 but may work with earlier and later versions of mp3tag as well.


Installation:

Unzip DisCoverArt.exe and custommsgbox.dll from DisCoverArt.zip to a permanent directory (f.i. %programfiles%\Mp3tag).
Register custommsgbox.dll (created by westconn1): 
open an elevated command prompt (cmd.exe as administrator) and type:
> cd %programfiles%\Mp3tag (directory where you unzipped custommsgbox.dll)
> regsvr32 custommsgbox.dll (a dialogbox will appear showing successful registration of the dll)


Description:

Usage: discoverart <artist> <title> <site> <quote> <short> <width> <height> <type> <num> <auto>
<artist> : name of the artist to search
<title>  : songtitle to search
<site>   : site to search, specify 'all' for all sites, -site to exclude a site (does not work since version 2.10.0.1)
<quote>  : 0=no quotes, 1=quote artist and title for literal search (this may reduce the number of results)
<short>  : 0=full title, 1=title part before - sign (for example titles from soundtracks who consist of 2 parts give better and uniform results)
<width>  : width of the image, 0=all size, 1=medium size (approx. 350 to 900 pixels)"
<height> : height of the image, 0=rectangle+square, 1=square"
<type>   : type of the image: .jpeg, gif, bmp, png, svg
<num>    : maximum number of images to download (1-20) (actual images downloaded may be less)
<auto>   : 0=manual single select image, 1=autosave all images


Examples:

Auto-download 1 .jpeg image with size 500x500 from the site discogs.com based on artist="Keane" and title="Everybody's Changing". 
The image will be named: "Keane - Everybody's Changing..jpeg":
> discoverart "Keane" "Everybody's Changing" discogs.com 0 0 500 500 jpeg 1 1

Auto-download 10 .jpeg images with size 300x300 from all sites, based on artist="Coldplay" and title="Viva La Vida". 
The images will be named: "Coldplay - Viva La Vida..jpeg", "Coldplay - Viva La Vida1..jpeg", "Coldplay - Viva La Vida2..jpeg",...:
> discoverart "Coldplay" "Viva La Vida" all 1 0 300 300 .jpeg 10 1

Manually select 1 .jpeg image with size 500x500 out of max. 5 suggestions from the site discogs.com based on artist="Keane" and title="Everybody's Changing". 
The image will be named: "Keane - Everybody's Changing..jpeg".
You will be presented with max. 5 images. You can select "Yes", this will keep the selected image; "No", this will continue to the next image; "Cancel", this will abort the search.
> discoverart "Keane" "Everybody's Changing" discogs.com 0 0 500 500 jpeg 5 0




Usage in conjunction with mp3tag (http://www.mp3tag.de/):

DisCoverArt was designed to be used in conjunction with a software called mp3tag (http://www.mp3tag.de/).
It has been tested that searching 300x300 images gives the best results. (500x500 is also an option, but gives less results).
Here are the possible suggestions to use DisCoverArt together with mp3tag.

Precondition: It is needed that at least the tags called "Artist" and "Title" are available in the mp3 files. 
If not, you can easily derive these tags from the filename using mp3tag. 
If the filename has the form "Artist - Title.mp3", select in the menu "Convert/Filename Tag" and use as the format string: %artist% - %title%.

Before using DisCoverArt, you should first make 3 definitions in mp3tag. One for auto-batch search and 2 (+2 optional) for manual search.
If you don't want to make these definitions manually, there is a configuration file for mp3tag available in DisCoverArt.zip called Mp3tagSettings.zip that you can unzip to %appdata%\mp3tag. Warning: these settings will overwrite your previous settings in mp3tag.
Here is the manual method:

Create a tool for the batch search 300x300:
In the menu, select "Tools/Options/Tools" and click on the button "New" (button with yellow star).
Name: "DisCoverArt Discogs 300x300 Artist+Title"
Path: select the path where you unzipped DisCoverArt.exe (f.i. C:\Program Files\Mp3tag) and select DisCoverArt.exe
Parameter: "%artist%" "%title%" discogs.com 0 1 300 300 jpeg 1 1
Select the checkbox "For all selected files" and click "Ok".

Create another tool for the manual single search 300x300:
In the menu, select "Tools/Options/Tools" and click on the button "New" (button with yellow star).
Name: "DisCoverArt Discogs 300x300 Artist+Title Manual"
Path: select the path where you unzipped DisCoverArt.exe (f.i. C:\Program Files\Mp3tag) and select DisCoverArt.exe
Parameter: "%artist%" "%title%" discogs.com 0 1 300 300 jpeg 20 0
Do not Select the checkbox "For all selected files" and click "Ok".

Create another tool for the manual single search 500x500:
In the menu, select "Tools/Options/Tools" and click on the button "New" (button with yellow star).
Name: "DisCoverArt Discogs 500x500 Artist+Title Manual"
Path: select the path where you unzipped DisCoverArt.exe (f.i. C:\Program Files\Mp3tag) and select DisCoverArt.exe
Parameter: "%artist%" "%title%" discogs.com 0 1 500 500 jpeg 20 0
Do not Select the checkbox "For all selected files" and click "Ok".

Optionally you can also create 2 extra definitions for 2 extra manual searches.

Create another tool for the manual single search Medium Size + Square images:
In the menu, select "Tools/Options/Tools" and click on the button "New" (button with yellow star).
Name: "DisCoverArt Discogs Medium+Square Artist+Title Manual"
Path: select the path where you unzipped DisCoverArt.exe (f.i. C:\Program Files\Mp3tag) and select DisCoverArt.exe
Parameter: "%artist%" "%title%" discogs.com 0 1 1 1 jpeg 20 0
Do not Select the checkbox "For all selected files" and click "Ok".

Create another tool for the manual single search Medium Size images:
In the menu, select "Tools/Options/Tools" and click on the button "New" (button with yellow star).
Name: "DisCoverArt Discogs Medium Artist+Title Manual"
Path: select the path where you unzipped DisCoverArt.exe (f.i. C:\Program Files\Mp3tag) and select DisCoverArt.exe
Parameter: "%artist%" "%title%" discogs.com 0 1 1 0 jepg 20 0
Do not Select the checkbox "For all selected files" and click "Ok".

Now you should also create 2 new actions in mp3tag: one to save coverart (and optionally another to delete coverart).

Create action to Save Coverart.
In the menu, select "Actions/Actions" and click on the button "New" (button with yellow star).
Name of action group: "Save Coverart", and click "Ok".
click on the button "New" (button with yellow star).
Select Action Type: "Import Cover From File"
Format string for image filename: %artist% - %title%..jpeg
Import cover as: Front Cover.
Check: "Delete existing cover art" and click "Ok".

Create action to  Delete Coverart.
In the menu, select "Actions/Actions" and click on the button "New" (button with yellow star).
Name of action group: "Delete Coverart", and click "Ok".
click on the button "New" (button with yellow star).
Select Action Type: "Remove fields"
Fields to remove: PICTURE

Now you can start importing coverart using mp3tag and DisCoverArt.
Important: existing coverart may be overwritten in the directory where the music file is located and also in the music file itself!

First load the directory where your mp3 files are located: In the menu, select "File/Change Directory" and select your mp3 directory.
It is handy to add a field "Cover" in the view to show and sort which mp3 files already have albumart/coverart.
To do that, right-click on the header of the table and select "Customize columns..." and check the label called "Cover" and click "Ok".
Now sort on that column "Cover". Those who already have coverart should show a 1, the others are empty.
Now multiple-select the "empty cover" music files (using shift or control key and mouse).
It is recommended to select a maximum of 300 mp3 files at once, otherwise your computer may slow down or results may be skipped, since queries are almost done simultaneously.
Now right-click on the selected mp3 files and select "Tools/DisCoverArt Discogs 300x300 Artist+Title"
Now you should see a number of black console windows popping up, one for each music file, doing a query using DisCoverArt.
Wait until all the console windows are closed. 
Now DisCoverArt has created ..jpeg files with the name "Artist - Title..jpeg" (note that existing .jpeg's with that name will be overwritten!).
Now you should batch import those ..jpeg files into the music files (keep the same music files select in mp3tag): from the menu select "Actions/Save Coverart"

Now you can walk over the music files in mp3tag and see/evaluate the imported coverart.

Sometimes it may occur that no coverart was found or that the imported .jpeg was not good.
In this case you can manually select an image to import as coverart.
Select only one mp3 file, right-click and select "Tools/DisCoverArt Discogs 300x300 Artist+Title Manual".
Now you can visually select the image you prefer: select "Yes", this will keep the selected image; "No", this will continue to the next image; "Cancel", this will abort the search.
After you selected an image, it is only downloaded to a file called "Artist - Title..jpeg" (note that an existing .jpeg with that name may be overwritten!).
Now you should import this .jpeg file into the music file: while the mp3 file is still selected, from the menu select "Actions/Save Coverart".
If this method does not succeed, try a 500x500 search: "Tools/DisCoverArt Discogs 500x500 Artist+Title Manual"
If this method does not succeed, try a Medium+Square search: "Tools/DisCoverArt Discogs Medium+Square Artist+Title Manual"
If this method does not succeed, try a Medium search: "Tools/DisCoverArt Discogs Medium Artist+Title Manual"
You can always remove the saved coverart via: "Actions/Remove Coverart" one by one or in group. This will leave your mp3 files untouched!

Using this method you can easily and fast batch import albumart/coverart for your complete music mp3 library.
Have fun! 


