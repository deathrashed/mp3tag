# ######################################################################
#                       WTF PUBLIC LICENSE
#                   Public Version 27, Sep 2023
#
# Copyright (C) 2020-2023 Bugzero <bugzero71@gmail.com>
# I would like to thank stevehero for his scripts. I've learned a lot.
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#                       WTF PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You can do WTF you imagine with this document.
# ######################################################################
# Version 0.52
# ######################################################################

[Name]=Genius [0.52 by Bugzero]
[MinAppVersionMac]=1.8.4
[MinAppVersionWin]=3.22
[Settings]=Genius#Settings….settings
[BasedOn]=Genius.com


[ParserScriptAlbum]=...
# #################################################################### #
#                               T I T L E
# #################################################################### #

# debug "on" "debug_genius_album_json.log"
# debugwriteinput "debug_genius_input.html"

# Find the body part of html code
findlinenocase "<!doctype"
joinuntil "</html>"

# Clear lyrics ads
# Do
#   regexpreplace "<div\s+class=\"[^lL][^>]*>[^<]*<\s*\/div\s*>" ""
#   regexpreplace "<div\s+id=\"[^lL][^>]*>[^<]*<\s*\/div\s*>" ""
# While "<!doctype" 6
# regexpreplace "<div\s*data-primis[^>]*>[^<]*<\s*\/div\s*>" "<br\>"
# regexpreplace "<div\s+data-[^>]*>[^<]*<\s*\/div\s*>" "<br\>"

# Search optional tags
regexpreplace "<meta\s*content=\"([^\"]+?)\"\s+property=\"og:image\"\s*\/>" "<cover:start>$1<cover:end>"
regexpreplace "<meta\s*content=\"([^\"]+?)\"\s+property=\"og:title\"\s*\/>" "<title:start>$1<title:end>"
regexpreplace "<meta\s*content=\"([^\"]+?)\"\s+property=\"og:url\"\s*\/>" "<url:start>$1<url:end>"

#
# #################################################################### #
# Clear lyrics html codes and advertisements
# #################################################################### #
#
replace "&quot;" "\""
replace "&#x27;" "'"
replace "&#39;" ","
replace "&amp;" "&"

replace "&lt;" "<"
replace "&gt;" ">"
# regexpreplace "<!--[\/ \w]*?-->" ""
# regexpreplace "<[\w\d]+ [^>]*?>" ""
# regexpreplace "<\/[\w\- _]*?>" ""
# regexpreplace "  +" " "

outputto "TEMP_CoverUrl"
gotochar 1
findinline "<cover:start>"
sayuntil "<cover:end>"

# outputto "TEMP_Title"
# gotochar 1
# findinline "<title:start>"
# sayuntil "<title:end>"

outputto "GENIUS_URL"
gotochar 1
findinline "<url:start>"
sayuntil "<url:end>"

gotochar 1

#
# #################################################################### #
# Time to get lyrics from JSON
# #################################################################### #
#
# Find the JSON information
regexpReplace "(?i).(window\.__APP_CONFIG__.*)" ""
regexpReplace "(?i).*__PRELOADED_STATE__[\s=]+JSON\.parse\('(.+\}+)'\);" "$1"

# Rubbish

# Clean href sometimes added when lyrics should be checked
regexpreplace "<a href=([^>]*?)>(.*?)<\\\/a>" "$2"

# Clean italics and bold modifiers
regexpreplace "<i>(.*?)<\\\/i>" "$1"
regexpreplace "<b>(.*?)<\\\/b>" "$1"

# Clean useless html codes
replace "<p>"    ""
regexpreplace "<\\\/p>" ""
replace "<br>"   ""

# Convert carriage return codes \n to the option on user preferences
IfVar "SettingLineEndingCharacter" "LF (Linux)"
  replace "\\\\n" "\\u000a"
Endif
IfVar "SettingLineEndingCharacter" "CR/LF (Windows)"
  replace "\\\\n" "\\u000d\\u000a"
Endif
IfVar "SettingLineEndingCharacter" "CR (Mac)"
  replace "\\\\n" "\\u000d"
Endif

# Convert some unicode characters to \u code
replace "\\\\\\\"" "\\u0022"
replace "\\'"      "\\u0027"
replace "\\$"      "\\u0024"

# json format spec for keys and values
replace "\\\"" "\""

#regexpreplace "\"embedContent\":\".+\"," ""

# #################################################################### #
# Read JSON Object
# #################################################################### #

json "ON" "current"

json_select_object "songPage"

# Get Song ID
json_select "song"
outputto "TEMP_SongId"
sayrest

#
#Lyrics

json_select_object "lyricsData"
json_select_object "body"
IfVar "SetUNSYNCEDLYRICS" "true"
outputto "UNSYNCEDLYRICS"
Else
outputto "LYRICS"
EndIf
json_select "html"
sayrest

json_unselect_object  # body
json_unselect_object  # lyricsData

json_foreach "trackingData"
  json_select "key"
  If "Title"
    outputto "TEMP_Title"
    json_select "value"
    sayrest
  Endif

  json_select "key"
  If "Primary Artists"
    IfNot "Primary Artists IDs"
      outputto "TEMP_Artist"
      IfVar "SettingMultiTAG" "Multiple"
        json_select_array "value" -1 "\\\\"
      Else
        json_select_array "value" -1 ", "
      Endif
      sayrest
    Endif
  EndIf

  json_select "key"
  If "Primary Album"
    IfNot "Primary Album ID"
      outputto "TEMP_Album"
      json_select "value"
      sayrest
    Endif
  EndIf

  json_select "key"
  If "Tag"
    outputto "TEMP_Genre"
    json_select "value"
    sayrest
  Endif

  json_select "key"
  If "Release Date"
    outputto "TEMP_Year"
    json_select "value"
    sayrest
  Endif

json_foreach_end

json_unselect_object  # songPage

json_select_object "entities"
json_select_object "songs"
json_select_object "%TEMP_SongId%"

#
# Artists
outputto "TEMP_GeniusPrimaryArtist"
json_select "primaryArtistNames"
sayrest

outputto "TEMP_GeniusArtists"
json_select "artistNames"
sayrest

#
# Writers
outputto "TEMP_Writer"
IfVar "SettingMultiTAG" "Multiple"
  json_select_many "writerArtists" "name" "\\\\"
Else
  json_select_many "writerArtists" "name" ";"
Endif
sayrest

#
# Tags/Genre
outputto "TEMP_Tags"
IfVar "SettingMultiTAG" "Multiple"
  json_select_many "tags" "name" "\\\\"
Else
  json_select_many "tags" "name" ";"
Endif
sayrest

#
# Producers
outputto "TEMP_Producers"
IfVar "SettingMultiTAG" "Multiple"
  json_select_many "producerArtists" "name" "\\\\"
Else
  json_select_many "producerArtists" "name" ";"
Endif
sayrest

#
# Featuring
outputto "TEMP_Featured"
IfVar "SettingMultiTAG" "Multiple"
  json_select_many "featuredArtists" "name" "\\\\"
Else
  json_select_many "featuredArtists" "name" ";"
Endif
sayrest

#
# #################################################################### #
#                       C U S T O M I Z A T I O N
# #################################################################### #
#

IfVar "SetUNSYNCEDLYRICS" "true"
set "LYRICS"
Else
set "UNSYNCEDLYRICS"
EndIf

outputto "Title"
sayoutput "TEMP_Title"

outputto "Artist"
IfVar "SetARTISTOrigin" "Generated"
  sayoutput "TEMP_Artist"
Else
  IfVar "SetARTISTOrigin" "Genius Primary"
    sayoutput "TEMP_GeniusPrimaryArtist"
  Else
    sayoutput "TEMP_GeniusArtists"
  Endif
Endif

outputto "CoverUrl"
sayoutput "TEMP_CoverUrl"

outputto "Album"
sayoutput "TEMP_Album"

outputto "Year"
sayoutput "TEMP_Year"

outputto "Genre"
IfVar "SetGENREOrigin" "Primary"
  sayoutput "TEMP_Genre"
Else
  sayoutput "TEMP_Tags"
Endif

outputto "Author"
sayoutput "TEMP_Writer"

outputto "Producer"
sayoutput "TEMP_Producers"

outputto "Featured"
sayoutput "TEMP_Featured"

# set "GENIUS_URL"

set "TEMP_Title"
set "TEMP_Artist"
set "TEMP_GeniusPrimaryArtist"
set "TEMP_GeniusArtists"
set "TEMP_Album"
set "TEMP_CoverUrl"
set "TEMP_Year"
set "TEMP_Genre"
set "TEMP_Writer"
set "TEMP_Tags"
set "TEMP_Producers"
set "TEMP_Featured"
set "TEMP_SongId"

# #################################################################### #
#
#     _____   _____   _   _   _____   _   _   _____
#    |  __ \ |  ___| | \ | | |_   _| | | | | /  ___|
#    | |  \/ | |__   |  \| |   | |   | | | | \ `--.
#    | | __  |  __|  | . ` |   | |   | | | |  `--. \
#    | |_\ \ | |___  | |\  |  _| |_  | |_| | /\__/ /
#     \____/ \____/  \_| \_/  \___/   \___/  \____/
#
#
#     _             _
#    | |           | |
#    | |__  _   _  | |__  _   _  __ _ _______ _ __ ___
#    | '_ \| | | | | '_ \| | | |/ _` |_  / _ \ '__/ _ \
#    | |_) | |_| | | |_) | |_| | (_| |/ /  __/ | | (_) |
#    |_.__/ \__, | |_.__/ \__,_|\__, /___\___|_|  \___/
#            __/ |               __/ |
#           |___/               |___/
#
# #################################################################### #
