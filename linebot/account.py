import random
import string

account_list = {
    "Cf7bb5c05288433dae62584999121acd0": {
        "parentId": "NULL",
        "country" : "TW",
        "username": "kjchen",
        "usrId": "00000000"
    }
}

def accountRegis(usr, pwd, parentId, country):
    usrId = "".join(random.sample(string.ascii_uppercase + string.digits, 8))
    global account_list; tmp = {
        pwd: {
            "parentId": parentId,
            "country" : country,
            "username": usr,
            "usrId": usrId
        }
    }; account_list.update(tmp)

def getAccountList():
    return account_list


def main():
    accountRegis (
        "darren",
        "Cf7bb5c05288433dae62584999121acd0",
        "00000000",
        "TW"
    ); print(account_list)

if __name__ == '__main__':
    main()
