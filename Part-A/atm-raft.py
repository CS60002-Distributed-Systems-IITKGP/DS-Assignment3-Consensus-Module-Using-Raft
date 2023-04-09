# from library import MyStorage
from pysyncobj import SyncObj, SyncObjConf, replicated
import sys
sys.path.append("../")

##### -------------- KV storage -------------- #####


class MyStorage(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        cfg = SyncObjConf(dynamicMembershipChange=True)
        super(MyStorage, self).__init__(selfAddress, partnerAddrs, cfg)
        self.__data = {}

    @replicated
    def set(self, key, value):
        self.__data[key] = value

    @replicated
    def pop(self, key):
        self.__data.pop(key, None)

    def get(self, key):
        return self.__data.get(key, None)

    def ls(self):
        return list(self.__data.keys())


_global_mystorage = None


def main():
    if len(sys.argv) < 2:
        print('Usage: %s selfHost:port partner1Host:port partner2Host:port')
        sys.exit(-1)

    selfAddr = sys.argv[1]
    if selfAddr == 'readonly':
        selfAddr = None
    partners = sys.argv[2:]

    global _global_mystorage
    _global_mystorage = MyStorage(selfAddr, partners)
    user = input("login(enter username): ").strip()

    while True:
        cmd = input("> ").split()
        if not cmd:
            continue

        elif cmd[0] == "chuser":
            user = cmd[1]
            print(f"Current user: {user}")

        elif cmd[0] == "wd":
            val = _global_mystorage.get(user)
            if val is None:
                val = 0
            newval = val-float(cmd[1])
            _global_mystorage.set(user, newval)
            print(f"Rs {cmd[1]} is withdrawn from {user} account")

        elif cmd[0] == "dp":
            val = _global_mystorage.get(user)
            if val is None:
                val = 0
            newval = val+float(cmd[1])
            _global_mystorage.set(user, newval)
            print(f"Rs {cmd[1]} is deposited to {user} account")

        elif cmd[0] == "balance":
            val = _global_mystorage.get(user)
            if val is None:
                print("Account does not exist")
            else:
                print(f"{user} has account balance: {val}")

        # elif cmd[0] == "trto":
        #     val = _global_mystorage.get(user)
        #     if val is None:
        #         val = 0
        #     newval = val-float(cmd[2])
        #     _global_mystorage.set(user, newval)
        #     val = _global_mystorage.get(cmd[1])
        #     if val is None:
        #         val = 0
        #     newval = val+float(cmd[2])
        #     _global_mystorage.set(cmd[1], newval)
        #     print("Transaction successful")

        elif cmd[0] == "add":
            if user == "admin":
                _global_mystorage.set(cmd[1], float(cmd[2]))
                print("Account created")
            else:
                print("Unauthorized")

        elif cmd[0] == "rm":
            if user == "admin":
                _global_mystorage.pop(cmd[1])
                print("Account removed")
            else:
                print("Unauthorized")

        elif cmd[0] == "ls":
            if user == "admin":
                l = _global_mystorage.ls()
                print(f"Users: {l}")
            else:
                print("Unauthorized")

        elif cmd[0] == "exit":
            sys.exit(0)

        else:
            print('Wrong command')


if __name__ == '__main__':
    main()
