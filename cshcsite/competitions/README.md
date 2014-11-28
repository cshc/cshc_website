# Competitions

This app contains no views but the models are some of the most fundamental. The models in the competitions app are referenced by other models such as Match, ClubTeamSeasonParticipation, AwardWinner, etc.


### Models

|Name                       | Description  |
|---------------------------|----------------
|**Season**                 |The various seasons (years) in which hockey matches are played. Each match is associated with a particular season.|
|**League***                |Represents the leagues that organise the divisions in which CSHC plays|
|**Division**               |The divisions in which CSHC plays competitive matches|
|**Cup**                    |Represents the cup competitions in which CSHC compete|
|**DivisionResult**         |Stores the playing records of teams (CSHC and opposition) over the years. See the divisionresult.py module docstring for a fuller description.|

### Admin Interface

You can add/edit/remove seasons, leagues, divisions and cup competitions through the [admin interface](http://www.cambridgesouthhockeyclub.co.uk/admin/competitions/). Note - DivisionResult is deliberately hidden from the admin interface as it is handled programmatically.
