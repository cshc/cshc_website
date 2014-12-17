""" Common template tags.
"""

import logging
from datetime import date
from itertools import groupby
from calendar import HTMLCalendar
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from zinnia.models.entry import Entry
from core.models import ClubInfo

register = template.Library()

LOG = logging.getLogger(__name__)


def get_absolute_static_url(request):
    """ Returns the absolute URL for settings.STATIC_URL.

        This is useful because the thumbnail template tag doesn't
        support relative urls. In our case we know if we're not in
        DEBUG mode STATIC_URL is absolute anyway (Amazon S3). If we
        are in DEBUG mode we need to convert the relative static url
        to an absolute url using the request.build_absolute_uri()
        utility method.
    """
    static_url = settings.STATIC_URL
    if settings.DEBUG:
        static_url = request.build_absolute_uri(static_url)
    return static_url

# Override of Zinnia's get_recent_entries tag.
# Here we include the context as we need to pass the request object
# to the template so we can make use of the base url etc.
@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def cshc_get_recent_entries(context, number=5, template='zinnia/tags/entries_recent.html'):
    """ Return the most recent blog entries. """
    return {'request': context['request'],
            'template': template,
            'absolute_static_url': get_absolute_static_url(context['request']),
            'entries': Entry.published.all()[:number]}


@register.filter()
def urlise_model(model, linktext=None):
    """
    Given a model object,
    returns an <a> link to the model (using the model's get_absolute_url() method)

    Accepts an optional argument to use as the link text;
    otherwise uses the model's string representation
    """
    if linktext is None:
        linktext = "%s" % model

    return mark_safe("<a href='{}' title='{}'>{}</a>".format(model.get_absolute_url(), model, linktext))


@register.filter()
def obfuscate(email, linktext=None, autoescape=None):
    """
    Given a string representing an email address,
	returns a mailto link with rot13 JavaScript obfuscation.

    Accepts an optional argument to use as the link text;
	otherwise uses the email address itself.
    Ref: http://djangosnippets.org/snippets/1475/

    An email address obfuscation template filter based on the ROT13 Encryption function
    in Textmate's HTML bundle.
    The filter should be applied to a string representing an email address. You can optionally
    pass the filter an argument that will be used as the email link text (otherwise it will
    simply use the email address itself).
    Example usage:
    {{ email_address|obfuscate:"Contact me!" }}
    or
    {{ email_address|obfuscate }}
    Of course, you can also use this on hardcoded email addresses, like this:
    {{ "worksology@example.com"|obfuscate }}
    """
    import re
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    try:
        email = re.sub('@', '\\\\100', re.sub('\.', '\\\\056',
                       esc(email))).encode('rot13')
    except TypeError:
        LOG.warn("Failed to obfuscate email address")
        email = ''

    if linktext:
        linktext = esc(linktext).encode('rot13')
    else:
        linktext = email

    rotten_link = """<script type="text/javascript">document.write \
        ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (email, linktext)
    return mark_safe(rotten_link)
obfuscate.needs_autoescape = True


@register.tag
def active(parser, token):
    """
    Used to apply the 'active' class based on the current URL.
    Ref: http://stackoverflow.com/questions/340888/navigation-in-django
    """
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])


class NavSelectedNode(template.Node):
    def __init__(self, patterns):
        self.patterns = patterns

    def render(self, context):
        path = context['request'].path
        for pattern in self.patterns:
            p_value = template.Variable(pattern).resolve(context)
            if path == p_value:
                return "active"
        return ""

############################################################################################
# CLUB INFO


@register.filter()
def lookup_value(queryset, key):
    """
    Used to lookup a value from the ClubInfo table, based on the provided key.

    queryset = a QuerySet of the ClubInfo table
    key = the value of the key field of the item for which the value field is required.
    """
    try:
        return queryset.get(key=key).value
    except ClubInfo.DoesNotExist:
        return None


@register.simple_tag
def clubinfo(key):
    """A simple tag that returns the value of the given key from the ClubInfo table."""
    try:
        return ClubInfo.objects.get(key=key).value
    except ClubInfo.DoesNotExist:
        return None


@register.assignment_tag
def get_clubinfo(key):
    """An assignment version of the clubinfo tag"""
    return clubinfo(key)


@register.simple_tag
def clubinfo_email(key, linktext=None):
    """A simple tag that returns an obfuscated mailto: link to the email address matching
    the given key from the ClubInfo table."""
    return obfuscate(clubinfo(key), linktext)
clubinfo_email.needs_autoescape = True


############################################################################################
# CALENDAR SUPPORT


@register.tag
def event_calendar(parser, token):
    """
    The template tag's syntax is {% event_calendar year month event_list %}
    """
    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        LOG.error("Failed to parse token")
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return EventCalendarNode(year, month, event_list)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        # Get the variables from the context so the method is thread-safe.
        try:
            try:
                my_event_list = self.event_list.resolve(context)
            except template.VariableDoesNotExist:
                LOG.error("event_list does not exist")
                return
            try:
                my_year = self.year.resolve(context)
            except template.VariableDoesNotExist:
                LOG.error("year does not exist")
                return
            try:
                my_month = self.month.resolve(context)
            except template.VariableDoesNotExist:
                LOG.error("month does not exist")
                return
        except ValueError:
            LOG.error("ValueError", exc_info=True)
            return
        try:
            #LOG.debug("Creating EventCalendar. year = {}, month = {}, event_list = {}".format(my_year, my_month, my_event_list))
            cal = EventCalendar(my_event_list)
            return mark_safe(cal.formatmonth(int(my_year), int(my_month)))
        except:
            LOG.error("Unexpected exception", exc_info=True)
            return


class EventCalendar(HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatweekday(self, weekday):
        try:
            if weekday == 0:
                return "<th class='mon'>M</th>"
            elif weekday == 1:
                return "<th class='tue'>T</th>"
            elif weekday == 2:
                return "<th class='wed'>W</th>"
            elif weekday == 3:
                return "<th class='thu'>T</th>"
            elif weekday == 4:
                return "<th class='fri'>F</th>"
            elif weekday == 5:
                return "<th class='sat'>S</th>"
            elif weekday == 6:
                return "<th class='sun'>S</th>"
        except:
            LOG.error("Failed to formatweekday {}".format(weekday))

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                dt = self.events[day][0].date
                matches_by_date_link = urlresolvers.reverse('matches_by_date', args=[dt.strftime("%d-%b-%y")])
                popover_title = '<a href=\'{}\'>Matches on {}</a>'.format(matches_by_date_link, dt.strftime("%d-%b"))
                popover_content = ['<ul>']
                for event in self.events[day]:
                    popover_content.append('<li>')
                    if event.is_home:
                        popover_content.append('<span class=\'label label-success\'>H</span>')
                    else:
                        popover_content.append('<span class=\'label\'>A</span>')
                    popover_content.append('<span class=\'time\'>{}</span>'.format(event.time_display()))
                    popover_content.append(conditional_escape("<a href=\'{}\' title=\'Match details...\'>{} vs {}, <span class=\'text-success\'>{}</span></a>".format(event.get_absolute_url(), event.our_team, event.opp_team.genderless_name(), event.simple_venue_name())))
                    popover_content.append('</li>')
                popover_content.append('</ul>')
                link_id = dt.strftime("%d-%b-%y")
                link_open = '<a id="{}" href="#" class="pop", data-toggle="popover" data-placement="bottom" data-html="true" data-original-title="{}" title data-content="{}">'.format(link_id, popover_title, ''.join(popover_content))
                return self.day_cell(cssclass, '<span class="dayNumber label label-success">{}{}</a></span>'.format(link_open, day))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">{}</span>'.format(day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date.day
        return dict(
            [(day, sorted(items, key=lambda i: i.time if i.time else i.datetime().time())) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


############################################################################################
# DISQUS SUPPORT

from core.sso import get_disqus_sso


@register.simple_tag(takes_context=True)
def disqus_config(context, user):
    try:
        return get_disqus_sso(context.request, user)
    except:
        LOG.error("Unable to get disqus sso info for user.", exc_info=True)
        return

# TEMP - until this is provided by the django-disqus app

def get_config(context):
    """
    return the formatted javascript for any disqus config variables
    """
    conf_vars = ['disqus_developer', 'disqus_identifier', 'disqus_url', 'disqus_title']

    output = []
    for item in conf_vars:
        if item in context:
            output.append('\tvar %s = "%s";' % (item, context[item]))
    return '\n'.join(output)

@register.inclusion_tag('disqus/recent_comments.html', takes_context=True)
def cshc_disqus_recent_comments(context, shortname='', num_items=5, excerpt_length=200, hide_avatars=0, avatar_size=32):
    """
    Return the HTML/js code which shows recent comments.

    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)

    return {
        'shortname': shortname,
        'num_items': num_items,
        'hide_avatars': hide_avatars,
        'avatar_size': avatar_size,
        'excerpt_length': excerpt_length,
        'config': get_config(context),
    }


############################################################################################
# ADMIN INTERACE SUPPORT

@register.inclusion_tag('core/_admin_link.html', takes_context=True)
def instance_admin_links(context, model, change=True, add=False, changelist=False):
    """
    """
    try:
        content_type = ContentType.objects.get_for_model(model)
        return AdminLinksCreator(content_type.app_label, content_type.name, content_type.model, model.pk, change, add, changelist).render(context)
    except:
        LOG.error("Failed to render instance_admin_links", exc_info=True)


@register.inclusion_tag('core/_admin_link.html', takes_context=True)
def model_admin_links(context, app_label, model_name, add=True, changelist=True):
    """
    """
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        return AdminLinksCreator(content_type.app_label, content_type.name, content_type.model, None, False, add, changelist).render(context)
    except:
        LOG.error("Failed to render model_admin_links", exc_info=True)


class AdminLinksCreator(object):

    def __init__(self, app_label, friendly_name, model_name, instance_id=None, change=False, add=False, changelist=False):
        self.app_label = app_label
        self.friendly_name = friendly_name
        self.model_name = model_name
        self.instance_id = instance_id
        self.change = change
        self.add = add
        self.changelist = changelist

    def render(self, context):
        ctx = {}
        user = context['user']
        ctx['user'] = user
        should_display = False

        if self.change and self.has_perm(user, 'change_'):
            ctx['change_url'] = self.get_admin_change_url()
            ctx['change_label'] = "Edit " + self.friendly_name
            should_display = True
        else:
            ctx['change_url'] = None
            ctx['change_label'] = None

        if self.add and self.has_perm(user, 'add_'):
            ctx['add_url'] = self.get_admin_add_url()
            ctx['add_label'] = "Add " + self.friendly_name
            should_display = True
        else:
            ctx['add_url'] = None
            ctx['add_label'] = None

        if self.changelist and self.has_perm(user):
            ctx['list_url'] = self.get_admin_list_url()
            ctx['list_label'] = self.friendly_name.capitalize() + " list"
            should_display = True
        else:
            ctx['list_url'] = None
            ctx['list_label'] = None

        ctx['display_admin_links'] = should_display
        return ctx

    def get_admin_change_url(self):
        return urlresolvers.reverse("admin:%s_%s_change" % (self.app_label, self.model_name), args=(self.instance_id,))

    def get_admin_add_url(self):
        return urlresolvers.reverse("admin:%s_%s_add" % (self.app_label, self.model_name))

    def get_admin_list_url(self):
        return urlresolvers.reverse("admin:%s_%s_changelist" % (self.app_label, self.model_name))

    def has_perm(self, user, prefix=''):
        return user.has_perm('{}.{}{}'.format(self.app_label, prefix, self.model_name))
