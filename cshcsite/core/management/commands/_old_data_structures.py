# -*-encoding: utf-8-*-
import string
import random
import math
from datetime import datetime
from competitions.models import Season, League, Division, Cup
from members.models import Member
from venues.models import Venue
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from opposition.models import Club, Team
from matches.models import Match, Appearance
from awards.models import MatchAward, MatchAwardWinner
from core.models import TeamGender, TeamOrdinal
from django.conf import settings

old_date_format = '%d/%m/%Y'    # e.g. '01/09/2009'
old_time_format1 = '%H:%M:%S'   # e.g. '00:00:00'
old_time_format2 = '%H:%M'      # e.g. '00:00'


def get_digits(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c += i
    return c


class Old_Table_Entry:

    def __init__(self, field_values):

        try:
            for attr_name, attr_value in zip(self.__class__.field_names, field_values):
                #v = bytearray(attr_value).replace('\x92', '\'').replace('\x93', '"').replace('\x94', '"').replace('\xa3', '\x9c').decode('utf-8')
                v = bytearray(attr_value).decode('cp1252')

                #print 'AFTER', type(v) # v.encode('string_escape')
                setattr(self, attr_name, v)
                #setattr(self, attr_name, attr_value)
        except UnicodeDecodeError:
            print "Failed to decode: {0}".format(field_values)
            raise

        # Lists of strings explaining errors and warnings associated with this data row
        self.errors = []
        self.warnings = []

    @property
    def new_table_class(self):
       return globals()[self.__class__.new_table_name]

    @property
    def is_valid(self):
        return not self.errors

    def validate(self):
        pass

    def fixup(self):
        for field in self.field_names:
            a = getattr(self, field)
            if a == '':
                setattr(self, field, None)

    @property
    def pk(self):
        try:
            return int(getattr(self, self.field_names[0]))
        except:
            print "Failed to get pk for {0}".format(self)
            raise

    @property
    def table_name(self):
        return self.__class__.__name__[4:]

    def __str__(self):
        return ", ".join("'{0}': {1}".format(k, v) for k, v in vars(self).iteritems())

    def _validate_float(self, field_name):
        a = getattr(self, field_name)
        try:
            f = float(a)
        except:
            self.errors.append("{0} must be a float (value = {1})".format(field_name, a))

    def _validate_integer(self, field_name):
        a = getattr(self, field_name)
        if a is None or not a.strip() or int(a) < 0:
            self.errors.append("{0} must be an integer (value = {1})".format(field_name, a))

    def _validate_positive_integer(self, field_name):
        a = getattr(self, field_name)
        if a is None or not a.strip() or int(a) <= 0:
            self.errors.append("{0} must be a positive integer (value = {1})".format(field_name, a))

    def _validate_not_null(self, field_name):
        a = getattr(self, field_name)
        if a is None:
            self.errors.append("{0} cannot be null".format(field_name))

    def _validate_not_empty(self, field_name):
        a = getattr(self, field_name)
        if a is None or not a.strip():
            self.errors.append("{0} cannot be null or empty".format(field_name))
            return 1
        return 0

    def _validate_option(self, field_name, options):
        a = getattr(self, field_name)
        if not a in options:
            self.errors.append("{0} must be one of {1} (value = {2})".format(field_name, options, a))

    def _validate_boolean(self, field_name):
        a = getattr(self, field_name)
        if a != 'True' and a != 'False':
            self.errors.append("{0} must be a boolean value (value = {1})".format(field_name, a))

    def _validate_date(self, field_name):
        a = getattr(self, field_name)
        try:
            datetime.strptime(a, old_date_format)
        except:
            self.errors.append("{0} must be a date in the format dd/mm/yyyy (value = {1})".format(field_name, a))

    def _validate_time(self, field_name):
        a = getattr(self, field_name)
        try:
            datetime.strptime(a, old_time_format1)
        except:
            try:
                datetime.strptime(a, old_time_format2)
            except:
                self.errors.append("{0} must be a time in the format hh:MM:ss or hh:MM (value = {1})".format(field_name, a))

    def _get_foreign_key(self, new_tables, new_table_name, field_name):
        old_fk = int(getattr(self, field_name))
        if new_tables[new_table_name].has_key(old_fk):
            return new_tables[new_table_name][old_fk].model.pk
        else:
            self.errors.append("Could not find new {0} with primary key matching {1} value of {2}".format(new_table_name, field_name, old_fk))
            return None


class Old_Match_Players(Old_Table_Entry):
    field_names = ('Match_Player_ID', 'Match_ID', 'Player', 'MOM', 'LOM', 'Goals_Scored', 'Report_Link', 'MOM_Comment', 'LOM_Comment', 'Played', 'Own_Goals')
    new_table_name = 'Appearance'

    mom_id = MatchAward.objects.MOM().pk
    lom_id = MatchAward.objects.LOM().pk

    def existing_check(self, new_row):
        return { "member":new_row.member, "match":new_row.match }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        self.MOM = str(math.ceil(float(self.MOM)))
        self.LOM = str(math.ceil(float(self.LOM)))
        if self.MOM_Comment is None:
            self.MOM_Comment = ''
        if self.LOM_Comment is None:
            self.LOM_Comment = ''
        if self.Own_Goals == '' or self.Own_Goals is None:
            self.Own_Goals = 0

        # TEMP
        #self.MOM_Comment = ''
        #self.LOM_Comment = ''

    def validate(self):
        self._validate_positive_integer('Match_Player_ID')
        self._validate_positive_integer('Match_ID')
        self._validate_positive_integer('Player')
        self._validate_float('MOM')
        self._validate_float('LOM')
        self._validate_integer('Goals_Scored')
        self._validate_boolean('Played')
        if self.Player in (Old_Players.guest_id, Old_Players.anon_id):
            self.errors.append("Cannot add appearance for a guest or annonymous player")

    def convert(self, new_tables, pre_req):
        new_match_player = Appearance()
        new_match_player.member_id = self._get_foreign_key(new_tables, 'Member', 'Player')
        new_match_player.match_id = self._get_foreign_key(new_tables, 'Match', 'Match_ID')
        if new_match_player.match_id is None:
            return None
        new_match_player.goals = self.Goals_Scored
        new_match_player.own_goals = self.Own_Goals
        if int(float(self.MOM)) > 0:
            MatchAwardWinner.objects.get_or_create(member_id=new_match_player.member_id, match_id=new_match_player.match_id, award_id=Old_Match_Players.mom_id, comment=self.MOM_Comment)
        if int(float(self.LOM)) > 0:
            MatchAwardWinner.objects.get_or_create(member_id=new_match_player.member_id, match_id=new_match_player.match_id, award_id=Old_Match_Players.lom_id, comment=self.LOM_Comment)
        if self.Played == 'True':
           return new_match_player


class Old_Match_Reports(Old_Table_Entry):
    field_names = ('Match_Date', 'Report_Link')

    @property
    def pk(self):
        # Override as we don't want to return an int
        return self.Match_Date


class Old_Matches(Old_Table_Entry):
    field_names = ('Match_ID','Match_Date','Match_Type','CSHC_Team_ID','Opposition_Team_ID','Match_Time',
                   'Venue_ID','Home_Away','CSHC_Score','Opposition_Score','CSHC_Score_Half','Opposition_Score_Half',
                   'Walkover','Ignore_For_Southerners','Ignore_For_Goal_Kings','Match_Report','Short_Comment',
                   'Include_Even_If_Off','Exclude_From_Roster','Fee_Adjust','GPG_Pro_Rata_Value','IncludeForFantasy',
                   'Override_Kit_Clash','Own_Goals_For')

    new_table_name = 'Match'

    def __init__(self, field_values):
        Old_Table_Entry.__init__(self, field_values)
        self.is_cancelled = False

    def existing_check(self, new_row):
        # WARNING: This assumes a CSHC team only plays a particular opposition team once on a given date (in a particular
        # fixture type)
        return { "our_team_id":new_row.our_team_id, "date":new_row.date, "fixture_type":new_row.fixture_type }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Match_Time:
            self.Match_Time = self.Match_Time.replace('.', ':')
        if self.Match_Time == 'TBC' or self.Match_Time == 'TBA':
            #self.warnings.append("'{0}' time set to null".format(self.Match_Time))
            self.Match_Time = None
        if self.Venue_ID in ('0', '-1'):
            # Issue #20 - no need to warn, just silently fix this up
            #self.warnings.append("Venue_ID value '0' set to null")
            self.Venue_ID = None
        if self.CSHC_Score == 'OFF' or self.CSHC_Score == 'NR':
            # If its not a walkover we assume it was cancelled
            self.is_cancelled = not self.Walkover == 'True'
            self.CSHC_Score = None
            self.Opposition_Score = None
        if self.Home_Away == '??':
            self.Home_Away = 'Away'
        # Tidy up/sanitize match report HTML
        if self.Match_Report is not None:
            self.Match_Report = '<p>' + self.Match_Report.lstrip('<p>').rstrip('\n').replace('\n', '</p><p>') + '</p>'
            # Add support for 'excerpt' from a match report (ref https://github.com/carljm/django-model-utils#splitfield)
            self.Match_Report = self.Match_Report.replace('</p><p>', '</p>\r\n{}\r\n<p>'.format(settings.SPLIT_MARKER), 1)

            # Correct urls to media
            self.Match_Report = self.Match_Report.replace('cambridgesouthhockeyclub.co.uk/media/', 'cambridgesouthhockeyclub.co.uk/static/media/')

        # TEMP
        #self.Match_Report = ''

    def validate(self):
        self._validate_positive_integer('Match_ID')
        self._validate_date('Match_Date')
        self._validate_option('Match_Type', ('Friendly', 'Cup', 'League'))
        self._validate_positive_integer('CSHC_Team_ID')
        self._validate_positive_integer('Opposition_Team_ID')
        if self.Match_Time is not None:
            self._validate_time('Match_Time')
        if self.Venue_ID is not None:
            self._validate_positive_integer('Venue_ID')
        self._validate_option('Home_Away', ('Home', 'Away'))
        if self.CSHC_Score is not None:
            self._validate_integer('CSHC_Score')
            if self.Opposition_Score is not None:
                self._validate_integer('Opposition_Score')
            if self.CSHC_Score_Half is not None:
                self._validate_integer('CSHC_Score_Half')
            if self.Opposition_Score_Half is not None:
                self._validate_integer('Opposition_Score_Half')
        self._validate_boolean('Walkover')
        self._validate_boolean('Ignore_For_Southerners')
        self._validate_boolean('Ignore_For_Goal_Kings')
        self._validate_boolean('Exclude_From_Roster')
        self._validate_boolean('Override_Kit_Clash')
        if self.Own_Goals_For is not None:
            self._validate_integer('Own_Goals_For')

        # You can't specify one score without the other
        if((self.CSHC_Score != None and self.Opposition_Score == None) or
            (self.CSHC_Score == None and self.Opposition_Score != None)):
            self.errors.append("Both scores must be provided")

        # ...same goes for half time scores
        if((self.CSHC_Score_Half != None and self.Opposition_Score_Half == None) or
            (self.CSHC_Score_Half == None and self.Opposition_Score_Half != None)):
            self.errors.append("Both half-time scores must be provided")

        # The opposition can't score more own goals than our total score
        if(self.CSHC_Score != None and self.Own_Goals_For != None and
            int(self.Own_Goals_For) > int(self.CSHC_Score)):
            self.errors.append("Too many opposition own goals")

        # Half-time scores must be <= the final scores
        if(self.CSHC_Score_Half != None and self.Opposition_Score_Half != None and self.CSHC_Score != None and self.Opposition_Score != None):
            if(int(self.CSHC_Score_Half) > int(self.CSHC_Score) or
                int(self.Opposition_Score_Half) > int(self.Opposition_Score)):
                self.errors.append("Half-time scores cannot be greater than final scores")

        for error in self.errors:
            print "ERROR:   {0}[{1}] {2}".format('Matches', self.Match_ID, error)



    def convert(self, new_tables, pre_req):
        new_match = Match()
        # Exceptions to the rule
        if self.Opposition_Team_ID == Old_Opposition_Club_Teams.bye_id:
            self.warnings.append("Skipped BYE cup match")
            return None
        elif self.Opposition_Team_ID == Old_Opposition_Club_Teams.tournament_id:
            self.warnings.append("Skipped tournament match")
            return None
        elif self.Opposition_Team_ID == Old_Opposition_Club_Teams.tba_id:
            self.warnings.append("Skipped match where the opposition team is TBA")
            return None
        new_match.our_team_id = self._get_foreign_key(new_tables, 'ClubTeam', 'CSHC_Team_ID')
        new_match.opp_team_id = self._get_foreign_key(new_tables, 'Team', 'Opposition_Team_ID')
        if self.Venue_ID is not None:
            new_match.venue_id = self._get_foreign_key(new_tables, 'Venue', 'Venue_ID')
        new_match.home_away = Match.HOME_AWAY.Home if self.Home_Away == 'Home' else Match.HOME_AWAY.Away
        new_match.fixture_type = getattr(Match.FIXTURE_TYPE, self.Match_Type)
        new_match.date = datetime.strptime(self.Match_Date, old_date_format)
        if self.Match_Time is not None:
            try:
                new_match.time = datetime.strptime(self.Match_Time, old_time_format1).time()
            except:
                new_match.time = datetime.strptime(self.Match_Time, old_time_format2).time()
        if self.Walkover == 'True':
            new_match.alt_outcome = Match.ALTERNATIVE_OUTCOME.Walkover
        elif self.is_cancelled:
            new_match.alt_outcome = Match.ALTERNATIVE_OUTCOME.Cancelled
        if self.CSHC_Score is not None:
            new_match.our_score = int(self.CSHC_Score)
        if self.Opposition_Score is not None:
            new_match.opp_score = int(self.Opposition_Score)
        if self.CSHC_Score_Half is not None:
            new_match.our_ht_score = int(self.CSHC_Score_Half)
        if self.Opposition_Score_Half is not None:
            new_match.opp_ht_score = int(self.Opposition_Score_Half)
        if self.Own_Goals_For is not None:
            new_match.opp_own_goals = int(self.Own_Goals_For)
        if self.Short_Comment is not None:
            new_match.report_title = self.Short_Comment
        if self.Match_Report is not None:
            new_match.report_body = self.Match_Report
        new_match.ignore_for_goal_king = True if self.Ignore_For_Goal_Kings == 'True' else False
        new_match.ignore_for_southerners = True if self.Ignore_For_Southerners == 'True' else False
        new_match.override_kit_clash = True if self.Override_Kit_Clash == 'True' else False
        if self.GPG_Pro_Rata_Value is not None:
            new_match.gpg_pro_rata = float(self.GPG_Pro_Rata_Value)
        # TEMP - set match report to None to try and get it through the conversion
        #new_match.report_body = ''
        return new_match


class Old_Opposition_Club_Teams(Old_Table_Entry):
    field_names = ('Team_ID', 'Team_Name', 'Club_ID', 'Short_Name', 'Sex')
    new_table_name = 'Team'

    bye_id = None
    tournament_id = None
    tba_id = None

    cheshunt_club_id = None

    def existing_check(self, new_row):
        return { "name":new_row.name }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Team_Name == 'BYE':
            Old_Opposition_Club_Teams.bye_id = self.Team_ID
            self.errors.append("'BYE' team ignored (but Team_ID cached for use when checking references to this 'team')")
        if self.Team_Name == 'Tournament':
            Old_Opposition_Club_Teams.tournament_id = self.Team_ID
            self.errors.append("'Tournament' team ignored (but Team_ID cached for use when checking references to this 'team')")
        if self.Team_Name == 'TBA':
            Old_Opposition_Club_Teams.tba_id = self.Team_ID
            self.errors.append("'TBA' team ignored (but Team_ID cached for use when checking references to this 'team')")
        if self.Team_ID == '73':
            self.errors.append("Ignoring duplicate entry for March Town 2")

    def validate(self):
        self._validate_positive_integer('Team_ID')
        self._validate_not_empty('Team_Name')
        self._validate_positive_integer('Club_ID')
        self._validate_option('Sex', ('Men', 'Ladies', 'Mixed'))

    def convert(self, new_tables, pre_req):
        new_team = Team()
        new_team.club_id = self._get_foreign_key(new_tables, 'Club', 'Club_ID')
        if self.Sex == 'Men':
            new_team.gender = TeamGender.Mens
        elif self.Sex == 'Ladies':
            new_team.gender = TeamGender.Ladies
        else:
            new_team.gender = TeamGender.Mixed
        new_team.name = self.Team_Name
        new_team.short_name = self.Short_Name
        return new_team


class Old_Opposition_Clubs(Old_Table_Entry):
    field_names = ('Club_Id', 'Club_Name', 'Club_Short_Name', 'Club_Link_Name', 'Default_Venue', 'Kit_Clash_Men', 'Kit_Clash_Ladies', 'Kit_Clash_Mixed', 'Mens_Fixtures')
    new_table_name = 'Club'

    none_id = None

    def existing_check(self, new_row):
        return { "name":new_row.name }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Default_Venue <= 0:
            self.Default_Venue = None
        if self.Club_Name == 'None':
            Old_Opposition_Clubs.none_id = self.Club_Id
            self.errors.append("'None' club ignored (but Club_Id cached for use when checking references to this 'club')")

    def validate(self):
        self._validate_positive_integer('Club_Id')
        if self.Default_Venue is not None:
            self._validate_positive_integer('Default_Venue')
        self._validate_not_empty('Club_Name')
        self._validate_boolean('Kit_Clash_Men')
        self._validate_boolean('Kit_Clash_Ladies')
        self._validate_boolean('Kit_Clash_Mixed')

    def convert(self, new_tables, pre_req):
        new_club = Club()
        new_club.name = self.Club_Name
        new_club.kit_clash_men = self.Kit_Clash_Men == 'True'
        new_club.kit_clash_ladies = self.Kit_Clash_Ladies == 'True'
        new_club.kit_clash_mixed = self.Kit_Clash_Mixed == 'True'
        if self.Default_Venue is not None:
            default_venue_id = self._get_foreign_key(new_tables, 'Venue', 'Default_Venue')
            if default_venue_id is None:
                return None
            else:
                new_club.default_venue_id = default_venue_id
        return new_club



class Old_Players(Old_Table_Entry):
    field_names = ('Player_ID', 'First_Name', 'Surname', 'Position', 'Short_First_Name', 'Short_Surname', 'Sex', 'xClub_Squad')
    new_table_name = 'Member'

    anon_id = None
    guest_id = None

    def existing_check(self, new_row):
        return { "first_name":new_row.first_name, "last_name":new_row.last_name }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Surname == 'Anon':
            self.errors.append("Ignoring player 'Anon' (but storing Player_ID for referencing later)")
            Old_Players.anon_id = self.Player_ID
        elif self.Surname == 'Guest':
            self.errors.append("Ignoring player 'Guest' (but storing Player_ID for referencing later)")
            Old_Players.guest_id = self.Player_ID
        elif self.Surname == 'Jorge':
            self.errors.append("Ignoring player 'Jorge' with no first name. Not referenced.")
        elif self.Surname == 'Phillippa':
            self.warnings.append("'Phillipa' has no surname. Setting to '???'.")
            self.First_Name = 'Phillippa'
            self.Surname = '???'
            self.Sex = 'Female'
        elif self.Surname == 'Joyce':
            self.warnings.append("'Joyce' has no first. Setting to '???'.")
            self.First_Name = 'Joyce'
            self.Surname = '???'
            self.Sex = 'Female'
        elif not self.First_Name:
            self.warnings.append("'{}' has no first name. Setting to '???'.".format(self.Surname))
            self.First_Name = '???'

    def validate(self):
        self._validate_positive_integer('Player_ID')
        self._validate_not_empty('First_Name')
        self._validate_not_empty('Surname')
        self._validate_option('Sex', ('Male', 'Female'))
        self._validate_option('Position', ('GK', 'Def', 'Mid', 'Fwd', 'Def/Mid', 'Mid/Fwd', 'Other', 'GK/Def', 'GK/Mid', 'GK/Fwd'))

    def convert(self, new_tables, pre_req):
        new_player = Member()
        new_player.first_name = self.First_Name
        new_player.last_name = self.Surname
        new_player.gender = getattr(Member.GENDER, self.Sex)
        new_player.pref_position = getattr(Member.POSITION, self.Position.replace('/', '_'))
        return new_player


class Old_Positions(Old_Table_Entry):
    field_names = ('Position', 'Order')

    @property
    def pk(self):
        # Override as we don't want to return an int
        return self.Position


class Old_Seasons(Old_Table_Entry):
    field_names = ('Season_ID', 'Season_Name', 'Start_Date', 'End_Date', 'Link_To_Rivals_Report', 'Default_Pitch_Hire', 'Default_Teas_Cost', 'Fuel_Per_Mile')
    new_table_name = 'Season'

    def existing_check(self, new_row):
        return { "start":new_row.start }

    def validate(self):
        self._validate_positive_integer('Season_ID')
        self._validate_date('Start_Date')
        self._validate_date('End_Date')

    def convert(self, new_tables, pre_req):
        new_season = Season()
        new_season.start = datetime.strptime(self.Start_Date, old_date_format)
        new_season.end = datetime.strptime(self.End_Date, old_date_format)
        return new_season



class Old_Team_Seasons(Old_Table_Entry):
    field_names = ('Team_Season_ID', 'Team', 'Season', 'League_Division', 'League_Position', 'Teams_In_League', 'Cup_Position', 'Pay_Fuel', 'Drivers_Free')
    new_table_name = 'ClubTeamSeasonParticipation'

    def existing_check(self, new_row):
        return { "team":new_row.team, "season":new_row.season }

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Cup_Position:
            self.Cup_Position = self.Cup_Position.replace('First Round', '1st Round')
            self.Cup_Position = self.Cup_Position.replace('Second Round', '2nd Round')
            if self.Cup_Position == 'N/A':
                self.Cup_Position = None

        # Treat Printwize league as East League
        if self.League_Division:
            self.League_Division = self.League_Division.lstrip('Printwize ')

    def validate(self):
        self._validate_positive_integer('Team_Season_ID')
        self._validate_positive_integer('Team')
        self._validate_positive_integer('Season')

    def convert(self, new_tables, pre_req):
        new_teamseason = ClubTeamSeasonParticipation()
        new_teamseason.team_id = self._get_foreign_key(new_tables, 'ClubTeam', 'Team')
        new_teamseason.season_id = self._get_foreign_key(new_tables, 'Season', 'Season')
        if self.League_Division is not None:
            if self.League_Division.find('East League') != -1:
                division = self.League_Division.lstrip('East League ')
            elif self.League_Division.find('Cambs League') != -1:
                division = self.League_Division.lstrip('Cambs League ')
            elif self.League_Division.find('Crowe Insurance') != -1:
                division = self.League_Division.lstrip('Crowe Insurance ')
            new_teamseason.division_id = pre_req['Division'][division].pk

        return new_teamseason


class Old_Teams(Old_Table_Entry):
    field_names = ('Team_ID','Team_Name','Sex','Fill_Blanks','Long_Name','Medium_Name','Position','Link','Anchor','Southerners','Rivals','Use_For_Personal_Stats')
    new_table_name = 'ClubTeam'

    def existing_check(self, new_row):
        return { "short_name":new_row.short_name }

    def validate(self):
        self._validate_positive_integer('Team_ID')
        self._validate_not_empty('Team_Name')
        self._validate_option('Sex', ('Men', 'Ladies', 'Mixed'))
        self._validate_boolean('Fill_Blanks')

    def convert(self, new_tables, pre_req):
        # New teams are already collected in the pre-requisites
        return pre_req['ClubTeam'][self.Team_Name]


class Old_Venues(Old_Table_Entry):
    field_names = ('Venue_ID','Venue_Name','Venue_Display','Venue_Link','Venue_Distance','Venue_PostCode','Venue_LongName','xVenue_PitchCost','Venue_Short_Name')
    new_table_name = 'Venue'

    tbc_id = None

    def existing_check(self, new_row):
        return { "name":new_row.name }

    def validate(self):
        self._validate_positive_integer('Venue_ID')
        self._validate_not_empty('Venue_Name')

    def fixup(self):
        Old_Table_Entry.fixup(self)
        if self.Venue_Name == 'TBC':
            Old_Venues.tbc_id = self.Venue_ID
            self.errors.append("'TBC' venue ignored (but Venue_ID cached for use when checking references to this 'venue')")
        if not self.Venue_Short_Name:
            self.Venue_Short_Name = self.Venue_Name
        if not self.Venue_LongName:
            self.Venue_LongName = self.Venue_Name
        if not self.Venue_Link or 'wblink' in self.Venue_Link:
            self.Venue_Link = ''
        if not self.Venue_PostCode:
            self.Venue_PostCode = ''

    def convert(self, new_tables, pre_req):
        new_venue = Venue()
        new_venue.name = self.Venue_LongName
        new_venue.short_name = self.Venue_Short_Name
        new_venue.url = self.Venue_Link
        new_venue.addr_postcode = self.Venue_PostCode
        new_venue.distance = int(float(self.Venue_Distance))
        if new_venue.name in ('The Leys School', 'Coldhams Common', 'Wilberforce Road', 'St Catharine\'s College', 'St John\'s College'):
            new_venue.is_home = True
            # HACK: The short names for home venues are stored in the Venue_Display field!
            new_venue.short_name = self.Venue_Display
        return new_venue