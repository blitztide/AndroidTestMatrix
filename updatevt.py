#!/usr/bin/env python3
import time
import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config
from AndroidTrustMatrix.util import CheckVT


def update_db_vt_records():
    db = AndroidTrustMatrix.db.db()
    db.Connect()
    while(True):
        unscanned = db.Get_VT_Queue()
        aged = db.Get_VT_Aged()
        applications = unscanned + aged
        if applications:
            for application in applications:
                sha256sum = application[0]
                isMalware = AndroidTrustMatrix.util.CheckVT(sha256sum)
                print(f"{sha256sum} - {isMalware}")
                if isMalware:
                    # Set db to reflect true
                    db.Update_Malware(sha256sum,isMalware)
                    db.Update_VTTime(sha256sum)
                else:
                    # No change as undetected *Try again later
                    db.Update_VTTime(sha256sum)
                    pass
                time.sleep(5)
        time.sleep(60)


if __name__ == "__main__":
    update_db_vt_records()