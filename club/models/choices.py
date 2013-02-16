# This file contains classes which encapsulate choices for various model fields
# Each class defines variables for the different choices and a CHOICES tuple
# to use as the choices parameter for a model field

class TeamGender:
    MENS = u'M'
    LADIES = u'L'
    MIXED = u'ML'

    CHOICES = (
        (MENS, u'Mens'),
        (LADIES, u'Ladies'),
        (MIXED, u'Mixed'),
    )

class PlayerGender:
    MALE = u'M'
    FEMALE = u'L'

    CHOICES = (
        (MALE, u'Male'),
        (FEMALE, u'Female'),
    )

class TeamOrdinal:
    T1 = u'1'
    T2 = u'2'
    T3 = u'3'
    T4 = u'4'
    T5 = u'5'
    T6 = u'6'
    T7 = u'7'
    T8 = u'8'
    T9 = u'9'
    T10 = u'10'
    T11 = u'11'
    T12 = u'12'
    T_VETS = u'V'
    T_OTHER = u'0'

    CHOICES = (
        (T1, u'1sts'),
        (T2, u'2nds'),
        (T3, u'3rds'),
        (T4, u'4ths'),
        (T5, u'5ths'),
        (T6, u'6ths'),
        (T7, u'7ths'),
        (T8, u'8ths'),
        (T9, u'9ths'),
        (T10, u'10ths'),
        (T11, u'11ths'),
        (T12, u'12ths'),
        (T_VETS, u'Vets'),
        (T_OTHER, u'Other'),
    )
    
class HomeAway:
    HOME = u'H'
    AWAY = u'A'

    CHOICES = (
        (HOME, u'Home'),
        (AWAY, u'Away'),
    )

class FixtureType:
    FRIENDLY = u'F'
    LEAGUE = u'L'
    CUP = u'C'

    Friendly_display = u'Friendly'
    League_display = u'League'
    Cup_display = u'Cup'

    CHOICES = (
        (FRIENDLY, Friendly_display),
        (LEAGUE, League_display),
        (CUP, Cup_display),
    )

class MatchOutcome:
    PENDING = u'Pe'
    PLAYED = u'Pl'
    POSTPONED = u'Po'
    CANCELLED = u'Ca'
    WALKOVER = u'Wa'

    CHOICES = (
        (PENDING, u'Pending'),
        (PLAYED, u'Played'),
        (POSTPONED, u'Postponed'),
        (CANCELLED, u'Cancelled'),
        (WALKOVER, u'Walkover'),
    )

class PlayerPosition:
    GOALKEEPER = u'GK'
    DEFENDER = u'DEF'
    MIDFIELDER = u'MID'
    FORWARD = u'FWD'
    NOT_KNOWN = u'???'

    CHOICES = (
        (GOALKEEPER, u'Goalkeeper'),
        (DEFENDER, u'Defender'),
        (MIDFIELDER, u'Midfielder'),
        (FORWARD, u'Forward'),
        (NOT_KNOWN, u'Not known'),
    )

class CupResult:
    DID_NOT_PARTICIPATE = u'DNP'
    ROUND_1 = u'1'
    ROUND_2 = u'2'
    ROUND_3 = u'3'
    ROUND_4 = u'4'
    ROUND_5 = u'5'
    ROUND_6 = u'6'
    QUARTER_FINAL = u'Q'
    SEMI_FINAL = u'S'
    THIRD_PLACE = u'3P'
    FINAL = u'F'
    WINNER = u'W'

    CHOICES = (
        (DID_NOT_PARTICIPATE, u'Did not participate'),   # Did not participate in the cup
        (ROUND_1, u'1st round'),               # Reached (knocked out in) the 1st round
        (ROUND_2, u'2nd round'),               # Reached (knocked out in) the 2nd round
        (ROUND_3, u'3rd round'),               # Reached (knocked out in) the 3rd round
        (ROUND_4, u'4th round'),               # Reached (knocked out in) the 4th round
        (ROUND_5, u'5th round'),               # Reached (knocked out in) the 5th round
        (ROUND_6, u'6th round'),               # Reached (knocked out in) the 6th round
        (QUARTER_FINAL, u'Quarter Final'),           # Reached the quarter final
        (SEMI_FINAL, u'Semi Final'),              # Reached the semi final
        (THIRD_PLACE, u'3rd Place'),              # Won the 3rd place playoff
        (FINAL, u'Final'),                   # Reached the final
        (WINNER, u'Winner'),                  # Won the cup
    )

class CupRound:
    ROUND_1 = u'1'
    ROUND_2 = u'2'
    ROUND_3 = u'3'
    ROUND_4 = u'4'
    ROUND_5 = u'5'
    ROUND_6 = u'6'
    QUARTER_FINAL = u'Q'
    SEMI_FINAL = u'S'
    THIRD_PLACE = u'3P'
    FINAL = u'F'

    CHOICES = (
        (ROUND_1, u'1st round'),               # Reached (knocked out in) the 1st round
        (ROUND_2, u'2nd round'),               # Reached (knocked out in) the 2nd round
        (ROUND_3, u'3rd round'),               # Reached (knocked out in) the 3rd round
        (ROUND_4, u'4th round'),               # Reached (knocked out in) the 4th round
        (ROUND_5, u'5th round'),               # Reached (knocked out in) the 5th round
        (ROUND_6, u'6th round'),               # Reached (knocked out in) the 6th round
        (QUARTER_FINAL, u'Quarter Final'),           # Reached the quarter final
        (SEMI_FINAL, u'Semi Final'),              # Reached the semi final
        (THIRD_PLACE, u'3rd Place'),              # Won the 3rd place playoff
        (FINAL, u'Final'),                   # Reached the final
    )

class AwardType:
    MOM = u'MOM'
    LOM = u'LOM'

    CHOICES = (
        (MOM, u'Man of the Match'),
        (LOM, u'Lemon of the Match'),
    )