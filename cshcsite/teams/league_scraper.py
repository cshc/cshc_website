"""
This module contains functions and classes used to scrape the league's website to extract league tables in a
format that can be used by our own template files to render the league tables on our site.
"""
import logging
import re
from urllib import urlopen
from bs4 import BeautifulSoup
from competitions.models import DivisionResult
from core.models import TeamGender
from teams.models import ClubTeam
from opposition.models import Team

log = logging.getLogger(__name__)


def parse_url(url):
    """ Reads the contents of specified url and returns a BeautifulSoup object that wraps it"""
    source = urlopen(url).read()
    return BeautifulSoup(source)

def get_east_leagues_nw_division(url, division, season):
    """Returns a ScrapedDivision object with the scraped league table from the specified url who's name matches
    the div_name parameter."""
    print url
    print division.name
    soup = parse_url(url)
    div_name = division.name.upper()
    # Hack: women's leagues slightly different
    if division.gender == TeamGender.Ladies:
        div_name = div_name.lstrip('DIVISION').rstrip('DIVISION').strip()
    # The first html row of the division is the one containing the division name
    div_row = soup.find(text=div_name).find_parent('tr')
    current_row = div_row.find_next('tr')
    # Find the next division - we'll need to stop before this point.
    # Account for the lowest division which won't have another one below it
    try:
        bottom = current_row.find_next('strong').find_parent('tr')
    except:
        bottom = None
    teams = []
    pos = 0
    while current_row != bottom:
        columns = current_row('td')
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
            team.points = int(columns[9].text) if columns[9].text else 0
            # The 11th column is not used!
            team.notes = columns[11].text
            team.save()
            teams.append(team)
            print "Parsed team: {}".format(team)
        try:
            current_row = current_row.find_next('tr')
        except:
            current_row = None

    return teams

def set_team(team, name, division):

    try:
        if name.startswith('Cambridge South '):
            ordinal = name.lstrip('Cambridge South ')
            gender = 'M' if division.gender == TeamGender.Mens else 'L'
            slug = gender + ordinal
            team.our_team = ClubTeam.objects.get(slug=slug.lower())
            team.opp_team = None
        else:
            if division.gender == TeamGender.Ladies:
                words = name.split()
                if 'Ladies' not in words:
                    words.insert(-1, 'Ladies')
                name = " ".join(words)
            team.opp_team = Team.objects.get(name=name)
            team.our_team = None
    except (Team.DoesNotExist, ClubTeam.DoesNotExist):
        log.error("Could not find team '{}'".format(name))


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