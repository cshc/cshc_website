""" Represents the playing record of a particular CSHC team in a particular season.

    This is another 'cache' model - the data is derived from other models but
    is calculated and stored in this database table for efficiency. A nightly
    cronjob task updates the Southerners statistics automatically - so the Southerner
    model is not accessible from the admin interface and should never be manually
    edited.
"""

from django.db import models
from teams.models import ClubTeam
from competitions.models import Season


class SouthernerManager(models.Manager):
    """ Model manager for the Southerner model"""

    def get_query_set(self):
        """ Gets the QuerySet, also selecting the related team and season models"""
        return super(SouthernerManager, self).get_query_set().select_related('team', 'season')

    def by_season(self, season):
        """ Filters the Southerner entries by the specified season - and orders them
            in descending average points per game.
        """
        return self.get_query_set().filter(season=season).order_by('-avg_points_per_game')


class Southerner(models.Model):
    """ Represents a Southerner League Table entry.
        Note: This is a derivative model which is calculated and updated for reasons of efficiency.
        It should never be manually edited (any manual adjustments will be overridden the next time
        the update is run).
    """
    # The team this entry applies to
    team = models.ForeignKey(ClubTeam)

    # The season this entry applies to
    season = models.ForeignKey(Season)

    won = models.PositiveSmallIntegerField("Total number of games won", default=0)
    drawn = models.PositiveSmallIntegerField("Total number of games drawn", default=0)
    lost = models.PositiveSmallIntegerField("Total number of games lost", default=0)

    goals_for = models.PositiveSmallIntegerField("Goals For", default=0)
    goals_against = models.PositiveSmallIntegerField("Goals Against", default=0)

    result_points = models.PositiveSmallIntegerField("Result points", default=0)
    bonus_points = models.SmallIntegerField("Bonus points", default=0)

    # These are attributes (db fields) rather than just methods so that we can take advantage of
    # SQL ordering - we typically want to order Southerners entries by average points per game.
    avg_points_per_game = models.FloatField("Average points per game", editable=False)

    class Meta:
        """ Meta-info for the Southerner model. """
        app_label = 'teams'
        unique_together = ('team', 'season')
        ordering = ['season', 'avg_points_per_game']


    objects = SouthernerManager()

    def clean(self):
        # Calculate non-editable, derived fields
        self.avg_points_per_game = (float)(self.total_points()) / (float)(self.played())

    def __unicode__(self):
        return unicode("{} - {}".format(self.team, self.season))

    def played(self):
        """ Returns the total number of games played by this team in this season"""
        return self.won + self.drawn + self.lost

    def total_points(self):
        """ Returns the total number of points (combined results and bonus)"""
        return self.result_points + self.bonus_points

    def reset(self):
        """ Resets all statistics. """
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.result_points = 0
        self.bonus_points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.avg_points_per_game = 0.0

    def add_match(self, match):
        """ Add a match to the tally"""
        assert match.final_scores_provided()
        assert match.season == self.season
        assert match.our_team == self.team

        if match.was_won():
            self.won += 1
            self.result_points += 3
            # Bonus point if we won by more than 2 goals
            if match.our_score > (match.opp_score + 2):
                self.bonus_points += 1
        elif match.was_drawn():
            self.drawn += 1
            self.result_points += 1
        else:
            assert match.was_lost()
            self.lost += 1
            # Negative bonus point if we lost by more than 2 goals
            if match.opp_score > (match.our_score + 2):
                self.bonus_points -= 1

        self.goals_for += match.our_score
        self.goals_against += match.opp_score

