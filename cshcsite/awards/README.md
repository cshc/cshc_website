# Awards

This app deals with awards - both those awarded each match (i.e. Man of the Match and Lemon of the Match) and at the End of Season dinner (e.g. Player of the Season, etc.).

This is a very simple app - there are no views directly associated with it. Typically you just add match award winners as you enter the details for a match result and end of season award winners once they're decided at the end of a season.

Awards appear on the website in the following locations:
- Player (member) profile pages (end of season and match awards)
- Match details (match awards)

### Models

|Name                       | Description  |
|---------------------------|----------------
|**Award**                  |A base class with common award functionality (the award name)|
|**MatchAward***            |The various awards that can be awarded at a match. Currently there are just two instances - MOM and LOM|
|**EndOfSeasonAward**       |The various awards that can be awarded at the end of a season. Note - these can change from year to year so some years you may need to add some awards (via the admin interface)|
|**AwardWinner**            |A base class with common award winner functionality (member, comment etc)|
|**MatchAwardWinner**       |All the MOM and LOM award winners|
|**EndOfSeasonAwardWinner** |All the end of season award winners|

### Admin Interface

You can add/edit/remove awards and award winners through the [admin interface](http://www.cambridgesouthhockeyclub.co.uk/admin/awards/).
