#!/usr/bin/env python
# -*-encoding: utf-8-*-
import traceback
from django.core.management.base import BaseCommand
from optparse import make_option
from core.models import CshcUser
from _command_utils import email_user, create_password

class Command(BaseCommand):
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
            # Email the user with their new password
            email_user(user, password, sim)



