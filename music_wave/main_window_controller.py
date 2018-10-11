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

    data_access_object = data_manager.Data_manager("", "rolas.db")

    if os.path.isfile("rolas.db"):
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
    else :
        data_access_object.create_database()
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
