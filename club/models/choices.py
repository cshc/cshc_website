

TEAM_GENDER = (
    (u'M', u'Mens'),
    (u'L', u'Ladies'),
    (u'ML', u'Mixed'),
)

PLAYER_GENDER = (
    (u'M', u'Male'),
    (u'L', u'Female'),
)

ORDINAL = (
    (u'1', u'1sts'),
    (u'2', u'2nds'),
    (u'3', u'3rds'),
    (u'4', u'4ths'),
    (u'5', u'5ths'),
    (u'6', u'6ths'),
    (u'7', u'7ths'),
    (u'8', u'8ths'),
    (u'9', u'9ths'),
    (u'10', u'10ths'),
    (u'11', u'11ths'),
    (u'12', u'12ths'),
    (u'V', u'Vets'),
    (u'0', u'Other'),
)
    
HOME_AWAY = (
    (u'H', u'Home'),
    (u'A', u'Away'),
)

FIXTURE_TYPE = (
    (u'F', u'Friendly'),
    (u'L', u'League'),
    (u'C', u'Cup'),
)

MATCH_OUTCOME = (
    (u'Pe', u'Pending'),
    (u'Pl', u'Played'),
    (u'Po', u'Postponed'),
    (u'Ca', u'Cancelled'),
    (u'Wa', u'Walkover'),
)

PLAYER_POSITION = (
    (u'GK', u'Goalkeeper'),
    (u'DEF', u'Defender'),
    (u'MID', u'Midfield'),
    (u'FWD', u'Forward'),
    (u'???', u'Not known'),
)

CUP_RESULT = (
    (u'DNP', u'Did not participate'),   # Did not participate in the cup
    (u'1', u'1st round'),               # Reached (knocked out in) the 1st round
    (u'2', u'2nd round'),               # Reached (knocked out in) the 2nd round
    (u'3', u'3rd round'),               # Reached (knocked out in) the 3rd round
    (u'4', u'4th round'),               # Reached (knocked out in) the 4th round
    (u'5', u'5th round'),               # Reached (knocked out in) the 5th round
    (u'6', u'6th round'),               # Reached (knocked out in) the 6th round
    (u'Q', u'Quarter Final'),           # Reached the quarter final
    (u'S', u'Semi Final'),              # Reached the semi final
    (u'3P', u'3rd Place'),              # Won the 3rd place playoff
    (u'F', u'Final'),                   # Reached the final
    (u'W', u'Winner'),                  # Won the cup
)

AWARD_TYPE = (
    (u'MOM', u'Man of the Match'),
    (u'LOM', u'Lemon of the Match'),
)