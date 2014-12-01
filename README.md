# Cambridge South Hockey Club Website

This is the main repository for the Cambridge South Hockey Club website source code.

### Django
The server side code is  written in Python using the [Django Web Framwork](https://www.djangoproject.com/).

### Bootstrap
The website styling relies heavily on the popular front-end framework [Bootstrap](http://getbootstrap.com/2.3.2/).

### jQuery
Javascript library [jQuery](http://jquery.com/) is used (its also a prerequisite of Bootstrap) for DOM manipulation and other Javascript-y things.

### Font Awesome
Icons are primarily (i.e. wherever possible) provided by [Font Awesome](http://fortawesome.github.io/Font-Awesome/3.2.1/).

### Amazon S3
Static files (anything within the cshc_website\cshcsite\static directory) are served from an [Amazon S3](http://aws.amazon.com/s3/) account.

### AngularJS
Some of the more dynamic front-end client-side functionality is written using the [AngularJS](https://angularjs.org) framework.

## Apps

The website is split into a number of logical Django apps. See the individual app's README files for more details.

|App                |Description                                                                 |
|-------------------|----------------------------------------------------------------------------|
|**core**           |Common/shared functionality and utilities, custom Django management commands, middleware, template tags, etc.|
|**matches**        |Handles matches, appearances and goal king and accidental tourist statistics|
|**teams**          |Handles CSHC teams, team captains etc.|
|**competitions**   |Handles leagues, divisions, cup competitions and seasons|
|**opposition**     |Handles opposition clubs and teams|
|**members**        |Handles club members (i.e. players)|
|**venues**         |Handles match venues|
|**training**       |Handles club training sessions|
|**awards**         |Handles match awards and end of season awards|