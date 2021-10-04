import hashlib
import time
import random

# ----------------------------------------------Patient Monitoring System------------------------------------------------
# ---------------------------------------------------------By-----------------------------------------------------------
# -------------------------------------------------------18i-0500--------------------------------------------------------
# -------------------------------------------------------18i-0698--------------------------------------------------------
# -------------------------------------------------------18i-1567--------------------------------------------------------

Stake_holders=list=list()                                              # All Nodes lie here

class Node:
    def __init__(self,id,coins,no_of_blocks_inserted):
        self.id=id
        self.coins=coins
        self.no_of_blocks_inserted=no_of_blocks_inserted
    def print_data(self):
        print("ID : ",self.id, " Number of Blocks inserted : ",self.no_of_blocks_inserted, " Coins : ",self.coins)
    def block_inserted(self):
        self.no_of_blocks_inserted+=1
        self.coins+=10

# Calculates hash
def calculate_hash(block):
    block_of_string = "{}{}{}{}{}".format(str(block.index), str(block.proof_no),
                                          str(block.prev_hash), str(block.data),
                                          str(block.timestamp))
    return hashlib.sha256(block_of_string.encode()).hexdigest()

# This class represents the data in a particular Block of the Blockchain

# For Patient Monitoring System :
# A block should have the following data:
# Patient ID
# Patient Name
# Patient DOB
# Patient Registration Nubmer

class BlockData:
    def __init__(self):
      self.data = []

    # Used to insert more data to the data section of a particular Block of a Blockchain
    def insert_data(self,data):
        self.data.append(data)
    #def __repr__(self):
    #    return self.data

    # Used to print the data present
    def print_data(self):
        for i in self.data:
            print(i,end=' ')
        print()

# This class represents the Block of a Blockchain
class Block:
    def __init__(self, index, proof_no, prev_hash, data,inserted_by, timestamp=None):
        self.index = index                           # Unique identifier for a Block
        self.proof_no = proof_no                     # Proof number
        self.prev_hash = prev_hash                   # Hash of the previous block
        self.data = data                             # Data section of a Block
        self.timestamp = timestamp or time.time()    # Timestamp
        self.prev_block = None                       # Link to the previous Block
        self.current_hash=calculate_hash(self)       # Hash of the Block
        self.inserted_by=inserted_by                 # Node, that inserted the Block

    # Prints the Current Block and all previous Blocks of this particular Block
    def ListBlocks(self):
        cur_block=self
        while cur_block is not None:
            print("Patient Number: ",cur_block.index," : ",end='  ')
            cur_block.data.print_data()
            cur_block=cur_block.prev_block

    # Inserts a new Block, such that the current block becomes the previous Block of the newly inserted Block and then returns that newly inserted Block
    def InsertBlock(self,dataToInsert,inserted_by,proof_no=0):
        # Adjusting the Proof number
        if (proof_no == 0):
            proof_no = self.proof_no + 1

        # Creating the Data section for the new Block and then inserting data into it
        new_block_data=BlockData()
        new_block_data.insert_data(dataToInsert)
        # Creating a new Block and also inserting the above data section to it
        new_block=Block(self.index+1,proof_no,self.current_hash,new_block_data,inserted_by)

        # Making the current Block, the previous Block of the newly created Block
        new_block.prev_block=self
        inserted_by.block_inserted()
        self = new_block
        return self

    # Verifies Block chain by comparing Hashes and Timestamps
    def VerifyChain(self):
        ver=True
        iterator=self
        while iterator.prev_block is not None:
            if (iterator.prev_hash!= iterator.prev_block.current_hash):
                #print("prev hash = "+str(iterator.prev_hash)+ "   prev.current_hash= " + str(iterator.prev_block.current_hash))
                ver=False
                break
            if(iterator.timestamp < iterator.prev_block.timestamp):
                ver=False
                print("Time changes !!!!!!!!")
                break
            iterator=iterator.prev_block
        if ver == True:

            print("The Block Chain is Verifed")
        else:
            print("The Block Chain is Not Verifed")
        return ver

    # Used to change the data present in a particular Block (For testing purpose only)
    def ChangeBlock(self,oldTrans,newTrans):
        print("A Change in the BlockChain is Happening")
        stop=False
        cur_block=self
        while cur_block is not None:
            for i in range(len(cur_block.data.data)):
                if cur_block.data.data[i]==oldTrans:
                    cur_block.data.data[i]=newTrans
                    cur_block.timestamp=time.time()
                    cur_block.current_hash=calculate_hash(cur_block)
                    stop=True
                    break
                cur_block=cur_block.prev_block
            if(stop):
                break
        return ()

if __name__ == '__main__':


    print("-------------------------------------------------\n")
    print("           Patient Monitoring System             \n")
    print("-------------------------------------------------\n")

    # Creating Nodes
    s1 = Node('000001',100,0)
    s2 = Node('000002', 70, 0)
    s3 = Node('000003', 50, 0)
    Stake_holders.append(s1)
    Stake_holders.append(s2)
    Stake_holders.append(s3)

    # Creation of Genesis block for Patient Monitoring System

    # Creation of the Data section of a Block
    b1 = BlockData()
    b1.insert_data("P1, Sadia Saad, 12th March,2000, 1st January,2021")

    # Creating a Block by the name genesis
    genesis=Block(0, 0, " ", b1,Stake_holders[0])

    # Appending new Blocks to genesis, but every time, we insert a new block, the 'current block' will become the
    # 'previous block' of the 'newly inserted Block' and the 'newly inserted Block' will be returned such that
    # the 'new block' will become 'current block'. So every time, genesis will point to the newly inserted block.

    miner = random.randint(0, 2)
    genesis = genesis.InsertBlock("P2, Sara Saad, 15th July,2010, 7th Februray,2019", Stake_holders[miner])
    miner = random.randint(0, 2)
    genesis = genesis.InsertBlock("P3, Wasif Ali,1st January,2000, 1st March,2021", Stake_holders[miner])
    miner = random.randint(0, 2)
    genesis = genesis.InsertBlock("P4, Umair Anwar,10th May,2000, 25th April,2021", Stake_holders[miner])
    miner = random.randint(0, 2)
    genesis = genesis.InsertBlock("P5, Laiba Imran,20th December, 2000, 13th June,2021", Stake_holders[miner])

    genesis.ListBlocks()
    genesis.VerifyChain()

    genesis.ChangeBlock("P1, Sadia Saad, 12th March,2000, 1st January,2021","P10, Aimen Zara, 15th March,2000, 1st July,2021")
    print("A block has been changed.")
    genesis.VerifyChain()

    genesis.ListBlocks()

    # Allowing Nodes to add additional records of patients after verification from all Nodes
    opt=1
    while opt==1:
        print("\n!!!!!!!    If you want to add more records, please press 1, else press 0    !!!!!!!")
        opt=int(input())
        # If a Node wants to Add a new record
        if(opt==1):
            data=input("PLease enter the record in the following format : 'id', 'name', 'DOB', 'Admitted on'")
            # Miner is selected Randomly
            miner = random.randint(0, 2)
            ver = 1
            # Now the new Block is verified by each Node
            print("######################################################## Validating ########################################################")
            for i in range(len(Stake_holders)):
                if (i != miner):
                    print("Node ", Stake_holders[i].id, ", Please Validate !!!!")
                    print("Miner ", Stake_holders[miner].id,
                          " want to insert a Block, press 1, if you validate else any other number : ")
                    val = input()
                    if val == "1":
                        ver += 1

            # If 51% Nodes agree, the new Block is inserted, else not
            if (ver > len(Stake_holders) / 2):
                genesis = genesis.InsertBlock(data,Stake_holders[miner])
                print("Block inserted by ", Stake_holders[miner].id)
            else:
                print("Unfortunately, the block isnt validated by At least 51% Nodes, therefore it cannot be added and hence it is an Orphan Block")

            print("\n<------------------------------------------------------------------------------------------------------------------------->\n")


    print("--------------------          Final data in the Blockchain          --------------------\n")
    genesis.ListBlocks()

    print("\n<<<<<<<<<<--------------------          Application is Closing          -------------------->>>>>>>>>>")