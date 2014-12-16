# Venues

This app handles one model - a Venue. It is pretty simple and a good example of a self-contained app. The only dependency it has on another app's models is for retrieving a list of fixtures for a particular venue.

Venues are typically astro pitches but the model can be used for any geographical location, ideally with a physical address. For example, the clubhouse is listed as a 'Venue'.

### URLS

|(Example) URL         |View            |Description                                 |
|----------------------|----------------|--------------------------------------------|
|**/venues/**          |VenueListView   |Lists all venues, home and away. Filterable.|
|**/venues/<leys>/**   |VenueDetailView |Details on a particular venue.              |

### Models

|Name       |Description    |
|-----------|----------------
|**Venue**  |The various venues at which hockey matches are played, plus one or two other locations (e.g. clubhouse).|

### Admin Interface

You can add/edit/remove venues through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/venues/).
