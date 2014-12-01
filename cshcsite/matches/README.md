# Matches

This is one of the main CSHC apps. Matches are at the heart of the club's data so a lot of the site's functionality is contained within this app.

Goal King and Accidental Tourist statistics are automatically calculated as part of a nightly cronjob and the stats cached in the GoalKing model/table. This is one of a number of tables used to facilitate the speedy display of data which would otherwise take an unacceptable amount of time to calculate 'live'.

### Feeds

RSS/Atom feeds of the latest match reports and an ical calendar feed of all matches this season are automatically generated - see feeds.py

### URLS

|(Example) URL                                      |View                               |Description                                 |
|---------------------------------------------------|-----------------------------------|--------------------------------------------|
|**/matches/**                                      |MatchListView                      |Searchable/filterable list of all matches.|
|**/matches/23/**                                   |MatchDetailView                    |Details of a specific match (fixture or result) - includes match report.|
|**/matches/23-Apr-13/**                            |MatchesByDateView                  |List of matches on a particular date.|
|**/matches/by-season/<2012-2013>/**                |MatchesBySeasonView                |Calendar view of all matches in a particular season. If the season is not supplied in the URL, the current season's matches will be displayed.|
|**/matches/latest-results/**                       |LatestResultsView                  |List of the latest result for each team.|
|**/matches/next-fixtures/**                        |NextFixturesView                   |List of the next fixture for each team.|
|**/matches/goal-king/<2012-2013>/**                |GoalKingSeasonView                 |Goal King stats table for a particular season. If the season is not supplied in the URL, the current season's stats will be displayed.|
|**/matches/goal-king/2011-2012/ajax/**             |GoalKingSeasonUpdateView           |AJAX-only: Updates and refreshes Goal King stats.|
|**/matches/accidental-tourist/<2012-2013>/**       |AccidentalTouristSeasonView        |Accidental Tourist stats table for a particular season. If the season is not supplied in the URL, the current season's stats will be displayed.|
|**/matches/accidental-tourist/<2012-2013>/ajax/**  |AccidentalTouristSeasonUpdateView  |AJAX-only: Updates and refreshes Accidental Tourist stats.|
|**/matches/naughty-step/**                         |NaughtyStepView                    |Statistics on the number of cards (red/yellow/green) received by members.|
|**/matches/feed/rss/**                             |RssMatchReportsFeed                |RSS feed of match reports.|
|**/matches/feed/atom/**                            |AtomMatchReportsFeed               |Atom feed of match reports.|
|**/matches/cshc_matches.ics**                      |MatchICalFeed                      |Calendar feed of this season's matches.|

### Models

|Name           |Description                                                                    |
|---------------|-------------------------------------------------------------------------------|
|**Match**      |One entry for each match we play. See module docstring in match.py for more details.|
|**Appearance** |Used to track which members (players) play in each match.|
|**GoalKing**   |Auto-updated goals and travelling statistics for each member in a particular season. Used for display of Goal King and Accidental Tourist statistics.|

### Admin Interface

You can add/edit/remove matches and appearances (typically done in-line for a particular match) through the [admin interface](http://www.cambridgesouthhockeyclub.co.uk/admin/matches/). Note - GoalKing is deliberately hidden from the admin interface as it is handled programmatically.
