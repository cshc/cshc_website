# Training

This app handles one model - a TrainingSession. Like the venues app, it is pretty simple and a good example of a self-contained app. The only dependencies it has on other apps' models are Venue and Season.

An instance of the TrainingSession model represents a training session at a particular date/time. 'Pay and Play' sessions are also recorded using the TrainingSession model.

### Feeds

One of the cool features of this app is the auto-generated ical calendar feed of training sessions for the current season. This enables users to subscribe to this calendar and see all the training sessions right in their own calendar app.

### URLS

|(Example) URL                   |View                         |Description                                 |
|--------------------------------|-----------------------------|--------------------------------------------|
|**/training/**                  |UpcomingTrainingSessionsView |Lists all upcoming training sessions.       |
|**/training/<41>/**             |TrainingSessionDetailView    |Details of a particular training session.   |
|**/training/cshc_training.ics** |TrainingSessionICalFeed      |Automatically generated ical calendar feed of this season's training sessions|

### Models

|Name                 |Description    |
|---------------------|----------------
|**TrainingSession**  |The various training sessions run by the club.|

### Admin Interface

You can add/edit/remove training sessions through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/training/).
