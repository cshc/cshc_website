# Opposition

This app deals with opposition clubs and their various teams. Each match references an opposition team. Note that this means Cambridge South appears as an opposition club as we often play matches against another South team. This also means that there will be TWO match instances for intra-club matches such as these - one for each CSHC team playing.

Cambridge South's playing record against each club is automatically calculated as part of a nightly cronjob and the stats cached in the ClubStats model/table. This is one of a number of tables used to facilitate the speedy display of data which would otherwise take an unacceptable amount of time to calculate 'live'.

### URLS

|(Example) URL                           |View                |Description                                 |
|----------------------------------------|--------------------|--------------------------------------------|
|**/opposition/clubs/**                  |ClubListView        |List of all oppostion clubs (including statistics).|
|**/opposition/clubs/ajax/**             |ClubStatsUpdateView |AJAX-only endpoint for refreshing the club stats.|
|**/opposition/clubs/<cambridge-city>/** |ClubDetailView      |Details of a particular opposition club. |

### Models

|Name          |Description                                                                    |
|--------------|-------------------------------------------------------------------------------|
|**Club**      |The various opposition clubs that we play against.                             |
|**Team**      |The teams within an opposition club (M1, M2, L1 etc)                           |
|**ClubStats** |Auto-updated playing record statistics for each club, broken down by CSHC team.|

### Admin Interface

You can add/edit/remove clubs and teams through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/opposition/). Note - ClubStats is deliberately hidden from the admin interface as it is handled programmatically.
