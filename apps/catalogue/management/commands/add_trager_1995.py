#-*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from catalogue.models import (
    Reference,
    Parameter,
    Observation,
    AstroObject,
    AstroObjectClassification,
)
from catalogue.utils import PrepareSupaHarrisDatabaseMixin
from data.parse_trager_1995 import parse_trager_1995_gc
from data.parse_trager_1995 import parse_trager_1995_tables


class Command(PrepareSupaHarrisDatabaseMixin, BaseCommand):
    help = "Add ReplaceMe data to the database"

    def handle(self, *args, **options):
        logger = logging.getLogger("console")
        super().handle(*args, **options)  # to run our Mixin modifications

        cmd = __file__.split("/")[-1].replace(".py", "")
        logger.info("\n\nRunning the management command '{0}'\n".format(cmd))

        ads_url = "https://ui.adsabs.harvard.edu/abs/1995AJ....109..218T"
        reference, created = Reference.objects.get_or_create(ads_url=ads_url)
        if not created:
            logger.info("Found the Reference: {0}\n".format(reference))
        else:
            logger.info("Created the Reference: {0}\n".format(reference))

        t95_gc = parse_trager_1995_gc()
        logger.debug("\ngc has {0} entries".format(len(gc)))
        logger.debug("keys: {0}".format(gc.keys()))
        t95_tables = parse_trager_1995_tables()
        logger.debug("\ntables has {0} entries".format(len(tables)))
        logger.debug("keys: {0}".format(tables.keys()))

        for gc_name in t95_gc["Name"]:
            logger.info("{0}".format(gc_name))
            gc = AstroObject.objects.filter(name=gc_name).first()
            if gc:
                logger.info("Found the AstroObject: {0}".format(gc))
            else:
                logger.info("Did not find AstroObject")
            continue

            # observation = Observation.objects.create(
            #     reference=reference,
            #     astro_object=gc,
            #     parameter=R_Sun,
            #     value=gc_R_Sun,
            # )
            # print("Created the Observation: {0}".format(observation))

        return
        for gc_name in clusters:
            igc, = numpy.where(t95_tables["Name"] == gc_name)