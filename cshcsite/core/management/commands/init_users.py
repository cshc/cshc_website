#!/usr/bin/env python
# -*-encoding: utf-8-*-
import traceback
from django.core.management.base import BaseCommand
from optparse import make_option
from core.models import CshcUser
from _command_utils import send_welcome_email_to_user, create_password
from core.reg_utils import create_profile

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save the password and email the users)'),
    )
    help = 'Initializes each user that doesn\'t have a password set. A random password is ' + \
           'generated and an email is sent to the user with their password.'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        sim = options['simulate']
        if sim:
            print "#### SIMULATION ONLY ####"

        # Get all users that don't have a password set.
        users = filter(lambda u: not u.has_usable_password(), CshcUser.objects.all())

        # For each user
        for u in users:
            u.is_active = False
            if not sim:
                u.save()
            password = create_password(u, sim)
            reg_profile = create_profile(u, sim)
            # Email the user with their new password
            send_welcome_email_to_user(reg_profile, password, sim)



