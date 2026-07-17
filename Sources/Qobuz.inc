# Qobuz Tag Source for Mp3tag
#
# Initial release by GMK.

[MinAppVersionWin]=3.22
[MinAppVersionMac]=1.8.6
[Settings]=&Qobuz#Settings….settings
[BasedOn]=qobuz.com
[WordSeparator]=%20
#[SearchBy]=$if($eql(%albumartist%,'Various Artists'),$regexp(%album%,'\s+\[.+\]$',,1),$regexp(%albumartist%,'\s+\[.+\]$',,1))
[SearchBy]=%albumartist% %album%
[Encoding]=url-utf-8
[IndexFormat]=%type%|%_url%|%_coverurl%|%Album%|%Artist%|%Date%|%Tracks%|%Label%
[Version]=26.07.02

[ParserScriptIndex]=...
# ###################################################################
#					I  N  D  E  X
# ###################################################################

#DebugWriteInput "%userprofile%\Desktop\Logs\MP3Tag-debug_Qobuz_INDEX_input.log"
#Debug "on" "%userprofile%\Desktop\Logs\MP3Tag-debug_Qobuz_INDEX.log"

FindLine "data-live-props-value=\""
Unspace
RegExpReplace ".*data-live-props-value=\"(.*)\".*" "$1"
Replace "&quot;" "\""
RegExpReplace ".*?\"albums\":\"(\{.*?\})\".*" "\[$1\]"
Replace "{\\\"" "{\""
Replace "\\\":" "\":"
Replace ":\\\"" ":\""
Replace "\\\"," "\","
Replace ",\\\"" ",\""
Replace "\\\\\\" ""
Replace "\\\"}" "\"}"
RegExpReplace "\"(.*?)\"\:(\{\"id\"\:\"\1\",)" "$2"
Replace "{{" "{"
Replace "}}]" "}]"


json "on" "current"
json_select_array "" -1 ""
json_foreach ""

    # Type
    Say "Album|"

    # URL
    json_select "slug"
    SayRest
    Say "/"
    json_select "id"
    SayRest
    Say "|"

    # Thumbnail
    json_select_object "image"
    json_select "small"
    SayRest
    json_unselect_object
    Say "|"

    # Album
    json_select "title"
    SayRest
    Say "|"

    # Artist
    json_select_many "artists" "name" ", "
    SayRest
    Say "|"

    # Date
    json_select "releasedAt"
    SayDate
    Say "|"

    # Tracks
    json_select "tracksCount"
    SayRest
    Say "|"

    # Label
    json_select_object "label"
    json_select "name"
    SayRest
    json_unselect_object

    SayNewLine
json_foreach_end
json "off"


[ParserScriptAlbum]=...
# ###################################################################
#					A  L  B  U  M
# ###################################################################

#DebugWriteInput "%userprofile%\Desktop\Logs\MP3Tag-debug_Qobuz_ALBUM_input.log"
#Debug "on" "%userprofile%\Desktop\Logs\MP3Tag-debug_Qobuz_ALBUM.log"

# QOBUZ_URL
OutputTo "QOBUZ_URL"
SayOutput "currentURL"

FindLine "<script type=\"application/ld+json\">"
JoinUntil "</script>"
KillTag "script"
KillTag "/script"
Replace "\\/" "/"
Unspace

json "on" "current"

# Album Artist
json_select_object "brand"
	OutputTo "ALBUMARTIST"
	json_select "name"
	If "Various Artists"
		Set "COMPILATION" "1"
	EndIf
	SayRest
json_unselect_object

# Cover Art
OutputTo "COVERURL"
json_select_array "image" 3
SayRest

# Release Date
OutputTo "YEAR"
json_select "releaseDate"
RegexpReplace "(\d{4})-01-01" "$1"
IfVar "yearFormat" "YYYY"
	RegexpReplace "(\d{4})-\d{2}-\d{2}" "$1"
EndIf
Unspace
SayRest

json "off"

GotoLine 1

# Album
FindLine "<span class=\"album-title\">"
Unspace
FindInLine "<span class=\"album-title\">"
OutputTo "ALBUM"
SayUntil "<"

# Genre
FindLine "<li class=\"album-meta__item\">" 3
JoinUntil "</li>"
Unspace
FindInLine "<a class"
FindInLine ">"
OutputTo "GENRE"
SayUntil "<"
GotoLine 1

# Total Discs & Total Tracks
FindLine "<section class=\"album-about\" id=\"about\">"
JoinUntil "</section>"
Unspace
Replace "組み枚数 : " ""
FindInLine "<li class=\"album-about__item\">"
IfGreater 1
	OutputTo "TEMP_TotalDiscs"
	Say "/"
	SayRegexp "\d+\s?(?=[Dd]isco?|disque|ディスク.*)"
	Set "TEMP_TotalTracks"
Else
	OutputTo "TEMP_TotalDiscs"
	Say "/"
	SayRegexp "\d+\s?(?=[Dd]isco?|disque|ディスク.*)"
	OutputTo "TEMP_TotalTracks"
	Say "/"
	SayRegexp "\d+ (?=faixa|[Tt]rack|pist[ae]|traccia)"
EndIf

# Copyright
FindInLine "<p class=\"album-about__copyright\">"
Replace "(C)" "©"
Replace "(P)" "℗"
OutputTo "TEMP_AlbumPublisher"
RegexpReplace "(©\s+)?(\d{4})\s+(.*?)\s+(℗\s+)?\2\s+\3" "© & ℗ $2 $3"
RegexpReplace "(?<=>)(\d{4})" "© $1"
SayRegexp "(?<=℗\s\d{4}\s).*?(?=<)"
RegexpReplace "((?:\w+)(?: \w+)+?)(?: \1)+" "© & ℗ $1"
FindInLine "<p class=\"album-about__copyright\">"
OutputTo "COPYRIGHT"
SayUntil "<"
GotoLine 1

# Tracklist
FindLine "<div class=\"player__item\">"
Unspace

Do
	OutputTo "TRACKS"
	Say "|"

	JoinUntil "</div>"
	Unspace
	KillTag "div"
	KillTag "/div"
	Unspace
	RegexpReplace ".*(?:Disc|DISC|DISCO|DISQUE)\s+(\d+).*" "$1"
	KillTag "p"
	KillTag "/p"
	If ""
		IfNotOutput "TEMP_DiscNumber"
			Set "TEMP_DiscNumber" "1"
		EndIf
	Else
		Set "TEMP_DiscNumber"
		OutputTo "TEMP_DiscNumber"
		SayRest
	EndIf
	MoveLine -1

	# Track
	FindLine "<div class=\"track__item track__item--number\">"
	JoinUntil "</div>"
	OutputTo "TRACK"
	SayRegexp "(?<=span>)\d+"
	IfOutput "TEMP_TotalTracks"
		SayOutput "TEMP_TotalTracks"
	EndIf
	Say "|"
	MoveLine -6

	FindLine "data-track-v2"
	RegexpReplace ".*data-track-v2=\"([^\"]+)\".*" "$1"
	Replace "&quot;" "\""
	json "on" "current"

	# Artist
	OutputTo "TEMP_Artist"
	json_select "item_brand"
	SayRest

	# Label
	OutputTo "LABEL"
	json_select "item_category2"
	SayRest
	Say "|"
	json "off"

	# Featuring
	FindLine "<div class=\"track__items\""
	OutputTo "TEMP_Featured"
	Replace "[" "("
	Replace "]" ")"
	SayRegexp "(?<=\([Ff]eat\. )[^\)]+"

	#Title
	OutputTo "TITLE"
	IfOutput "TEMP_Featured"
		Replace "[" "("
		Replace "]" ")"
		RegexpReplace "(.*?)(\s\([Ff]eat.[^\)]+\))" "$1"
	EndIf
	RegexpReplace "(\s)+" "$1"
	RegexpReplace "([\(\)])+" "$1"
	SayRegexp "(?<=title=\")[^\"]+"
	Say "|"

	# Length
	FindLine "<span class=\"track__item track__item--duration\">"
	JoinUntil "</span>"
	OutputTo "_LENGTH"
	SayRegexp "(?<=<span class=\"track__item track__item--duration\">)[^<]+"
	Say "|"

	# DiscNumber
	OutputTo "DISCNUMBER"
	SayOutput "TEMP_DiscNumber"
	SayOutput "TEMP_TotalDiscs"
	Say "|"

	# Credits
	MoveLine 2
	Unspace
	If "<div class=\"track__infos\">"
		FindLine "<p class=\"track__info\">" 1
		JoinUntil "</p>"
		RegexpReplace "Not Applicable[^-]+\s-\s" ""
		RegexpReplace "Unknown[^-]+\s-\s" ""
		RegexpReplace "Various Artists[^-]+\s-\s" ""
		OutputTo "CREDITS"
		SayRegexp "(?<=p class=\"track__info\">)[^<]+" "" "</p>"
		Say "|"

		UnSpace
		Replace "Performer" "MainArtist"
		KillTag "p"
		KillTag "/p"
		Replace " - " " | "
		RegexpReplace ", (?!MainArtist)[^,|]+" ""
		OutputTo "TEMP_MainArtist"
		SayRegExp "[^\|]+(?=, MainArtist)" ", "

		OutputTo "ARTIST"
		IfOutput "TEMP_MainArtist"
			SayOutput "TEMP_MainArtist"
		Else
			IfNotOutput "COMPILATION"
				SayOutput "TEMP_Artist"
			EndIf
		EndIf

		# Featured
		IfNotOutput "TEMP_Featured"
			MoveLine -1
			MoveLine 1
			UnSpace
			RegexpReplace "Not Applicable[^-]+\s-\s" ""
			RegexpReplace "Unknown[^-]+\s-\s" ""
			RegexpReplace "Various Artists[^-]+\s-\s" ""
			KillTag "p"
			KillTag "/p"
			Replace " - " " | "
			RegexpReplace ", (?!FeaturedArtist)[^,|]+" ""
			OutputTo "TEMP_Featured"
			SayRegexp "[^\|]+(?=, FeaturedArtist)" ", "
		EndIf
		OutputTo "ARTIST"
		IfOutput "TEMP_Featured"
			# Add parentheses and change spelling/abbrev as desired
			IfOutput "TEMP_MainArtist"
				Say " (feat. "
			EndIf
			SayOutput "TEMP_Featured"
			IfOutput "TEMP_MainArtist"
				Say ")"
			EndIf
		EndIf
		Say "|"

		Set "TEMP_MainArtist"
		Set "TEMP_Artist"
		Set "TEMP_Featured"

		# Composer
		MoveLine -1
		MoveLine 1
		UnSpace
		RegexpReplace "Not Applicable[^-]+\s-\s" ""
		RegexpReplace "Unknown[^-]+\s-\s" ""
		RegexpReplace "Various Artists[^-]+\s-\s" ""
		KillTag "p"
		KillTag "/p"
		Replace " - " " | "

		# Trying to remove spaces from all credit roles
		RegexpReplace "(\s[^,]+)\s(Arranger)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Artist)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Bass)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Controller)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Effects)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Engineer)" "$1$2"
        Replace "12-String Acoustic Guitar" "12-StringAcousticGuitar"
		RegexpReplace "(\s[^,]+)\s(Guitar)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Performer)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Personnel)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Producer)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Production)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Programmer)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Programming)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Saxophone)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Vocal)" "$1$2"
        RegexpReplace "(\s[^,]+)\s(Vocalist)" "$1$2"
		RegexpReplace "(\s[^,]+)\s(Vocals)" "$1$2"
		RegexpReplace "Author|Songwriter|Writer" "Composer"
		Replace "ComposerLyricist" "Composer"
		RegexpReplace ", (?!Composer|\w+\s\w+)[^,|]+" "" # Remove all but Composer credits
		RegexpReplace "(, Composer)+" "$1" # Remove duplicate Composer credits
		OutputTo "COMPOSER"
		SayRegexp "[^\|]+(?=, Composer)" ", "
		Say "|"

		# Lyricist
		MoveLine -1
		MoveLine 1
		UnSpace
		RegexpReplace "Not Applicable[^-]+\s-\s" ""
		RegexpReplace "Unknown[^-]+\s-\s" ""
		RegexpReplace "Various Artists[^-]+\s-\s" ""
		RegexpReplace "<p class=\"track__info\">([^<]+)</p>" "$1"
		Replace " - " " | "
		Replace "ComposerLyricist" "Lyricist"
		RegexpReplace ", (?!Lyricist)[^,|]+" "" # Remove all but Lyricist credits
		RegexpReplace "(, Lyricist)+" "$1" # Remove duplicate Lyricist credits
		OutputTo "LYRICIST"
		SayRegexp "[^\|]+(?=, Lyricist)" ", "
		Say "|"

		# Publisher
		MoveLine -1
		MoveLine 1
		UnSpace
		RegexpReplace "Not Applicable[^-]+\s-\s" ""
		RegexpReplace "Unknown[^-]+\s-\s" ""
		RegexpReplace "Various Artists[^-]+\s-\s" ""
		KillTag "p"
		KillTag "/p"
		Replace " - " " | "
		RegexpReplace ", (?!MusicPublisher)[^,|]+" ""
		RegexpReplace "(, MusicPublisher)+" "$1"
		OutputTo "TEMP_Publisher"
		SayRegexp "[^\|]+(?=, MusicPublisher)" " / "
		OutputTo "PUBLISHER"
		IfOutput "TEMP_Publisher"
			SayOutput "TEMP_Publisher"
			Set "TEMP_Publisher"
		Else
			SayOutput "TEMP_AlbumPublisher"
		EndIf
		Say "|"
		Set "TEMP_Publisher"
	Else
		# Credits
		OutputTo "CREDITS"
		Say "|"

		# Artist
		OutputTo "ARTIST"
		SayOutput "TEMP_Artist"
		IfOutput "TEMP_Featured"
			# Add parentheses and change spelling/abbrev as desired
			Say " (feat. "
			SayOutput "TEMP_Featured"
			Say ")"
		EndIf
		Say "|"
		Set "TEMP_Artist"
		Set "TEMP_Featured"

		# Composer
		OutputTo "COMPOSER"
		Say "|"

		# Lyricist
		OutputTo "LYRICIST"
		Say "|"

		# Publisher
		OutputTo "PUBLISHER"
		SayOutput "TEMP_AlbumPublisher"
		Say "|"
	EndIf

	# Loop
	FindLine "<div class=\"player__item\">" 1 1
	Unspace

While "<div class=\"player__item\">" 200

Set "TEMP_DiscNumber"
Set "TEMP_TotalDiscs"
Set "TEMP_TotalTracks"
Set "TEMP_AlbumPublisher"
Set "TEMP_Artist"
