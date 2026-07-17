##############################################################################
#
# WebSourceScript for Mp3tag, fetching Metadata from MusicBrainz.org
# Version v2.00
#
# This file will be called by a *.src file. It does not run independently.
#
##############################################################################
# This *.inc file together with all the linked *.src files must be placed
# in your Mp3tag sources directory, on Windows 10 found in this folder:
# %appdata%\Mp3tag\data\sources
# Since Mp3tag v3.12 you can also open the configuration folder via
# File -> Open configuration folder, then navigate to data\sources
# and there extract the downloaded Tag Source file (.src)
#
# History:
# --------
#
# 2022-01-15    v1.00
# 2022-01-25    v1.01   + CHG: [Name] to MusicBrainz
#                       + FIX: Only fill metadata to matching number of tracks
#                       + CHG: Comment tag will not be written anymore
#
# 2022-04-08    v1.20   + ADD: Performing Orchestra with Begin- & End-Date
#                       + FIX: Trim "off" added for INDEX-part too
#
# 2024-05-08    v1.30   + NEW: Showing cover art thumbnail in the search query result overview
#                              This feature was introduced with Mp3tag 3.25c
#
# 2024-06-01    v2.00   Rewritten from scratch
#                       + NEW: pregap-Track (aka "hidden Track") will be listed too
#                       + NEW: Some more release level metadata added like producer
#                       ATTENTION:
#                       + DEL: Removed the Performing Orchestra with Begin- & End-Date
#                              and all other track-level informations that are filled
#                              into INVOLVEDPEOPLE.
#                              Maybe I will find some time to write an additional
#                              WSS-Script "MusicBrainz involved"...
#
# Special thanks to @Florian and @ohrenkino and @Casual_Tea for the support
# and tests of the preview releases
#
##############################################################################

[Name]=MusicBrainz
[BasedOn]=musicbrainz.org
[IndexUrl]=https://musicbrainz.org/ws/2/release/?fmt=json&limit=50&query=
[AlbumUrl]=https://musicbrainz.org/ws/2/release/
[WordSeparator]=%20
[WordSeparator]=%20
[IndexFormat]=%_preview%|%_coverurl%|%_url%|%Score%|%Type%|%Albumname%|%Artistname(s)%|%No of Media%|%Format%|%Total Tracks%|%Country%|%Date%|%Catalog No%|%Label/Publisher%|%ASIN%|%Barcode%|%Status%|
#[SearchBy]=will be provided by parent *.src file
[UserAgent]=1
[Encoding]=url-utf-8
[Settings]=MusicBrainz Expanded#Settings….settings
[MinAppVersionWin]=3.25c

[ParserScriptIndex]=...
####################################################################
#                           I  N  D  E  X
####################################################################
#
# This part is building the selection of possibly matching releases.
#
# The medata for the manually selected release will then be fetched
# in a second call from the MusicBrainz webservice server.
#
####################################################################

replace "|" "$verticalBar()"
json "ON" "current"

# Trim was introduced with Mp3tag v3.11h
# Using it before will crash this index parsing part
Trim "off"

# Only proceed if there is any result
json_select_object "count"
    json_select "count"

    ifnot "0"

    json_foreach "releases"

        # Change to releases level
        json_select_object "releases"

            # Preview (no column, only for online preview in Browser)
            say "http://musicbrainz.org/release/"
            json_select "id"
                sayrest
            say "|"

            # Get Cover Art Thumbnails for preview in 'List of search results', if available at the CoverArtArchive
            # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
            # Content of settings.json will be written from "Settings" context-entry of this WSS
            IfVar "b_Download_CoverThumbnail" "true"
                say "https://coverartarchive.org/release/"
                json_select "id"
                    sayrest
                    say "/front-250"
            endif
            say "|"

            # URL (no column, only for preview)
            json_select "id"
                sayrest
                say "?inc=artists+artist-credits+isrcs+labels+release-groups+recordings+recording-level-rels+area-rels+place-rels+artist-rels"
                say "&fmt=json"
                say "|"

            # Column: Score
            json_select "score"
                sayrest
                say "|"

            # Column: Type
            # Change to release-group level
            json_select_object "release-group"
                json_foreach "release-group"
                    json_select "primary-type"
                        sayrest
                json_foreach_end
            json_unselect_object
            #json_unselect_object "release-group"
                say "|"

            # Column: Albumtitle
            json_select "title"
                sayrest
                say "|"

        json_unselect_object
        #json_unselect_object "releases"


        # Artist credit
        # Change to artist-credit level
        json_select_object "artist-credit"
            set "artist"
            json_foreach "artist-credit"
                json_select "name"
                    sayrest
                json_select "joinphrase"
                ifnot ""
                    sayrest
                endif
            json_foreach_end
            #json_foreach_end "artist-credit"

        json_unselect_object
        #json_unselect_object "artist-credit"

        # Add complete content to Column: Artistname(s)
        sayoutput "name"
        say "|"

        # Column: (# of Media)
        json_select "count"
            IfGreater 1
                set "TEMP_MultipleMedia" "y"
            else
                set "TEMP_MultipleMedia"
            endif
            sayrest
            say "|"

        # Format
        # Change to media level
        json_select_object "media"
            json_foreach "media"
                json_select "format"
                    sayrest
                json_select "track-count"
                ifnot ""
                    ifOutput "TEMP_MultipleMedia"
                        say " ("
                        sayrest
                        say ") "
                    endif
                endif
            json_foreach_end
        json_unselect_object
        #json_unselect_object "media"
        say "|"

        # Change back to releases level
        json_select_object "releases"

            # Column: Total Tracks
            json_select "track-count"
            sayrest
            say "|"

            # Column: Country
            json_select "country"
            sayrest
            say "|"

            # Column: Date
            json_select "date"
            sayrest
            say "|"

        json_unselect_object
        #json_unselect_object "releases"

        # label-info
        json_select_array "label-info" 1

            # Column: Catalog-No
            json_select "catalog-number"
                sayrest
                say "|"

            # Column: Label / Publisher
            json_select "label"
            json_select "name"
                sayrest
                say "|"

        #json_unselect_object
        #json_unselect_object "label-info"

        json_select_object "releases"
            # Column: Asin
            json_select "asin"
            sayrest
            say "|"

            # Column: Barcode
            json_select "barcode"
            sayrest
            say "|"

            # Column: Status
            json_select "status"
            sayrest
            say "|"

        json_unselect_object
        #json_unselect_object "releases"

        saynewline

    json_foreach_end
    #json_foreach_end "releases"

    # Delete temporary variables, don't show them
    set "TEMP_MultipleMedia"

    endif
    # endif ifnot "0"

json_unselect_object
#json_unselect_object "count"

json "OFF"


[ParserScriptAlbum]=...
####################################################################
#                           A  L  B  U  M
####################################################################

# Necessary for special names like "M|A|R|S|S|"
replace "|" "$verticalBar()"

json "ON" "current"

# Trim was introduced with Mp3tag v3.11h
# Using it before will crash this album parsing part
# Trim	S	Enables or disables default auto-trimming of whitespace characters, S= "on" or "off"
Trim "off"

# Goes to "Adjust tag information window", Panel top right "Metadata Album"
# Reflects metadata valid for the entire album (and therefore for all tracks)
# Mp3tag converts all Tag names to UPPERCASE

#########################
# Root-Level of Release #
#########################

# In MB Picard shown as "Album"
outputto "Album"
json_select "title"
    sayrest

# In MB Picard shown as "ASIN"
outputto "ASIN"
json_select "asin"
    sayrest

# In MB Picard shown as "Barcode"
outputto "BARCODE"                                   # Important: UPPERCASE for MB Picard Compatibility
json_select "barcode"
    sayrest

# In MB Picard shown as "Disambiguation"
outputto "Disambiguation"
json_select "disambiguation"
    sayrest

# In MB Picard shown as "MusicBrainz Release Id"
outputto "MUSICBRAINZ_ALBUMID"
json_select "id"
    sayrest

# In MB Picard shown as "Release Status"
outputto "MUSICBRAINZ_ALBUMSTATUS"                   # Example: Official or Album (MB Picard shows: official or album)
json_select "status"
# Settings read from file settings.json in subdirectory \data\sources of Mp3tag
# Content of settings.json will be written from "Settings" context-entry of this WSS
IfVar "b_Convert_Status_and_PrimaryType" "true"
    RegexpReplace "^(.*)$" "\L$1"
    SayRegexp "^.*$"                                 # MB Picard shows lowercase: ep
else
    sayrest                                          # Example: EP - Content remains untouched and not converted to lowercase as in MB Picard
endif

# In MB Picard shown as "Release Country"
outputto "MUSICBRAINZ_ALBUMRELEASECOUNTRY"
json_select "country"
# regexpreplace "^GB$" "UK"                          # No manipulation of the source metadata, can be replaced by user if necessary
    sayrest

# In MB Picard shown as "Quality"
outputto "Quality"
json_select "quality"
    sayrest

# In MB Picard shown as YYYY-MM-DD "Date"
outputto "Year"
json_select "date"
    saynchars 4

# In MB Picard shown as "Date"
# Strange MB Picard format, creates 1503 DDMM from date 2024-03-15 and show it together with "Year" YYYY
# In Mp3tag it is shown as DATE with 1503 and YEAR with 2024
outputto "Date"
json_select "date"
    findinline "-" 1 1
    ifnot ""
        # Search for     YYYY     MM      DD      Output it as DDMM
        RegexpReplace "^(\d{4})-(\d{2})-(\d{2})$" "$3$2"
        SayRegexp "^.*$"
    endif

################################
# Object "text-representation" #
################################

# In MB Picard shown as "Script"
json_select_object "text-representation"
    json_select "text-representation"
        outputto "SCRIPT"                   # Important: UPPERCASE for MB Picard Compatibility
        json_select "script"
            sayrest

        outputto "Language"
        json_select "language"
            sayrest
json_unselect_object
#json_unselect_object "text-representation"


##############################
# Object "cover-art-archive" #
##############################

# Settings read from file settings.json in subdirectory \data\sources of Mp3tag
# Content of settings.json will be written from "Settings" context-entry of this WSS

# Get Cover Art, if available at the CoverArtArchive
# Goes to "Adjust tag information window", Panel top right "Cover"
# If you never want to download a Cover from an online source, then activate the last line 'set "coverurl"' in this WSS-Script
IfVar "b_Download_CoverAlbumArt" "true"
    json_select_object "cover-art-archive"
        json_select "count"
            # If "NEVER-EVER"     # Debug only, much faster without CoverArt Download
            IfNot "0"
                # Cover via CoverArtArchive (CAA)
                outputto "coverurl"
                say "http://coverartarchive.org/release/"
                sayoutput "MUSICBRAINZ_ALBUMID"

                # Since Mp3tag v3.11h we can configure one of the 4 available "MusicBrainz Cover Size"
                # in Tools -> Options -> Tag Sources:
                # 250 Pixels, 500 Pixels, 1200 Pixels or the Original size
                # An Original size 7000 Pixel Cover with 50MB needs up to 60 seconds to download
                say "/front"
            else
               # Cover via ASIN
               # If "NEVER-EVER"     # Debug only, much faster without CoverArt Download
               ifOutput "ASIN"
                   outputto "coverurl"
                   say "http://images.amazon.com/images/P/"
                   sayoutput "ASIN"
                   say ".01.LZZZZZZZ.jpg"
               endif
            endif
            # endif "ifNot 0"

    json_unselect_object
    #json_unselect_object "cover-art-archive"
endif
#IfVar "b_Download_CoverAlbumArt" "true"


#######################
# Object "label-info" #
#######################

# Goes to "Adjust tag information window", Panel top right "Metadata Album"
json_select_object "label-info"

    # In MB Picard shown as "Catalog Number"
    outputto "CATALOGNUMBER"
    json_select_many "label-info" "catalog-number" "/"
            sayrest

    # In MB Picard shown as "Record Label"
    outputto "Publisher"
    json_foreach "label-info"
        json_select "label"

            json_select "name"
                ifOutput "Publisher"
                    say "/"
                endif
                sayrest

            # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
            # Content of settings.json will be written from "Settings" context-entry of this WSS
            IfVar "b_Show_MB_Nonstandard_Tags" "true"
                json_select "sort-name"         # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_Sortname"
                    sayrest

                json_select "disambiguation"    # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_Disambiguation"
                    sayrest

                json_select "id"                # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_ID"
                    sayrest

                json_select "label-code"        # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_Labelcode"
                    sayrest

                json_select "type"              # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_Type"
                    sayrest

                json_select "type-id"           # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_LabelInfo_Publisher_Type_ID"
                    sayrest
            endif
            # IfVar "b_Show_MB_Nonstandard_Tags" "true"

    json_foreach_end
    #json_foreach_end "label-info"

json_unselect_object
#json_unselect_object "label-info"


##########################
# Object "release-group" #
##########################

# Goes to "Adjust tag information window", Panel top right "Metadata Album"
json_select_object "release-group"

    # In MB Picard shown as "MusicBrainz Release Group Id"
    outputto "MUSICBRAINZ_RELEASEGROUPID"
    json_select "id"
        sayrest

    # In MB Picard shown as "Release Type"
    outputto "MUSICBRAINZ_ALBUMTYPE"                # Example: Album (MB Picard shows lowercase: album)
    json_select "primary-type"                      # Remains untouched and not converted to lower case as in MB Picard

    # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
    # Content of settings.json will be written from "Settings" context-entry of this WSS
    IfVar "b_Convert_Status_and_PrimaryType" "true" # MB Picard shows lowercase: album
        RegexpReplace "^(.*)$" "\L$1"               # Convert "Album" to "album"
        SayRegexp "^.*$"
    else
        sayrest
    endif

    json_select_array "secondary-types" -1 "/"      # Remains untouched and not converted to lower case as in MB Picard
    ifNot ""
        say "/"

        # MB Picard set it to 1 only if AlbumArtist is "Various Artists", as on "Bravo Hits"
        # This WSS set it always if secondary-types contains "Compilation",
        # as the COMPILATION tag can be deactivated easily in the Panel top right "Metadata Album"
        if "Compilation"                            # case-sensitive
        outputto "COMPILATION"
            say "1"
        endif

        outputto "MUSICBRAINZ_ALBUMTYPE"
        IfVar "b_Convert_Status_and_PrimaryType" "true"  # MB Picard shows lowercase: compilation
            RegexpReplace "^(.*)$" "\L$1"           # Convert "Compilation" to "compilation"
            SayRegexp "^.*$"
        else
            sayrest
        endif
    endif

    # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
    # Content of settings.json will be written from "Settings" context-entry of this WSS
    IfVar "b_Show_MB_Nonstandard_Tags" "true"

        outputto "MB_Releasegroup_Title"                # ATTENTION: This value is NOT available in MB Picard
        json_select "title"
            sayrest

        outputto "MB_Releasegroup_Disambiguation"       # ATTENTION: This value is NOT available in MB Picard
        json_select "disambiguation"
            sayrest

        outputto "MB_Releasegroup_PrimaryType_ID"       # ATTENTION: This value is NOT available in MB Picard
        json_select "primary-type-id"
            sayrest

        outputto "MB_Releasegroup_FirstRelease_Date"    # ATTENTION: This value is NOT available in MB Picard
        json_select "first-release-date"
            sayrest
    endif
    #IfVar "b_Show_MB_Nonstandard_Tags" "true"


    # In MB Picard shown as "Original Release Date"
    outputto "ORIGYEAR"
    json_select "first-release-date"
        saynchars 4

    # In MB Picard shown as "Original Year"
    outputto "originalyear"
        sayoutput "ORIGYEAR"

    # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
    # Content of settings.json will be written from "Settings" context-entry of this WSS
    IfVar "b_Show_MB_Nonstandard_Tags" "true"

        json_select_object "artist-credit"
            json_foreach "artist-credit"
                outputto "MB_Releasegroup_ArtistCredit_Name"                # ATTENTION: This value is NOT available in MB Picard
                json_select "name"
                    IfOutput "MB_Releasegroup_ArtistCredit_Name"
                        IfNot ""
                            say "/"     # add a slash if current content is not empty and a new ArtistCredit-Name will be added
                        endif
                    endif
                    sayrest

                outputto "MB_Releasegroup_ArtistCredit_Joinphrase"          # ATTENTION: This value is NOT available in MB Picard
                json_select "joinphrase"
                    sayrest

                    json_select "artist"
                    json_foreach "artist"
                        outputto "MB_Releasegroup_ArtistCredit_Artist_ID"               # ATTENTION: This value is NOT available in MB Picard
                        json_select "id"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_ID"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistID will be added
                                endif
                            endif
                            sayrest

                        outputto "MB_Releasegroup_ArtistCredit_Artist_Name"             # ATTENTION: This value is NOT available in MB Picard
                        json_select "name"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_Name"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistName will be added
                                endif
                            endif
                            sayrest

                        outputto "MB_Releasegroup_ArtistCredit_Artist_SortName"         # ATTENTION: This value is NOT available in MB Picard
                        json_select "sort-name"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_SortName"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistSortname will be added
                                endif
                            endif
                            sayrest

                        outputto "MB_Releasegroup_ArtistCredit_Artist_Disambiguation"   # ATTENTION: This value is NOT available in MB Picard
                        json_select "disambiguation"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_Disambiguation"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new disambiguation will be added
                                endif
                            endif
                            sayrest

                        outputto "MB_Releasegroup_ArtistCredit_Artist_Type"             # ATTENTION: This value is NOT available in MB Picard
                        json_select "type"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_Type"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistType will be added
                                endif
                            endif
                            sayrest

                        outputto "MB_Releasegroup_ArtistCredit_Artist_Type_ID"          # ATTENTION: This value is NOT available in MB Picard
                        json_select "type-id"
                            IfOutput "MB_Releasegroup_ArtistCredit_Artist_Type_ID"
                                IfNot ""
                                    say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistTypeID will be added
                                endif
                            endif
                            sayrest
                    json_foreach_end
                    #json_foreach_end "artist"

            json_foreach_end
            #json_foreach_end "artist-credit"

        json_unselect_object
        #json_unselect_object  "artist-credit"

    endif
    # IfVar "b_Show_MB_Nonstandard_Tags" "true"

json_unselect_object
#json_unselect_object "release-group"


##########################
# Object "artist-credit" #
##########################

# Goes to "Adjust tag information window", Panel top right "Metadata Album"
# This is the Artist Credit on the Release-Level
json_select_object "artist-credit"
    json_foreach "artist-credit"

        # In MB Picard shown as "Album Artist"
        outputto "ALBUMARTIST"
        json_select "name"
            sayrest

        json_select "joinphrase"
        ifnot ""
            sayrest
            GotoChar 1
            outputto "TEMP_MB_JOINPHRASE"
                sayrest
        else
            set "TEMP_MB_JOINPHRASE"
        endif
        # ifnot ""


        # Fill artist-credit -> artist -> sortname
        # In MB Picard shown as "Album Artist Sort Order"
        json_select "artist"
            json_select "sort-name"
            outputto "Albumartistsort"
                sayrest
                sayoutput "TEMP_MB_JOINPHRASE"

            # In MB Picard shown as "MusicBrainz Release Artist Id"
            json_select "id"
            outputto "MUSICBRAINZ_ALBUMARTISTID"
                sayrest
            ifOutput "TEMP_MB_JOINPHRASE"
                say "/"
            endif

            # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
            # Content of settings.json will be written from "Settings" context-entry of this WSS
            IfVar "b_Show_MB_Nonstandard_Tags" "true"
                json_select "type"
                outputto "MB_ArtistCredit_Artist_Type"
                    IfOutput "MB_ArtistCredit_Artist_Type"
                        IfNot ""
                            say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistType will be added
                        endif
                    endif
                    sayrest

                json_select "type-id"
                outputto "MB_ArtistCredit_Artist_Type_ID"
                    IfOutput "MB_ArtistCredit_Artist_Type_ID"
                        IfNot ""
                            say "/"     # add a slash if current content is not empty and a new ArtistCredit-ArtistTypeID will be added
                        endif
                    endif
                    sayrest

                json_select "disambiguation"
                outputto "MB_ArtistCredit_Artist_Disambiguation"
                    IfOutput "MB_ArtistCredit_Artist_Disambiguation"
                        IfNot ""
                            say "/"     # add a slash if current content is not empty and a new ArtistCredit-Disambiguation will be added
                        endif
                    endif
                    sayrest
            endif
            # IfVar "b_Show_MB_Nonstandard_Tags" "true"

        # Immediately clear this temporary variable
        set "TEMP_MB_JOINPHRASE"

    json_foreach_end
    #json_foreach_end "artist-credit"

json_unselect_object
#json_unselect_object "artist-credit"



######################
# Object "relations" #
# on Release level   #
######################

# Goes to "Adjust tag information window", Panel top right "Metadata Album"
# This is only useful to fill the INVOLVEDPEOPLE tag with release level "producer"
# and optional "printed in".
# This does NOT need +work-rels+work-level-rels in the JSON-Get-URL
json_select_object "relations"
    json_foreach "relations"
        ifNot "0"

            json_select "type"

            # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
            # Content of settings.json will be written from "Settings" context-entry of this WSS
            IfVar "b_Show_MB_Nonstandard_Tags" "true"
                # Assumption: There is only 1 "printed in" on release level. This could be wrong. No examples found.
                if "printed in"
                    #outputto "MB_Release_Relations_Type_PrintedIn"
                    #    sayrest

                    json_select "area"
                        outputto "MB_Release_Relation_PrintedIn_Area_Name"
                        json_select "name"
                            sayrest
                        outputto "MB_Release_Relation_PrintedIn_Area_SortName"
                        json_select "sort-name"
                            sayrest
                        outputto "MB_Release_Relation_PrintedIn_Area_Disambiguation"
                        json_select "disambiguation"
                            sayrest
                        outputto "MB_Release_Relation_PrintedIn_Area_ID"
                        json_select "id"
                            sayrest

                        json_select_array "iso-3166-1-codes" -1 "/"
                        outputto "MB_Release_Relation_PrintedIn_Area_ISO3166"
                            sayrest
                    say "|"
                endif
                # endif "printed in"
            endif
            #IfVar "b_Show_MB_Nonstandard_Tags" "true"

            # Assumption: There is only 1 producer on release level. This could be wrong. No examples found.
            if "producer"

                json_select "target-credit"
                outputto "MB_Release_Relation_TargetCredit"
                    sayrest

                json_select "artist"
                json_foreach "artist"

                    #outputto "MB_Release_Relation_Artist_Name"    # ATTENTION: This value is NOT available in MB Picard
                    json_select "name"
                        IfNot ""
                            outputto "INVOLVEDPEOPLE"
                            say "producer:"
                            ifOutput "MB_Release_Relation_TargetCredit"
                                sayoutput "MB_Release_Relation_TargetCredit"
                            else
                                sayrest
                            endif
                            say ";"
                        endif

                    # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
                    # Content of settings.json will be written from "Settings" context-entry of this WSS
                    IfVar "b_Show_MB_Nonstandard_Tags" "true"

                        outputto "MB_Release_Relation_Artist_ID"               # ATTENTION: This value is NOT available in MB Picard
                        json_select "id"
                            sayrest

                        outputto "MB_Release_Relation_Artist_SortName"         # ATTENTION: This value is NOT available in MB Picard
                        json_select "sort-name"
                            sayrest

                        outputto "MB_Release_Relation_Artist_Disambiguation"   # ATTENTION: This value is NOT available in MB Picard
                        json_select "disambiguation"
                            sayrest

                        outputto "MB_Release_Relation_Artist_Type"             # ATTENTION: This value is NOT available in MB Picard
                        json_select "type"
                            sayrest

                        outputto "MB_Release_Relation_Artist_Type_ID"          # ATTENTION: This value is NOT available in MB Picard
                        json_select "type-id"
                            sayrest
                    endif
                    #IfVar "b_Show_MB_Nonstandard_Tags" "true"

                json_foreach_end
                #json_foreach_end "artist"

                say "|"

            endif
            # endif "producer"

        endif
        # ifNot "0"

    json_foreach_end
    #json_foreach_end "relations"

json_unselect_object
#json_unselect_object "relations"

###########################
# Object "release-events" #
###########################

# Settings read from file settings.json in subdirectory \data\sources of Mp3tag
# Content of settings.json will be written from "Settings" context-entry of this WSS
IfVar "b_Show_MB_Nonstandard_Tags" "true"

    # Goes to "Adjust tag information window", Panel top right "Metadata Album"
    json_select_object "release-events"
        json_foreach "release-events"

        # In MB Picard shown as "MusicBrainz Release Group Id"
        outputto "MB_Release_Events_Date"
        json_select "date"
            sayrest

            json_select "area"

                outputto "MB_Release_Events_Area_Name"
                json_select "name"
                    sayrest
                outputto "MB_Release_Events_Area_SortName"
                json_select "sort-name"
                    sayrest
                outputto "MB_Release_Events_Area_Disambiguation"
                json_select "disambiguation"
                    sayrest
                outputto "MB_Release_Events_Area_ID"
                json_select "id"
                    sayrest

                json_select_array "iso-3166-1-codes" -1 "/"
                outputto "MB_Release_Events_Area_ISO3166"
                    sayrest

        json_foreach_end
        #json_foreach_end "release-events"

    json_unselect_object
    #json_unselect_object "release-events"

endif
#IfVar "b_Show_MB_Nonstandard_Tags" "true"


##################
# Object "media" #
##################

# Goes to "Adjust tag information window", Panel top left "Metadata Title" (Same Metadata for all Tracks)
# AND
# Goes to "Adjust tag information window", Panel bottom left "Tracks" (Individual Metadata per Track)
#
# This object contains all the medias (like CD1, CD2) and all the tracks on every media
# There are two main loops:
# The first loop is looking for every media
# The second loop inside every media is looking for every track on the individual media

# Count number of existing Medias
json_select_object "media"

    # START Loop to iterate through every media
    json_foreach "media"

        # In MB Picard shown as "Total MB_"
        # Write the media array size = the MB_ Discnumberss
        outputto "TEMP_TOTALDISCS"
        if "1"
            # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
            # Content of settings.json will be written from "Settings" context-entry of this WSS
            ifVar "b_Fill_DISCNUMBER" "false"
                # Deleted, if only 1 Disc exists
                set "TEMP_DiscnumberOneToggle"
            else
                # For those preferring to see "1/1" as DISCNUMBER
                set "TEMP_DiscnumberOneToggle" "OneDisc"
            endif
        else
            # Set, if 2 or more Discs exists
            set "TEMP_DiscnumberOneToggle" "TwoOrMoreDiscs"
        endif
        # if "1"
        sayrest

        # Clear content for each loop

        set "TEMP_MEDIATYPE"
        json_select "format"
            # In MB Picard shown as "Media"
            # Mp3tag seems to convert MEDIATYPE to TMED - https://docs.mp3tag.de/mapping/#mediatype
            outputto "TEMP_MEDIATYPE"
            sayrest

            # In MB Picard shown as "Disc Subtitle"
            set "TEMP_TrackDiscTitle"
            outputto "TEMP_TrackDiscTitle"
            json_select "title"
                sayrest

        # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
        # Content of settings.json will be written from "Settings" context-entry of this WSS
        IfVar "b_Show_MB_Nonstandard_Tags" "true"

            # Clear content for each loop
            set "MB_Media_Format_ID"
            json_select "format-id"                     # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_Media_Format_ID"
                sayrest

            # Clear content for each loop
            set "MB_Media_Title"
            json_select "title"                         # ATTENTION: This value is NOT available in MB Picard
                outputto "MB_Media_Title"
                sayrest

            # Clear content for each loop
            set "MB_Media_TrackOffset"
            json_select "track-offset"
                outputto "MB_Media_TrackOffset"         # ATTENTION: This value is NOT available in MB Picard
                sayrest
        endif
        # IfVar "b_Show_MB_Nonstandard_Tags" "true"

        # Clear content for each media loop
        set "MB_Media_Position"
        json_select "position"
            outputto "MB_Media_Position"
            sayrest

        # In MB Picard shown as "Total Tracks"
        json_select "track-count"
            # Clear content for each loop
            set "MB_Media_TrackCount"
            outputto "MB_Media_TrackCount"
            sayrest

            set "TEMP_TrackTotalPlusOne"
            outputto "TEMP_TrackTotalPlusOne"
                # +1 will be added to the same "MB_Media_TrackCount"
                # The "+1 value" will be used later, if a "pregap" was found
                # Increase value +1 in a 2-Step regular expression .-) What a hack...
                RegexpReplace "(\d.*)" "0$1~01234567890"
                RegexpReplace "0(?!9*~)|([0-9])(?=9*~[0-9]*?\1([0-9]))|~[0-9]*" "$2"
                SayRegexp "^.*$"

        # Start Loop to iterate through every media.pregap.track
        # ------------------------------------------------------
        json_select_object "pregap"

            # Only proceed if a pregap (aka "Hidden Track 0") exists
            if "pregap"

                # If a "pregap" was found, use the increased +1 "MB_Media_TrackCount"
                set "MB_Media_TrackCount"              # Clear current content
                outputto "MB_Media_TrackCount"
                    sayoutput "TEMP_TrackTotalPlusOne"    # Fill content of TrackCount

                # Start Loop to iterate through every media.pregap.track - only if "pregap" exists
                # --------------------------------------------------------------------------------
                json_foreach "pregap"

                    # Construct the detail row for every track, with at least
                    # track number, optional /Total Tracks, track title, track length

                    # This not so obvious line is extremely important to only fill the existing number of local tracks
                    # The number of local tracks has not to match the number of tracks of the currently choosen release
                    outputto "tracks"
                        # To get the columns separated in the lower left column Tracks list, we need a "|"
                        # It doesn't matter at which position and order the track details get filled into the individual tags
                        say "|"

                    # In MB Picard shown as (Track-) "Track Number"
                    json_select "number"
                        outputto "TRACK"

                        if ""               # If a pregap-track has no track-number at all
                            say "0"         # fill 0 (zero) and not let create /14 instead of 0/14
                        endif

                        # This "sayrest" must be disabled, if the "pregap" track should appear as track number 1
                        sayrest

                        # This section must be enabled, if the "pregap" track should appear as track number 1
                        # # This would only be necessary, if the "pregap" track should not appear as track number 0 (zero)
                        # # If this would be enabled, the following tracks needs also to be incremented by +1
                        #  outputto "TEMP_PREGAP_TrackNumberPlusOne"
                        #  # Increase value +1 in a 2-Step regular expresssion .-) What a hack...
                        #  RegexpReplace "(\d.*)" "0$1~01234567890"
                        #  RegexpReplace "0(?!9*~)|([0-9])(?=9*~[0-9]*?\1([0-9]))|~[0-9]*" "$2"
                        #  set "TEMP_PREGAP_TrackNumberPlusOne"           # Clear current content
                        #  SayRegexp "^.*$"
                        #  outputto "TRACK"
                        #      sayoutput "TEMP_PREGAP_TrackNumberPlusOne"  # Fill content of TEMP_PREGAP_TrackNumberPlusOne

                        # If the content of "MB_Media_TrackCount" is not empty
                        ifOutput "MB_Media_TrackCount"
                            # Add a slash between the TRACK number and total number of tracks
                            say "/"
                            # Use the value filled at the Media-Level above
                            sayoutput "MB_Media_TrackCount"
                        endif
                        #ifOutput "MB_Media_TrackCount"
                        say "|"

                    # In MB Picard shown as (Track-) "Title"
                    json_select "title"
                        outputto "Title"
                        sayrest
                        say "|"

                    # Write current Discnumber per Track
                    # In MB Picard shown as (Track-) "Disc Number"
                    IfOutput "TEMP_DiscnumberOneToggle"         # By default: Only Discnumbers greater than 1 will be written (3/11)
                        outputto "Discnumber"                   # This prevents "useless" Discnumber 1/1
                        sayoutput "MB_Media_Position"           # Override is prossible in the WSS-Settings
                        ifnot "TEMP_TOTALDISCS"
                            say "/"
                            sayoutput "TEMP_TOTALDISCS"
                        endif
                        say "|"
                    endif
                    #IfOutput "TEMP_DiscnumberOneToggle"

                    # In MB Picard shown as "MusicBrainz Track Id"
                    # In Mp3tag    shown as "MUSICBRAINZ_RELEASETRACKID"
                    # For technical details in German  see https://community.mp3tag.de/t/58074/3
                    # For technical details in English see https://community.metabrainz.org/t/650381/4
                    outputto "MUSICBRAINZ_RELEASETRACKID"
                    json_select "id"
                        sayrest
                        say "|"

                    # In MB Picard shown as "Disc Subtitle"     # id3Tag TSST is officially only available in ID3v2.4
                    outputto "SetSubtitle"                      # MB Picard - but not Mp3tag - write it also in ID3v2.3 for "compatibility reasons"
                    sayoutput "TEMP_TrackDiscTitle"             # https://community.mp3tag.de/t/add-field-mapping-for-musicbrainz-picard/44062/8
                        say "|"                                 # You have to set a MB Picard-Tagger script for full compatibility

                    # In MB Picard shown as "Media"
                    outputto "MediaType"
                    sayoutput "TEMP_MEDIATYPE"
                        say "|"

                    # Artist-Credits from pregap-Track-Level, not Release-Level for compatibility to MB Picard
                    json_select "artist-credit"
                    json_foreach "artist-credit"
                        # In MB Picard shown as (Track-) "Artist"
                        json_select "name"
                            outputto "Artist"
                            sayrest
                            say "|"

                        # Assumption: There is only 1 ARTIST for "pregap". This could be wrong. No examples found.
                        # In MB Picard shown as "Artists"
                        json_select "name"
                            outputto "ARTISTS"
                            sayrest
                            say "|"

                            json_select "artist"
                                json_select "sort-name"
                                    # In MB Picard shown as (Album Main-) "Artist Sort Order"
                                    outputto "Artistsort"
                                    sayrest
                                    say "|"

                                # In MB Picard shown as "MusicBrainz Artist Id"
                                json_select "id"
                                    outputto "MUSICBRAINZ_ARTISTID"
                                    sayrest
                                    say "|"

                                # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
                                # Content of settings.json will be written from "Settings" context-entry of this WSS
                                IfVar "b_Show_MB_Nonstandard_Tags" "true"
                                    json_select "disambiguation"
                                        #outputto "MB_Media_Pregap_ArtistCredit_Artist_Disambiguation"  # must be filled in Tracks not Pregap
                                        outputto "MB_Media_Tracks_ArtistCredit_Artist_Disambiguation"   # otherwise the number of entries does not match the number of tracks
                                        sayrest
                                        say "|"
                                    json_select "type"
                                        #outputto "MB_Media_Pregap_ArtistCredit_Artist_Type"
                                        outputto "MB_Media_Tracks_ArtistCredit_Artist_Type"
                                        sayrest
                                        say "|"
                                    json_select "type-id"
                                        #outputto "MB_Media_Pregap_ArtistCredit_Artist_TypeID"
                                        outputto "MB_Media_Tracks_ArtistCredit_Artist_TypeID"
                                        sayrest
                                        say "|"
                                endif
                                # IfVar "b_Show_MB_Nonstandard_Tags" "true"

                    json_foreach_end
                    #json_foreach_end "artist-credit"


                    # Change to media -> pregap -> recording level
                    # In MB Picard shown as "MusicBrainz Recording Id"
                    #json_select_object "recording"
                    json_select "recording"
                    json_foreach "recording"
                        # Special tag ISRC (International Standard Recording Code)
                        # Assumption: There NO ISRC for a "pregap" track. This could be wrong. No examples found.
                        outputto "ISRC"
                            #say "no ISRC for pregap track"
                            say ""
                            say "|"

                        # Visible as last column "length" in the lower left Panel in "Adjust tag information" only
                        # Read only value, can not be changed
                        outputto "_LENGTH"
                        json_select "recording"
                            json_select "length"
                                sayrest
                                say "|"

                        # In MB Picard shown as "MusicBrainz Recording Id"
                        # In Mp3tag    shown as "MUSICBRAINZ_TRACKID"
                        # For technical details in German  see https://community.mp3tag.de/t/58074/3
                        # For technical details in English see https://community.metabrainz.org/t/650381/4
                        outputto "MUSICBRAINZ_TRACKID"
                        json_select "id"
                            sayrest
                            say "|"

                        # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
                        # Content of settings.json will be written from "Settings" context-entry of this WSS
                        IfVar "b_Show_MB_Media_Tracks_Recording_Metadata" "true"
                            json_select "title"
                                #outputto "MB_Media_Pregap_Recording_Title"       # must be filled in Tracks not Pregap
                                outputto "MB_Media_Tracks_Recording_Title"        # otherwise the number of entries does not match the number of tracks
                                    sayrest
                                    say "|"
                            json_select "first-release-date"
                                #outputto "MB_Media_Pregap_Recording_FirstRelease_Date"
                                outputto "MB_Media_Tracks_Recording_FirstRelease_Date"
                                    sayrest
                                    say "|"
                            json_select "disambiguation"
                                #outputto "MB_Media_Pregap_Recording_Disambiguation"
                                outputto "MB_Media_Tracks_Recording_Disambiguation"
                                    sayrest
                                    say "|"
                            json_select "video"
                                #outputto "MB_Media_Pregap_Recording_IsThis_Video"
                                outputto "MB_Media_Tracks_Recording_IsThis_Video"
                                    sayrest
                                    say "|"
                        endif
                        # IfVar "b_Show_MB_Media_Tracks_Recording_Metadata" "true"

                    #json_unselect_object
                    # json_unselect_object "recording"
                    json_foreach_end
                    #json_foreach_end "recording"

                json_foreach_end
                # json_foreach_end "pregap"
                # ----------------------------------------------------
                # End Loop to iterate through every media.pregap.track

            endif
            # endif "pregap"

        json_unselect_object
        # json_unselect_object "pregap"

        json_select_object "tracks"

            # START Loop to iterate through every individual track
            json_foreach "tracks"

                # This not so obvious line is extremely important to only fill the existing number of local tracks
                # The number of local tracks has not to match the number of tracks of the currently choosen release
                outputto "tracks"
                    say "|"

                json_select "number"
                    outputto "TRACK"
                        # This "sayrest" must be disabled, if the "pregap" track should appear as track number 1
                        sayrest

                        # # This section must be enabled, if the "pregap" track should appear as track number 1
                        # # This would only be necessary, if the "pregap" track should not appear as track number 0 (zero)
                        # # If this would be enabled, the following tracks needs also to be incremented by +1
                        # outputto "TEMP_TRACK_TrackNumberPlusOne"
                        # # Increase value +1 in a 2-Step regular expresssion .-) What a hack...
                        # RegexpReplace "(\d.*)" "0$1~01234567890"
                        # RegexpReplace "0(?!9*~)|([0-9])(?=9*~[0-9]*?\1([0-9]))|~[0-9]*" "$2"
                        # set "TEMP_TRACK_TrackNumberPlusOne"            # Clear current content
                        # SayRegexp "^.*$"
                        # outputto "TRACK"
                        #     sayoutput "TEMP_TRACK_TrackNumberPlusOne"  # Fill content of "TEMP_TRACK_TrackNumberPlusOne"


                    # If the content of MB_Media_TrackCount is not empty
                    ifOutput "MB_Media_TrackCount"
                        # Add a slash between the TRACK number and total number of tracks
                        say "/"
                        # Use the value filled at the Media-Level above
                        sayoutput "MB_Media_TrackCount"
                    endif
                    #ifOutput "MB_Media_TrackCount"

                    # To get the TITLEs separated in the lower left column Tracks list, we need a "|"
                    # It doesn't matter at which position and order the track details get filled into the individual tags
                    say "|"

                # In MB Picard shown as (Track-) "Title"
                json_select "title"
                    outputto "TITLE"
                        sayrest
                        say "|"

                # Write current Discnumber per Track
                # In MB Picard shown as (Track-) "Disc Number"
                IfOutput "TEMP_DiscnumberOneToggle"                         # By default: Only Discnumbers greater than 1 will be written (3/11)
                    outputto "Discnumber"                                   # This prevents "useless" Discnumber 1/1
                    sayoutput "MB_Media_Position"                           # Override is prossible in the WSS-Settings
                    ifnot "TEMP_TOTALDISCS"
                        say "/"
                        sayoutput "TEMP_TOTALDISCS"
                    endif
                    say "|"
                endif
                #IfOutput "TEMP_DiscnumberOneToggle"


                # In MB Picard shown as "MusicBrainz Track Id"
                # In Mp3tag    shown as "MUSICBRAINZ_RELEASETRACKID"
                # For technical details in German  see https://community.mp3tag.de/t/58074/3
                # For technical details in English see https://community.metabrainz.org/t/650381/4
                json_select "id"
                    outputto "MUSICBRAINZ_RELEASETRACKID"
                        sayrest
                        say "|"

                # In MB Picard shown as "Disc Subtitle"     # id3Tag TSST is officially only available in ID3v2.4
                outputto "SetSubtitle"                      # MB Picard - but not Mp3tag - write it also in ID3v2.3 for "compatibility reasons"
                sayoutput "TEMP_TrackDiscTitle"             # https://community.mp3tag.de/t/add-field-mapping-for-musicbrainz-picard/44062/8
                    say "|"                                 # You have to set a MB Picard-Tagger script for full compatibility

                json_select "length"
                    # Visible as last column "length" in the lower left Panel in "Adjust tag information" only
                    # Read only value, can not be changed, will automatically be converted from seconds like 213000 into 3:33
                    # There is no need to use sayduration "_LENGTH" with any parameters
                    outputto "_LENGTH"
                        sayrest
                        say "|"

                # In MB Picard shown as "Media"
                outputto "MediaType"
                sayoutput "TEMP_MEDIATYPE"
                    say "|"

                # START Loop to iterate through every individual artist-credit per track
                json_foreach "artist-credit"
                    json_select "name"
                        # Artist-Credits from pregap-Track-Level, not Release-Level for compatibility to MB Picard
                        # Only if an Artist name was found
                        outputto "LOOP_AC_Artist_Name"      # add it to the loop variable
                        sayrest

                        # For whatever reason, MB Picard is using this same value also as "LOOP_AC_ARTIST_Artist_Name"
                        outputto "LOOP_AC_ARTIST_Artist_Name"
                        GotoChar 1
                        sayrest

                    json_select "joinphrase"
                        ifNot ""
                            outputto "LOOP_AC_Joinphrase"
                            sayrest
                            GotoChar 1
                            outputto "TEMP_MB_JOINPHRASE"
                            sayrest
                        else
                            set "TEMP_MB_JOINPHRASE"
                        endif

                        IfOutput "LOOP_AC_Artist_Name"             # if the loop variable is not empty (as at the first run)
                            outputto "LOOP_AC_Artist_Name"
                            sayoutput "LOOP_AC_Joinphrase"         # Divides multiple names with the individual joinphrase like " feat. " or " and "
                            #set "LOOP_AC_Joinphrase"
                        endif

                        # For whatever reason, MB Picard is using this name also as "LOOP_AC_ARTIST_Artist_Name"
                        IfOutput "TEMP_MB_JOINPHRASE"              # if the loop variable is not empty (as at the first run)
                            outputto "LOOP_AC_ARTIST_Artist_Name"
                            say "/"                                # Divides multiple names with a fixed Slash
                        endif


                    # START Loop to iterate through every individual artist in artist-credit per track
                    json_select "artist"
                    json_foreach "artist"
                        json_select "name"
                            # In MB Picard shown as (Album Main-) "Artist"
                            # For whatever reason, MB Picard is not using this "LOOP_AC_ARTIST_Artist_Name"
                            # outputto "LOOP_AC_ARTIST_Artist_Name"
                            # sayrest
                            # IfOutput "TEMP_MB_JOINPHRASE"
                            #     say "/"
                            # endif
                            # For whatever reason, MB Picard is using the above "artist-credit" name
                            # and divides multiple names with a slash

                        json_select "sort-name"
                            # In MB Picard shown as (Album Main-) "Artist Sort Order"
                            outputto "LOOP_AC_ARTIST_Artistsort_Name"
                            sayrest
                            IfOutput "LOOP_AC_ARTIST_Artistsort_Name"      # if the loop variable is not empty (as at the first run)
                                outputto "LOOP_AC_ARTIST_Artistsort_Name"
                                sayoutput "LOOP_AC_Joinphrase"
                                set "LOOP_AC_Joinphrase"
                            endif

                        json_select "id"
                            # In MB Picard shown as "MusicBrainz Artist Id"
                            outputto "LOOP_MUSICBRAINZ_ARTISTID"
                            sayrest
                            IfOutput "TEMP_MB_JOINPHRASE"
                                say "/"
                            endif

                        # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
                        # Content of settings.json will be written from "Settings" context-entry of this WSS
                        IfVar "b_Show_MB_Nonstandard_Tags" "true"
                            json_select "disambiguation"
                                outputto "MB_Media_Tracks_ArtistCredit_Artist_Disambiguation"
                                sayrest
                                say "|"
                            json_select "type"
                                outputto "MB_Media_Tracks_ArtistCredit_Artist_Type"
                                sayrest
                                say "|"
                            json_select "type-id"
                                outputto "MB_Media_Tracks_ArtistCredit_Artist_TypeID"
                                sayrest
                                say "|"
                        endif
                        # IfVar "b_Show_MB_Nonstandard_Tags" "true"

                    json_foreach_end
                    #json_foreach_end "artist"
                    # STOP Loop to iterate through every individual artist in artist-credit per track

                json_foreach_end
                #json_foreach_end "artist-credit"
                # STOP Loop to iterate through every individual artist-credit per track

                # In MB Picard shown as (Album Main-) "Artist"
                outputto "Artist"
                    sayoutput "LOOP_AC_Artist_Name"
                    say "|"
                    set "LOOP_AC_Artist_Name"

                # In MB Picard shown as "Artists"
                outputto "ARTISTS"
                    sayoutput "LOOP_AC_ARTIST_Artist_Name"
                    say "|"
                    set "LOOP_AC_ARTIST_Artist_Name"


                # In MB Picard shown as (Album Main-) "Artist Sort Order"
                outputto "Artistsort"
                    sayoutput "LOOP_AC_ARTIST_Artistsort_Name"
                    say "|"
                    set "LOOP_AC_ARTIST_Artistsort_Name"

                # In MB Picard shown as "MusicBrainz Artist Id"
                outputto "MUSICBRAINZ_ARTISTID"
                    sayoutput "LOOP_MUSICBRAINZ_ARTISTID"
                    say "|"
                    set "LOOP_MUSICBRAINZ_ARTISTID"

                set "LOOP_AC_Joinphrase"


                 # START Loop to iterate through every individual recording per track
                json_select "recording"
                json_foreach "recording"

                    # Settings read from file settings.json in subdirectory \data\sources of Mp3tag
                    # Content of settings.json will be written from "Settings" context-entry of this WSS
                    IfVar "b_Show_MB_Media_Tracks_Recording_Metadata" "true"
                        json_select "title"
                            outputto "MB_Media_Tracks_Recording_Title"
                                sayrest
                                say "|"
                        json_select "first-release-date"
                            outputto "MB_Media_Tracks_Recording_FirstRelease_Date"
                                sayrest
                                say "|"
                        json_select "disambiguation"
                            outputto "MB_Media_Tracks_Recording_Disambiguation"
                                sayrest
                                say "|"
                        json_select "video"
                            outputto "MB_Media_Tracks_Recording_IsThis_Video"
                                sayrest
                                say "|"
                    endif
                    # IfVar "b_Show_MB_Media_Tracks_Recording_Metadata" "true"

                    # In MB Picard shown as "MusicBrainz Recording Id"
                    # In Mp3tag    shown as "MUSICBRAINZ_TRACKID"
                    # For technical details in German  see https://community.mp3tag.de/t/58074/3
                    # For technical details in English see https://community.metabrainz.org/t/650381/4
                    json_select "id"
                        outputto "MUSICBRAINZ_TRACKID"
                        sayrest
                        say "|"

                    # https://en.wikipedia.org/wiki/International_Standard_Recording_Code
                    # Format   CC-RGC-YY-DESCO (CountryCode, RegistrantCode, YearOfReference, DesignatinCode)
                    # Example: CA-CWV-21-15971
                    # In MB Picard shown as "ISRC"
                    json_select_array "isrcs" -1 "/"
                        outputto "ISRC"
                            # Unformatted version:
                            sayrest                          # Remains untouched and unformated
                            # Formatted version:
                            # RegexpReplace "(([A-Z]{2})?(\w{3}?)(\d{2})?(\d{5}))" "$2-$3-$4-$5"
                            # SayRegexp "^.*$"                # Prettyfied format
                            say "|"

                json_foreach_end
                #json_foreach_end "recording"
                # STOP Loop to iterate through every individual recording per track
                #

            json_foreach_end
            #json_foreach_end "tracks"
            # STOP Loop to iterate through every individual track

        json_unselect_object
        # json_unselect_object "tracks"

    json_foreach_end
    #json_foreach_end "media"
    # STOP Loop to iterate through every media

json_unselect_object
#json_unselect_object "media"

# Not shown/set by default in MB Picard, just to identify the data source
# outputto "Comment"
# say "Tagged with one of the Mp3tag WS Scripts MusicBrainz expanded v1.00"
#
JSON "OFF"


#############################################
# Delete temporary variables, never show them
set "TEMP_DiscnumberOneToggle"
set "TEMP_MB_JOINPHRASE"
set "TEMP_MEDIATYPE"
set "TEMP_TOTALDISCS"
set "TEMP_TrackTotalPlusOne"
set "TEMP_PREGAP_TrackNumberPlusOne"
set "TEMP_TRACK_TrackNumberPlusOne"
set "TEMP_TrackDiscTitle"
set "MB_Media_Position"
set "MB_Media_TrackCount"
set "LOOP_AC_Artist_Name"
set "LOOP_AC_ARTIST_Artist_Name"
set "LOOP_AC_Joinphrase"
set "LOOP_AC_ARTIST_Artistsort_Name"
set "LOOP_MUSICBRAINZ_ARTISTID"

##################################################################
# If you want to always skip a tag, you can just delete the # sign
# in front of the following tags:

#set "Title"
#set "Artist"
#set "Album"
#set "Track"
#Length can't be set or unset
#set "Year"
#set "Date"
#set "ALBUMARTIST"
#set "Albumartistsort"
#set "Artistsort"
#set "ARTISTS"
#set "ASIN"
#set "BARCODE"
#set "CATALOGNUMBER"
#set "Comment"
#set "COMPILATION"
#set "DATE"
#set "DISAMBIGUATION"
#set "Discnumber"
#set "ISRC"
#set "LANGUAGE"
#set "MEDIATYPE"
#set "MUSICBRAINZ_ALBUMARTISTID"
#set "MUSICBRAINZ_ALBUMRELEASECOUNTRY"
#set "MUSICBRAINZ_ALBUMSTATUS"
#set "MUSICBRAINZ_ALBUMTYPE"
#set "MUSICBRAINZ_ALBUMID"
#set "MUSICBRAINZ_ARTISTID"
#set "MUSICBRAINZ_RELEASEGROUPID"
#set "MUSICBRAINZ_RELEASETRACKID"
#set "MUSICBRAINZ_TRACKID"
#set "ORIGYEAR"
#set "originalyear"
#set "PUBLISHER"
#set "SCRIPT"

#######################################################
# If you want to always show the experimental MB_ tags,
# you can enable/check these Script-Settings:
# "Show all available non-standard MusicBrainz metadata tags?"
#  (EXPERIMENTAL and SLOW!)
# and/or
# "Show available metadata for every track recording as own column?"
#  (This includes MB_Media_Tracks_Recording_Title, MB_Media_Tracks_Recording_FirstRelease_Date and MB_Media_Tracks_Recording_Disambiguation)"

# If you want to see the DISCNUMBER tag also for one disc releases as 1/1
# you can enable/check this Script-Settings:
# "Fill DISCNUMBER tag with 1/1 for releases with one media only?"

# If you want to see the ALBUMSTATUS and ALBUMTYPE tag content in lowercase as in MB Picard
# you can enable/check this Script-Settings:
# "Convert ALBUMSTATUS and ALBUMTYPE to lowercase like MB Picard?"

# If you don't want to download the frontcover album picture at all
# you can disable/uncheck this Script-Settings:
# "Download the album front picture from Cover Art Archive?"

# If you don't want to download and see the small album pictures for preview in 'List of search results'
# you can disable/uncheck this Script-Settings:
# "Download small thumbnail album pictures for preview in 'List of search results'?"

# If you don't want an album cover at all, you can configure it in the Mp3tag-GUI:
# You can use the checkbox below the preview image to select whether you want to embed the cover in the APIC image tag.
#
# You can also prevent that a cover will be downloaded, if you remove
# the # in the following line
#set "coverurl"

# Notes:
# ------
#
# You need to set a MB Picard Tagger script for compatibility with SetSubtitle
# MB Picard Options -> Options -> Scripting -> Enable Tagger Script(s)
#   $set(SetSubtitle,%discsubtitle%)
#   $unset(discsubtitle)
#
#set "SetSubtitle"

# MusicBrainz Picard reads the "Total Discs" from "DISCNUMBER" in format "1/3"
# if you want to see TOTALDISCS tag with content outside MB Picard
# set a # in front of the following line
#
set "totaldiscs"

# MusicBrainz Picard reads the "Total Tracks" from "TRACK" in format "10/30"
# if you want to see TOTALTRACKS tag with content outside MB Picard
# set a # in front of the following line
#
set "totaltracks"
