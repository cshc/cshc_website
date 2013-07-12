"""
This module contains functions and classes used to scrape the league's website to extract league tables in a 
format that can be used by our own template files to render the league tables on our site.
"""
import logging
import re
from urllib import urlopen
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


def parse_url(url):
    """ Reads the contents of specified url and returns a BeautifulSoup object that wraps it"""
    source = urlopen(url).read()
    return BeautifulSoup(source)

def get_east_leagues_nw_division(url, div_name):
    """Returns a ScrapedDivision object with the scraped league table from the specified url who's name matches 
    the div_name parameter."""
    print url
    print div_name
    soup = parse_url(url)

    div = ScrapedDivision()

    # The first html row of the division is the one containing the division name
    div_row = soup.find(text=div_name.upper()).find_parent('tr')
    current_row = div_row.find_next('tr')
    # Find the next division - we'll need to stop before this point. 
    # Account for the lowest division which won't have another one below it
    try:
        bottom = current_row.find_next(text=re.compile('DIVISION')).find_parent('tr')
    except:
        bottom = None

    while current_row != bottom:
        #print current_row
        columns = current_row('td')
        team = ScrapedDivisionTeam()
        team.name = columns[0].text
        # The 2nd column is not used!
        team.played = columns[2].text
        team.won = columns[3].text
        team.drawn = columns[4].text
        team.lost = columns[5].text
        team.goals_for = columns[6].text
        team.goals_against = columns[7].text
        team.goal_difference = columns[8].text
        team.points = columns[9].text
        # The 11th column is not used!
        team.notes = columns[11].text
        div.teams.append(team)
        try:
            current_row = current_row.find_next('tr')
        except:
            current_row = None

    return div

def get_old_east_leagues_division(url, div_name):
    """Returns a ScrapedDivision object with the scraped league table from the specified url who's name matches 
    the div_name parameter."""
    print url
    print div_name
    soup = parse_url(url)
    div = ScrapedDivision()

    # Find the header row 
    header_row = soup.find(text='Pl').find_parent('tr')
    rows = header_row.find_next_siblings('tr')

    for current_row in rows:
        columns = current_row('td')
        if current_row.find(text=re.compile('DIVISION')):
            break
        team = ScrapedDivisionTeam()
        team.name = columns[0].text
        team.played = columns[1].text
        team.won = columns[2].text
        team.drawn = columns[3].text
        team.lost = columns[4].text
        team.goals_for = columns[5].text
        team.goals_against = columns[6].text
        team.goal_difference = columns[7].text
        team.points = columns[8].text
        team.notes = columns[9].text    # May be columns[10]
        div.teams.append(team)

    return div


def get_old_east_leagues_nw_division(url, div_name):
    """Returns a ScrapedDivision object with the scraped league table from the specified url who's name matches 
    the div_name parameter."""
    print url
    print div_name
    soup = parse_url(url)
    div = ScrapedDivision()

    # The first html row of the division is the one containing the division name
    header_row = soup.find(text=div_name).find_parent('tr')
    current_row = header_row.find_next('tr')
    # Find the next division - we'll need to stop before this point (there's also a blank line). 
    # Account for the lowest division which won't have another one below it
    try:
        bottom = current_row.find_next(text=re.compile('DIVISION')).find_parent('tr').find_previous('tr')
    except:
        bottom = None

    while current_row != bottom:
        columns = current_row('td')
        team = ScrapedDivisionTeam()
        team.name = columns[0].text
        # The 2nd column is not used!
        team.played = columns[2].text
        team.won = columns[3].text
        team.drawn = columns[4].text
        team.lost = columns[5].text
        team.goals_for = columns[6].text
        team.goals_against = columns[7].text
        team.goal_difference = columns[8].text
        team.points = columns[9].text
        team.notes = columns[10].text
        div.teams.append(team)
        try:
            current_row = current_row.find_next('tr')
        except:
            current_row = None

    return div

def get_east_leagues_cambs_division(url):
    """Returns a ScrapedDivision object with the scraped league table from the specified url.
    
    Note that for Cambs Leagues there is only one division per URL - so no need to pass in 
    the division name."""
    soup = parse_url(url)

    div = ScrapedDivision()

    # The main table is the first html table in the document
    main_table = soup.table
    # Find the first row in the table
    div_row = main_table.tr

    current_row = div_row.find_next('tr')
    while current_row != None:
        columns = current_row('td')
        team = ScrapedDivisionTeam()
        team.name = columns[0].div.text
        team.played = columns[1].div.text
        team.won = columns[2].div.text
        team.drawn = columns[3].div.text
        team.lost = columns[4].div.text
        team.goals_for = columns[5].div.text
        team.goals_against = columns[6].div.text
        team.goal_difference = columns[7].div.text
        team.points = columns[8].div.text
        team.notes = columns[9].text
        div.teams.append(team)
        current_row = current_row.find_next('tr')

    return div



class ScrapedDivision(object):
    """Represents a league table (division) scrapped from another website"""

    def __init__(self):
        self.teams = []


class ScrapedDivisionTeam(object):
    """Represents a single row of a ScrapedDivision league table"""

    def __init__(self):
        self.name = None
        self.played = None
        self.won = None
        self.drawn = None
        self.lost = None
        self.goals_for = None
        self.goals_against = None
        self.goal_difference = None
        self.points = None

    