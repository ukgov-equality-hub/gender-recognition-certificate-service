from datetime import datetime
from typing import List
from flask import session
from grc.models import db, Application, ListStatus, ApplicationStatus

from math import exp
import time
import requests
import threading

class Threading():
    """ Exponentially make the app sleep to prevent attacks
    """
    thread_local = threading.local()

    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()

    def __init__(self, number):
        self.number = number

    def throttle(self):
        if not self.number:
            self.number = 0

        # set upper limit to prevent aws timeout
        if self.number < 4:
            self.number = self.number + 1

        t1 = threading.Thread(target=self.sleep(self.number))
        t1.start()

        return self.number

    @staticmethod
    def sleep(number):
        time.sleep(exp(number))