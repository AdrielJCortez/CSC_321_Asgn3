import bcrypt
from nltk.corpus import words
# import nltk
# nltk.download('words')
import time

def generate_word_list():
    # generate a random word list
    word_list = words.words()

    # filter the words to be 6 <= len <= 10 and make sure there is no duplicates
    
    # now a set (to prevent duplicates)
    updated_word_list = {
        w for w in word_list
        if 6 <= len(w) <= 10
    }

    # # check the len of how many words
    # print(len(updated_word_list))

    return list(updated_word_list)

def crack_passwords(w_list, h):
    # # logic i need to loop
    # h = b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq"
    # first_check = w_list[0]

    # b = first_check.encode("utf-8")

    # if bcrypt.checkpw(b, h):
    #     print("match!")
    # else:
    #     print("no match")

    start = time.time() 
    for w in w_list:
        b = w.encode("utf-8")
        if bcrypt.checkpw(b, h):
            end = time.time()
            return w, (end - start)
    
def main():
    filtered_word_list = generate_word_list()

    hashes = [b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq",
         b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC",
         b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.6B7jUcPdnqJz4tIUwKBu8lNMs5NdT9q",
         b"$2b$09$M9xNRFBDn0pUkPKIVCSBzuwNDDNTMWlvn7lezPr8IwVUsJbys3YZm",
         b"$2b$09$M9xNRFBDn0pUkPKIVCSBzuPD2bsU1q8yZPlgSdQXIBILSMCbdE4Im",
         b"$2b$10$xGKjb94iwmlth954hEaw3O3YmtDO/mEFLIO0a0xLK1vL79LA73Gom",
         b"$2b$10$xGKjb94iwmlth954hEaw3OFxNMF64erUqDNj6TMMKVDcsETsKK5be",
         b"$2b$10$xGKjb94iwmlth954hEaw3OcXR2H2PRHCgo98mjS11UIrVZLKxyABK",
         b"$2b$11$/8UByex2ktrWATZOBLZ0DuAXTQl4mWX1hfSjliCvFfGH7w1tX5/3q",
         b"$2b$11$/8UByex2ktrWATZOBLZ0Dub5AmZeqtn7kv/3NCWBrDaRCFahGYyiq",
         b"$2b$11$/8UByex2ktrWATZOBLZ0DuER3Ee1GdP6f30TVIXoEhvhQDwghaU12",
         b"$2b$12$rMeWZtAVcGHLEiDNeKCz8OiERmh0dh8AiNcf7ON3O3P0GWTABKh0O",
         b"$2b$12$rMeWZtAVcGHLEiDNeKCz8OMoFL0k33O8Lcq33f6AznAZ/cL1LAOyK",
         b"$2b$12$rMeWZtAVcGHLEiDNeKCz8Ose2KNe821.l2h5eLffzWoP01DlQb72O",
         b"$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay"]
    
    for h in hashes:
        password, time_elapsed = crack_passwords(filtered_word_list, h)
        print(h, password, time_elapsed)

if __name__ == "__main__":
    print(main())