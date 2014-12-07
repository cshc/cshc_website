#!/usr/bin/env python
# -*-encoding: utf-8-*-

""" Various utility management commands for emailing users.

    Usage:
    - Send a welcome email to a user:
        python manage.py email_user -w <email>
"""

import traceback
from optparse import make_option
from django.core.management.base import BaseCommand
from core.models import CshcUser
from core.management.commands.command_utils import send_welcome_email_to_user, create_password
from core.reg_utils import create_profile


class Command(BaseCommand):
    """ Management command for emailing users. """

    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually email the user)'),
        make_option('-w', '--welcome',
                    action='store',
                    type="string",
                    dest='welcome_email',
                    metavar='EMAIL',
                    help='Send a welcome email to EMAIL'),
    )
    help = 'Various email tasks relating to users'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        sim = options['simulate']
        if sim:
            print "#### SIMULATION ONLY ####"

        if options['welcome_email']:
            print "Sending welcome email to '{}'".format(options['welcome_email'])
            email = options['welcome_email']
            user = CshcUser.objects.get(email=email)
            password = create_password(user, sim)
            user.is_active = False
            if not sim:
                user.save()
            reg_profile = create_profile(user, sim)
            # Email the user with their new password
            send_welcome_email_to_user(reg_profile, password, sim)
