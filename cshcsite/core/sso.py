import base64
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


def get_disqus_sso(user):
    # create a JSON packet of our data attributes
    output = ["""<script type="text/javascript">
        var disqus_config = function() {"""]
    if user.is_authenticated():

        data = json.dumps({
            'id': user.pk,
            'username': user.get_full_name(),   # TODO: Are spaces ok here?
            'email': user.email,
            # TODO: link comments to members where possible
            #'url': user.get_absolute_url(),
        })
        # encode the data to base64
        message = base64.b64encode(data)
        # generate a timestamp for signing the message
        timestamp = int(time.time())
        # generate our hmac signature
        sig = hmac.HMAC(settings.DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

        output.append("""
                this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        """ % dict(
            message=message,
            timestamp=timestamp,
            sig=sig,
            pub_key=settings.DISQUS_PUBLIC_KEY
        ))

    output.append("""
        this.page.api_key = "%(pub_key)s";

        // This adds the custom login/logout functionality
        this.sso = {
              name:   "CSHC",
              button:  "%(static_url)smedia/disqus-sso-login-button.gif",
              //icon:     "http://%(domain)s/favicon.png",
              url:        "http://%(domain)s%(login_url)s",
              logout:  "http://%(domain)s/members/logout/",
              width:   "360",
              height:  "480"
        };
    };
    </script>""" % dict(
        pub_key=settings.DISQUS_PUBLIC_KEY,
        static_url=settings.STATIC_URL,
        domain=Site.objects.get_current().domain,
        login_url=reverse('auth_login')))

    print "".join(output)
    return "".join(output)

