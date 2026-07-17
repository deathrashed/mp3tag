#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
#---------------- Soundcloud Web Source for Cover Art -----------------------#
#----------------------------------------------------------------------------#

[Name]=SoundCloud Cover Art
[BasedOn]=www.soundcloud.com
[IndexUrl]=https://soundcloud.com/search?q=%s
[AlbumUrl]=
[WordSeparator]=+
[IndexFormat]=% TITLE %|% UPLOADER %|%_URL%
[Encoding]=url-utf-8
[MinAppVersionWin]=3.33
[MinAppVersionMac]=1.8.4
[Settings]=Soundcloud#Settings.settings

#----------------------------------------------------------------------------#
#-------------------------------- I N D E X ---------------------------------#
#----------------------------------------------------------------------------#

[ParserScriptIndex]=...

findline "<!DOCTYPE html>"
findinline "<!DOCTYPE html>"
joinuntil "</html>"

#------------------------- Remove unnecessary html --------------------------#

regexpreplace "<!DOCTYPE.+People<\/a><\/li><\/ul>" ""
regexpreplace "<\/noscript><style>.+<\/html>" ""

#----------- Transform html into json format for simple parsing -------------#

regexpreplace "<ul>\s+" "["
regexpreplace "\s+<\/ul>" "\]\}"
regexpreplace "<li><h2><a href=\"" ",{\"url\":\"https://soundcloud.com"
regexpreplace "\">" "\",\"title\":\""
regexpreplace "<\/a><\/h2><\/li>\s*" "\"}"
regexpreplace "\[," "\{\"array\":\["

#----------------------------- Parse results --------------------------------#

json "ON" "current"
json_foreach "array"

# TITLE #
json_select "title"
sayrest
say "|"

# UPLOADER #
json_select "url"
SayRegexp "(?<=https:\/\/soundcloud.com\/).+(?=\/)" "" ""
say "|"

# URL #
json_select "url"
sayrest
saynewline
json_foreach_end


#----------------------------------------------------------------------------#
#---------------------------------A L B U M  (Cover Art Only) ---------------#
#----------------------------------------------------------------------------#

[ParserScriptAlbum]=...

# Use hydration script to retrieve data #
findline "<script>window.__sc_hydration ="
findinline "<script>window.__sc_hydration ="
joinuntil ";</script>"
regexpreplace "<script>window.__sc_hydration =" ""
regexpreplace ";</script>" ""
unspace

json "on" "current"

# Initialize Cover Art URL variable
set "COVERURL"

json_foreach
	json_select "hydratable"
	If "sound"
		json_select_object "data"
			outputto "COVERURL"
			json_select "artwork_url"
			If ""
				json_select_object "user"
				json_select "avatar_url"
				json_unselect_object
			EndIf
			Replace "large" "original"
			sayrest
		json_unselect_object
	EndIf

	If "playlist"
		json_select_object "data"
			outputto "COVERURL"
			json_select "artwork_url"
			If ""
				json_select_object "user"
				json_select "avatar_url"
				json_unselect_object
			EndIf
			Replace "large" "original"
			sayrest
		json_unselect_object
	EndIf
json_foreach_end
