import rola
import miner
import data_manager
import os
import os.path

if __name__ == "__main__" :
    home = os.getenv("HOME")
    path = str(home + "/Music")

    miner_object = miner.Miner(path)
    miner_object.mine()
    rolas = miner_object.get_rolas()
    albums = miner_object.get_albums()
    performers = miner_object.get_performers()

    for rola in rolas.values() :
        print("================================")
        print(rola.get_title())
        print("================================")

    for performer in performers.values():
        print("///////////////////")
        print(performer)

    for album in albums.values():
        print("@@@@@@@@@@@@@@@@@@")
        print(album)
