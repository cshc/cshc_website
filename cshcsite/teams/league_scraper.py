""" This module contains functions and classes used to scrape the league's
    website to extract league tables in a format that can be used by our own
    template files to render the league tables on our site.

    WARNING: As the scraping logic relies on the East League's website pages
    sticking to a particular layout, it is prone to go wrong at some point in
    the future when they update their layout! When this breaking change happens,
    you should spot it in the cronjob error report (and in incomplete league
    tables on the CSHC website). You will then need to debug the league scraping
    code and modify it to cope with the new layout of the East League's pages.
"""

import logging
import re
from urllib import urlopen
from bs4 import BeautifulSoup
from django.db.models import Q
from core.models import TeamGender
from competitions.models import DivisionResult
from matches.models import Match
from teams.models import ClubTeam
from opposition.models import Team

LOG = logging.getLogger(__name__)

def parse_url(url):
    """ Reads the contents of specified url and returns a BeautifulSoup object that wraps it"""
    source = urlopen(url).read()
    return BeautifulSoup(source)

def get_east_leagues_division(url, division, season):
    """ Returns a ScrapedDivision object with the scraped league table from the specified
        url who's name matches the division parameter.
    """
    existingTeams = DivisionResult.objects.league_table(season=season, division=division)

    soup = parse_url(url)
    divisionName = division.name.upper()
    divisionElement = soup.find(text=divisionName)
    currentRow = divisionElement.find_next('tr')
    nextDivisionElement = divisionElement.find_next('strong')
    blankRow = divisionElement.find_next(text=u'\xa0')
    bottomRow = nextDivisionElement.find_parent('tr') if nextDivisionElement != None else blankRow.find_parent('tr')
    teams = []
    pos = 0
    while currentRow != bottomRow:
        columns = currentRow('td')
        pos += 1
        team = DivisionResult()
        team.division = division
        team.season = season
        team.position = pos
        name = columns[0].text.strip()
        if '---' not in name and name != '' and name is not None:
            set_team(team, name, division)
            # The 2nd column is not used!
            team.played = int(columns[2].text) if columns[2].text else 0
            team.won = int(columns[3].text) if columns[3].text else 0
            team.drawn = int(columns[4].text) if columns[4].text else 0
            team.lost = int(columns[5].text) if columns[5].text else 0
            team.goals_for = int(columns[6].text) if columns[6].text else 0
            team.goals_against = int(columns[7].text) if columns[7].text else 0
            team.goal_difference = int(columns[8].text) if columns[8].text else 0
            # Some league tables display percentage win instead. In this case calculate the total
            if columns[9].text.endswith('%'):
                team.points = team.won * Match.POINTS_FOR_WIN + team.drawn * Match.POINTS_FOR_DRAW
            else:
                team.points = int(columns[9].text) if columns[9].text else 0
            # The 11th column is not used!
            team.notes = columns[11].text
            teams.append(team)
            LOG.debug("Parsed team: {}".format(team))
        try:
            currentRow = currentRow.find_next('tr')
        except:
            break

    # Only replace existing entries if we've got at least as many entries
    if len(teams) >= len(existingTeams):
        existingTeams.delete();
        for t in teams:
            t.save()
    else:
        LOG.debug("Did not save division results for {}: Only {} teams parsed ({} teams before)".format(url, len(teams), len(existingTeams)))
    return teams

def set_team(team, name, division):
    """ Works out whether the team should be a CSHC team (ClubTeam) or
        an opposition team (Team). Also handles the lack of the text 'Ladies'
        in the team name.
    """

    try:
        if name.startswith('Cambridge South '):
            ordinal = name.lstrip('Cambridge South ')
            slug = division.gender[0] + ordinal
            team.our_team = ClubTeam.objects.get(slug=slug.lower())
            team.opp_team = None
        else:
            # Build the full name by inserting either 'Mens' or 'Ladies' into the name
            # before the ordinal number
            words = name.split()
            if division.gender not in words:
                words.insert(-1, division.gender)
            fullName = " ".join(words)
            # Build the short name by prepending the ordinal number with either 'M' or 'L'
            words = name.split()
            if division.gender in words:
                words.remove(division.gender)
            words[-1] = division.gender[0] + words[-1]
            shortName = " ".join(words)
            name_q = Q(name=fullName) | Q(short_name=shortName)
            team.opp_team = Team.objects.get(name_q)
            team.our_team = None
    except (Team.DoesNotExist, ClubTeam.DoesNotExist):
        LOG.error("Could not find team '{}'".format(name))


# Deprecated:
# def get_east_leagues_cambs_division(url):
#     """Returns a ScrapedDivision object with the scraped league table from the specified url.

#     Note that for Cambs Leagues there is only one division per URL - so no need to pass in
#     the division name."""
#     soup = parse_url(url)

#     div = ScrapedDivision()

#     # The main table is the first html table in the document
#     main_table = soup.table
#     # Find the first row in the table
#     div_row = main_table.tr

#     current_row = div_row.find_next('tr')
#     while current_row != None:
#         columns = current_row('td')
#         team = ScrapedDivisionTeam()
#         team.name = columns[0].div.text
#         team.played = columns[1].div.text
#         team.won = columns[2].div.text
#         team.drawn = columns[3].div.text
#         team.lost = columns[4].div.text
#         team.goals_for = columns[5].div.text
#         team.goals_against = columns[6].div.text
#         team.goal_difference = columns[7].div.text
#         team.points = columns[8].div.text
#         team.notes = columns[9].text
#         div.teams.append(team)
#         current_row = current_row.find_next('tr')

#     return div
