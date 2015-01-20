""" URL redirection rules for legacy URLs from the old website.
"""

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',

    # All old pages are, conveniently, prefixed with '/pages/'
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r'^join-us.php$', RedirectView.as_view(url=reverse_lazy('contact_us'))),
    url(r'^training.php$', RedirectView.as_view(url=reverse_lazy('upcoming_trainingsession_list'))),
    url(r'^fees.php$', RedirectView.as_view(url=reverse_lazy('about_fees'))),
    url(r'^about.php$', RedirectView.as_view(url=reverse_lazy('about_us'))),
    url(r'^about/pitch-directions.php$', RedirectView.as_view(url=reverse_lazy('directions'))),
    url(r'^about/pitch-directions/the-leys-school-astro.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['leys']))),
    url(r'^about/pitch-directions/coldham-s-common-aka-abbey.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['abbey']))),
    url(r'^about/pitch-directions/the-perse-school.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['perse-boys-school']))),
    url(r'^about/pitch-directions/st-catharine-s-college.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['catz']))),
    url(r'^about/pitch-directions/the-perse-girls-school.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['perse-girls']))),
    url(r'^about/pitch-directions/cambridge-university-astro.php$', RedirectView.as_view(url=reverse_lazy('venue_detail', args=['univ']))),
    url(r'^about/committee-meetings.php$', RedirectView.as_view(url=reverse_lazy('about_committee'))),
    url(r'^about/chairmans-notes.php$', RedirectView.as_view(url='/blog/categories/chairman/')),
    url(r'^about/members-offers.php$', RedirectView.as_view(url=reverse_lazy('members_offers'))),
    url(r'^kit.php$', RedirectView.as_view(url=reverse_lazy('about_kit'))),
    url(r'^social.php$', RedirectView.as_view(url=reverse_lazy('about_social'))),
    url(r'^social/2012-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2012'))),
    url(r'^social/2011-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2011'))),
    url(r'^social/2010-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2010'))),
    url(r'^social/2009-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2009'))),
    url(r'^social/2008-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2008'))),
    url(r'^social/2007-club-dinner.php$', RedirectView.as_view(url=reverse_lazy('dinner2007'))),
    url(r'^social/2008-tour.php$', RedirectView.as_view(url=reverse_lazy('tour2008'))),
    url(r'^commission.php$', RedirectView.as_view(url=reverse_lazy('commission'))),
    url(r'^calendar.php$', RedirectView.as_view(url=reverse_lazy('calendar'))),
    url(r'^teams.php$', RedirectView.as_view(url=reverse_lazy('clubteam_list'))),
    url(r'^reports.php$', RedirectView.as_view(url=reverse_lazy('match_list'))),
    url(r'^reports/(.*).php$', RedirectView.as_view(url=reverse_lazy('match_list'))),
    url(r'^stats/(.*).php$', RedirectView.as_view(url=reverse_lazy('stats'))),

    url(r'^(.*)ladies-1st-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['l1']))),
    url(r'^(.*)ladies-2nd-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['l2']))),
    url(r'^(.*)mens-1st-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['m1']))),
    url(r'^(.*)mens-2nd-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['m2']))),
    url(r'^(.*)mens-3rd-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['m3']))),
    url(r'^(.*)mens-4th-xi(.*)$', RedirectView.as_view(url=reverse_lazy('clubteam_detail', args=['m4']))),
)