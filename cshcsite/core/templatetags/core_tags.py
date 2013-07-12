import logging
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from core.models import ClubInfo

register = template.Library()

log = logging.getLogger(__name__)


@register.filter()
def urlise_model(model, linktext=None):
    """
    Given a model object, 
    returns an <a> link to the model (using the model's get_absolute_url() method)
    
    Accepts an optional argument to use as the link text;
    otherwise uses the model's string representation
    """
    if linktext == None:
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

    email = re.sub('@','\\\\100', re.sub('\.', '\\\\056', \
        esc(email))).encode('rot13')

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
    import re
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
        for p in self.patterns:
            pValue = template.Variable(p).resolve(context)
            if path == pValue:
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