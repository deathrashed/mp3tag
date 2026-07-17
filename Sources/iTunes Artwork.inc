# iTunes API 2.1 - Cover Art Only
# © 2021-2025 All Rights Reserved
[Name]=iTunes Cover Art
[BasedOn]=https://itunes.apple.com/
[WordSeparator]=+
[Encoding]=url-utf-8
[IndexFormat]=%_url%|%_preview%|%_coverurl%|%Title%|%Artist%|%Tracks%|%Kind%|%Explicit%|%Released%|%Genre%|%Copyright%|%Notes%

[ParserScriptIndex]=...

json "on"

json_foreach "results"
    json_select "wrapperType"
    If "collection"
        json_select "collectionType"
        If "Album"
            json_select "collectionId"
            SayNextNumber
            Say "|"
            json_select "collectionViewUrl"
            Replace "?uo=4" ""
            Replace "&uo=4" ""
            SayRest
            Say "|"
            json_select "artworkUrl100"
            SayRest
            Say "|"
            json_select "collectionName"
            If ""
                json_select "collectionCensoredName"
            EndIf
            OutputTo "TEMP"
            SayRegexp "\s-\sSingle"
            IfOutput "TEMP"
                Set "KIND" "Single"
                Set "TEMP"
            EndIf
            SayRegexp "\s-\sEP"
            IfOutput "TEMP"
                Set "KIND" "EP"
                Set "TEMP"
            EndIf
            OutputTo "Output"
            Replace " - Single" ""
            Replace " - EP" ""
            RegexpReplace "\[.*\]" ""
            RegexpReplace "\{.*\}" ""
            SayRest
            Say "|"
            json_select "artistName"
            SayRest
            Say "|"
            json_select "trackCount"
            SayNextNumber
            Say "|"
            json_select "collectionType"
            IfOutput "KIND"
                SayOutput "KIND"
                Set "KIND"
            Else
                SayRest
            EndIf
            Say "|"
            json_select "collectionExplicitness"
            Replace "notExplicit" "No"
            Replace "explicit" "Yes"
            Replace "cleaned" "Cleaned"
            SayRest
            Say "|"
            json_select "releaseDate"
            SayNChars 10
            Say "|"
            json_select "primaryGenreName"
            SayRest
            Say "|"
            json_select "copyright"
            SayRest
            Say "|"
            json_select "collectionName"
            SayRegexp "(?<=\()[^)]*(?=\))"
            Say " "
            SayRegexp "(?<=\[)[^)]*(?=\])"
            Say " "
            SayRegexp "(?<=\{)[^}]*(?=\})"
            SayNewline
        EndIf
    EndIf
json_foreach_end

json "off"

[ParserScriptAlbum]=...

json "on"

json_foreach "results"
    json_select "wrapperType"
    If "collection"
        json_select "collectionType"
        If "Album"
            OutputTo "COVERURL"
            json_select "artworkUrl100"
            # Hardcode maximum original quality artwork retrieval
            Replace "://is" "://a"
            Replace "-ssl.mzstatic.com/image/thumb/" ".mzstatic.com/us/r1000/0/"
            RegexpReplace "(.*)\/.*" "$1"
            SayRest
        EndIf
    EndIf
json_foreach_end

json "off"
