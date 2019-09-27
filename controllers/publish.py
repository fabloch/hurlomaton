import os
import errno
from cups import Connection
from datetime import datetime
from PIL import Image
from utils import CONST, format_time


class PublishController(object):
    def __init__(self):
        self.conn = Connection()
        self.printers = self.conn.getPrinters()
        self.check_printer_status()
        self.job_id = None

    def check_printer_status(self):
        is_selphy = []
        for printer in self.printers:
            is_selphy.append(printer == CONST["PRINTER_1"])
        if any(is_selphy):
            print("printer {} is available.".format(CONST["PRINTER_1"]))
            return True
        else:
            print("Printer {} is missing.".format(CONST["PRINTER_1"]))
            return False

    def start_print(self, print_on_1):
        if print_on_1:
            self.conn.enablePrinter(CONST["PRINTER_1"])
            self.job_id = self.conn.printFile(
                CONST["PRINTER_1"],
                "ramdisk/polaroid.jpg",
                "{event}-{date}".format(
                    event=CONST["EVENT_NAME"],
                    date=datetime.now().strftime("%Y%m%d_%H-%M"),
                ),
                {},
            )
        else:
            self.conn.enablePrinter(CONST["PRINTER_2"])
            self.job_id = self.conn.printFile(
                CONST["PRINTER_2"],
                "ramdisk/polaroid.jpg",
                "{event}-{date}".format(
                    event=CONST["EVENT_NAME"],
                    date=datetime.now().strftime("%Y%m%d_%H-%M"),
                ),
                {},
            )
        self.save_image()

    def check_print_done(self):
        if self.conn.getJobs().get(self.job_id, None) is not None:
            print("Still printing...")
            return False
        return True

    def save_image(self):
        filepath = "events/{event_name}/{date_time}.jpg".format(
            event_name=CONST["EVENT_NAME"], date_time=format_time(datetime.now(), True)
        )
        """ create folder """
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        image = Image.open("ramdisk/polaroid.jpg")
        image.save(filepath)
