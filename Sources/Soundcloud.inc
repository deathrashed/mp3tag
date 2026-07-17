#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
#---------------- Soundcloud Web Source by Artist & Title -------------------#
#----------------------------------------------------------------------------#

[Name]=SoundCloud
[BasedOn]=www.soundcloud.com
[IndexUrl]=https://soundcloud.com/search?q=%s
[AlbumUrl]=
[WordSeparator]=+
[IndexFormat]=% TITLE %|% UPLOADER %|%_URL%
[Encoding]=url-utf-8
[MinAppVersionWin]=3.33
[MinAppVersionMac]=1.8.4
[Settings]=Soundcloud#Settings….settings

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
#---------------------------------A L B U M ---------------------------------#
#----------------------------------------------------------------------------#

[ParserScriptAlbum]=...

#debug "on" "\debug\debug_soundcloud.txt"

# Use hydration script to retrieve data #
findline "<script>window.__sc_hydration ="
findinline "<script>window.__sc_hydration ="
joinuntil ";</script>"
regexpreplace "<script>window.__sc_hydration =" ""
regexpreplace ";</script>" ""
unspace

json "on" "current"

# Initialize variables to avoid leakage
set "COVERURL"
set "ALBUM"
set "ARTIST"
set "ALBUMARTIST"
set "GENRE"
set "COMMENT"
set "PUBLISHER"
set "COPYRIGHT"
set "WWW"
set "WWWPAYMENT"
set "SUBTITLE"
set "YEAR"
set "TRACKS"

json_foreach
	json_select "hydratable"
	If "sound"
		json_select_object "data"

			# Artwork #
			IfVar "SettingParseCoverImage" "true"
				outputto "COVERURL"
				json_select "artwork_url"
				If ""
					json_select_object "user"
					json_select "avatar_url"
					json_unselect_object
				EndIf
				Replace "large" "original"
				sayrest
			EndIf

			# Title / Album #
			IfVar "SettingParseTitle" "true"
				outputto "ALBUM"
				json_select "title"
				sayrest
			EndIf

			# Tags #
			outputto "TAGS"
			json_select "tag_list"
			RegexpReplace "(?<!\")\b([A-Za-z]+)\b(?!\")" "\"$1\""
			RegexpReplace "\s+\"" "\""
			RegexpReplace "\"\"" ", "
			RegexpReplace "\"" ""
			sayrest

			# Genre #
			IfVar "SettingGenreSource" "Genre (Top Right)"
				outputto "GENRE"
				json_select "genre"
				sayrest
			EndIf
			IfVar "SettingGenreSource" "All tags"
				outputto "GENRE"
				Use "%tags%"
				SayRest
			EndIf
			IfVar "SettingGenreSource" "First tag"
				outputto "GENRE"
				Use "%tags%"
				RegexpReplace ",.*$" ""
				SayRest
			EndIf

			# Label / Publisher #
			IfVar "SettingParseLabel" "true"
				outputto "PUBLISHER"
				json_select "label_name"
				sayrest
			EndIf

			# License #
			outputto "COPYRIGHT"
			json_select "license"
			sayrest

			# URL #
			IfVar "SettingParseUrl" "true"
				outputto "WWW"
				json_select "permalink_url"
				sayrest
			EndIf

			# Purchase URL #
			outputto "WWWPAYMENT"
			json_select "purchase_url"
			sayrest

			# Comment / Description #
			outputto "COMMENT"
			json_select "description"
			sayrest

			# Subtitle #
			outputto "SUBTITLE"
			json_select "title"
			SayRegexp "(?<=\().*\b"

			# Year #
			IfVar "SettingParseYear" "true"
				outputto "YEAR"
				json_select "release_date"
				If ""
					json_select "created_at"
				EndIf
				RegexpReplace "T.+Z" ""
				IfVar "SettingFormatYear" "YYYY"
					SayRegexp "\d\d\d\d" "" ""
				EndIf
				IfVar "SettingFormatYear" "YYYY-MM-DD"
					SayRegexp "\d\d\d\d-\d\d-\d\d" "" ""
				EndIf
				IfVar "SettingFormatYear" "DD-MM-YYYY"
					RegexpReplace "(\d\d\d\d)-(\d\d)-(\d\d)" "$3-$2-$1"
					sayrest
				EndIf
			EndIf

			# Artist of original song remixed #
			json_select_object "publisher_metadata"
				IfNot ""
					outputto "ORIGARTIST"
					json_select "artist"
					sayrest
				EndIf
			json_unselect_object

			# Artist / Username #
			json_select_object "user"
				IfVar "SettingParseArtist" "true"
					outputto "ARTIST"
					json_select "username"
					sayrest
				EndIf
				IfVar "SettingParseMixArtist" "true"
					outputto "MIXARTIST"
					json_select "username"
					Sayrest
				EndIf
				outputto "WWWARTIST"
				json_select "permalink_url"
				sayrest
			json_unselect_object

			# Track Title for Tracklist
			outputto "TRACKS"
			json_select "title"
			sayrest
			say "|"

		json_unselect_object
	EndIf

	If "playlist"
		json_select_object "data"

			# Artwork #
			IfVar "SettingParseCoverImage" "true"
				outputto "COVERURL"
				json_select "artwork_url"
				If ""
					json_select_object "user"
					json_select "avatar_url"
					json_unselect_object
				EndIf
				Replace "large" "original"
				sayrest
			EndIf

			# Album Title #
			outputto "ALBUM"
			json_select "title"
			sayrest

			# Tags #
			outputto "TAGS"
			json_select "tag_list"
			RegexpReplace "(?<!\")\b([A-Za-z]+)\b(?!\")" "\"$1\""
			RegexpReplace "\s+\"" "\""
			RegexpReplace "\"\"" ", "
			RegexpReplace "\"" ""
			sayrest

			# Genre #
			IfVar "SettingGenreSource" "Genre (Top Right)"
				outputto "GENRE"
				json_select "genre"
				sayrest
			EndIf
			IfVar "SettingGenreSource" "All tags"
				outputto "GENRE"
				Use "%tags%"
				SayRest
			EndIf
			IfVar "SettingGenreSource" "First tag"
				outputto "GENRE"
				Use "%tags%"
				RegexpReplace ",.*$" ""
				SayRest
			EndIf

			# Label / Publisher #
			IfVar "SettingParseLabel" "true"
				outputto "PUBLISHER"
				json_select "label_name"
				sayrest
			EndIf

			# License #
			outputto "COPYRIGHT"
			json_select "license"
			sayrest

			# URL #
			IfVar "SettingParseUrl" "true"
				outputto "WWW"
				json_select "permalink_url"
				sayrest
			EndIf

			# Purchase URL #
			outputto "WWWPAYMENT"
			json_select "purchase_url"
			sayrest

			# Comment / Description #
			outputto "COMMENT"
			json_select "description"
			sayrest

			# Year #
			IfVar "SettingParseYear" "true"
				outputto "YEAR"
				json_select "release_date"
				If ""
					json_select "created_at"
				EndIf
				RegexpReplace "T.+Z" ""
				IfVar "SettingFormatYear" "YYYY"
					SayRegexp "\d\d\d\d" "" ""
				EndIf
				IfVar "SettingFormatYear" "YYYY-MM-DD"
					SayRegexp "\d\d\d\d-\d\d-\d\d" "" ""
				EndIf
				IfVar "SettingFormatYear" "DD-MM-YYYY"
					RegexpReplace "(\d\d\d\d)-(\d\d)-(\d\d)" "$3-$2-$1"
					sayrest
				EndIf
			EndIf

			# Artist of original song remixed #
			json_select_object "publisher_metadata"
				IfNot ""
					outputto "ORIGARTIST"
					json_select "artist"
					sayrest
				EndIf
			json_unselect_object

			# Artist / Username #
			json_select_object "user"
				IfVar "SettingParseArtist" "true"
					outputto "ARTIST"
					json_select "username"
					sayrest
				EndIf
				IfVar "SettingParseMixArtist" "true"
					outputto "MIXARTIST"
					json_select "username"
					Sayrest
				EndIf
				outputto "WWWARTIST"
				json_select "permalink_url"
				sayrest
			json_unselect_object

			# Tracks list #
			json_select_array "tracks"
			json_foreach
				outputto "TRACKS"
				json_select "title"
				sayrest
				say "|"
			json_foreach_end
			json_unselect_object

		json_unselect_object
	EndIf
json_foreach_end
