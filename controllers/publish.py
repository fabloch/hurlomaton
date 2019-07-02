from cups import Connection, IPPError
from datetime import datetime
from utils import CONST


class PublishController(object):
    def __init__(self):
        self.conn = Connection()
        self.printers = self.conn.getPrinters()
        self.check_printer_status()
        self.job_id = None

    def check_printer_status(self):
        is_selphy = []
        for printer in self.printers:
            is_selphy.append(printer == CONST["PRINTER_NAME"])
        if any(is_selphy):
            print("printer {} is available.".format(CONST["PRINTER_NAME"]))
            return True
        else:
            print("Printer {} is missing.".format(CONST["PRINTER_NAME"]))
            return False

    def start_print(self):
        self.conn.enablePrinter(CONST["PRINTER_NAME"])
        self.job_id = self.conn.printFile(
            CONST["PRINTER_NAME"],
            "ramdisk/polaroid.jpg",
            "{event}-{date}".format(
                event=CONST["EVENT_NAME"], date=datetime.now().strftime("%Y%m%d_%H-%M")
            ),
            {},
        )   

    def check_print_done(self):
        if self.conn.getJobs().get(self.job_id, None) is not None:
            print("Still printing...")
            return False
        return True
