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
    print(rolas)
