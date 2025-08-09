import argparse
from ..control import set_paused, is_paused
from ..config import KILL_SWITCH_PATH
import os, sys, json

def main():
    p = argparse.ArgumentParser("ttbctl")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("status")
    sub.add_parser("pause")
    sub.add_parser("resume")

    k = sub.add_parser("killswitch")
    k.add_argument("--on", action="store_true")
    k.add_argument("--off", action="store_true")

    args = p.parse_args()

    if args.cmd == "status":
        print(json.dumps({"paused": is_paused(), "kill_file_exists": os.path.exists(KILL_SWITCH_PATH)}))
    elif args.cmd == "pause":
        set_paused(True, "manual")
        print("paused")
    elif args.cmd == "resume":
        set_paused(False)
        print("resumed")
    elif args.cmd == "killswitch":
        if args.on:
            open(KILL_SWITCH_PATH, "w").close()
            print("kill switch ON (file created)")
        elif args.off:
            if os.path.exists(KILL_SWITCH_PATH):
                os.remove(KILL_SWITCH_PATH)
            print("kill switch OFF (file removed)")
    else:
        p.print_help(); sys.exit(1)

if __name__ == "__main__":
    main()