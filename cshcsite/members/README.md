# Members

This app deals with club members and their membership in squads and the committee.

Members are closely related to Users. To distinquish:

A Member:
- participates in matches (see the Appeaerance model)
- (potentially) holds committee positions
- (hopefully) wins awards

A User:
- logs in/out of the website
- has permissions (e.g. to access the admin interface)

A User may request (via a button on their profile page) that their corresponding Member be associated (linked) with their User. This is done as a manual step by an administrator using the admin interface (the Member model has a 'User' field.) Once a Member is linked to a User, the User may edit their profile picture (and preferred playing position) via their profile page.

### URLS

|(Example) URL                 |View             |Description                                              |
|------------------------------|-----------------|---------------------------------------------------------|
|**/members/**                 |MemberListView   |List of all members (filterable).                        |
|**/members/<32>/**            |MemberDetailView |Details of a particular member.                          |
|**/members/<32>/ajax/stats/** |MemberStatsView  |Member stats are retrived asynchronously for efficiency. |

### Models

|Name                    |Description                                                                    |
|------------------------|-------------------------------------------------------------------------------|
|**Member**              |Club members - see above description for more details.                         |
|**SquadMembership**     |Associates a member with a squad (in a particular season).                     |
|**CommitteePosition**   |Definitions of the various committee positions.                                |
|**CommitteeMembership** |Tracks which member held which committee position in a particular season.      |

### Admin Interface

You can add/edit/remove members, squad membership and committee positions and memberships through the [admin interface](http://www.cambridgesouthhockeyclub.co.uk/admin/members/).