from members.models import CommitteePosition, CommitteeMembership
from core.models import TeamGender
from competitions.models import Season
from datetime import date

def delete_old():
    CommitteeMembership.objects.all().delete()
    CommitteePosition.objects.all().delete()

def add_committee_positions():
    chairperson = CommitteePosition.objects.create(name="Chairperson", gender=TeamGender.Mixed, index=0)
    secretary = CommitteePosition.objects.create(name="Hon. Secretary", gender=TeamGender.Mixed, index=1)
    treasurer = CommitteePosition.objects.create(name="Hon. Treasurer", gender=TeamGender.Mixed, index=2)
    fix_sec = CommitteePosition.objects.create(name="Fixtures Secretary", gender=TeamGender.Mixed, index=3)
    mens_league_liason = CommitteePosition.objects.create(name="Men's League Liaison Officer", gender=TeamGender.Mixed, index=4)
    ladies_league_liason = CommitteePosition.objects.create(name="Ladies' League Liaison Officer", gender=TeamGender.Mixed, index=5)
    mens_umpire_liaison = CommitteePosition.objects.create(name="Men's Umpires' Liaison Officer", gender=TeamGender.Mixed, index=6)
    ladies_umpire_liaison = CommitteePosition.objects.create(name="Ladies' Umpires' Liaison Officer", gender=TeamGender.Mixed, index=7)
    training = CommitteePosition.objects.create(name="Training Co-ordinator", gender=TeamGender.Mixed, index=8)
    comms = CommitteePosition.objects.create(name="Communications Officer", gender=TeamGender.Mixed, index=9)
    mens_social_sec = CommitteePosition.objects.create(name="Men's Social Secretary", gender=TeamGender.Mixed, index=10)
    ladies_social_sec = CommitteePosition.objects.create(name="Ladies' Social Secretary", gender=TeamGender.Mixed, index=11)
    m1_c = CommitteePosition.objects.create(name="Men's 1st XI Captain", gender=TeamGender.Mens, index=0)
    m1_vc = CommitteePosition.objects.create(name="Men's 1st XI Vice-Captain", gender=TeamGender.Mens, index=1)
    m2_c = CommitteePosition.objects.create(name="Men's 2nd XI Captain", gender=TeamGender.Mens, index=2)
    m2_vc = CommitteePosition.objects.create(name="Men's 2nd XI Vice-Captain", gender=TeamGender.Mens, index=3)
    m3_c = CommitteePosition.objects.create(name="Men's 3rd XI Captain", gender=TeamGender.Mens, index=4)
    m3_vc = CommitteePosition.objects.create(name="Men's 3rd XI Vice-Captain", gender=TeamGender.Mens, index=5)
    m4_c = CommitteePosition.objects.create(name="Men's 4th XI Captain", gender=TeamGender.Mens, index=6)
    m4_vc = CommitteePosition.objects.create(name="Men's 4th XI Vice-Captain", gender=TeamGender.Mens, index=7)
    m5_c = CommitteePosition.objects.create(name="Men's 5th XI Captain", gender=TeamGender.Mens, index=8)
    m5_vc = CommitteePosition.objects.create(name="Men's 5th XI Vice-Captain", gender=TeamGender.Mens, index=9)
    l1_c = CommitteePosition.objects.create(name="Ladies' 1st XI Captain", gender=TeamGender.Ladies, index=0)
    l1_vc = CommitteePosition.objects.create(name="Ladies' 1st XI Vice-Captain", gender=TeamGender.Ladies, index=1)
    l2_c = CommitteePosition.objects.create(name="Ladies' 2nd XI Captain", gender=TeamGender.Ladies, index=2)
    l2_vc = CommitteePosition.objects.create(name="Ladies' 2nd XI Vice-Captain", gender=TeamGender.Ladies, index=3)
    l3_c = CommitteePosition.objects.create(name="Ladies' 3rd XI Captain", gender=TeamGender.Ladies, index=4)
    l3_vc = CommitteePosition.objects.create(name="Ladies' 3rd XI Vice-Captain", gender=TeamGender.Ladies, index=5)


if __name__ == "__main__":
    delete_old()
    add_committee_positions()