
import time
import os
import pickle
import hashlib
from flask import Flask, request
import requests
import json
import zkp_org as zkp

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)  

zkp_para = zkp.ZKP_Para()
# userList = []

class User:
    """User class to store user details
    """
    def __str__(self): return json.dumps(self.__dict__, cls = SimpleObject, indent=4)

    def __init__(self, username, password) -> None:
        """Initializes the user with given username and password
        Also generates a ZKP signature for the password which will be used for verification

        Args:
            username (str): username of the user
            password (str): password of the user
        """
        self.username = username
        self.password = password
        self.zkp_signature = zkp.ZKP_Signature(zkp_para, self.password)
        self.reportList = []
        
    @classmethod
    def takeInput(cls):
        return cls(input("Enter username: "), input("Enter password: "))
        
    def addReport(self, report):
        """Adds a report to the user's report list

        Args:
            report (str): description of the report
        """
        self.reportList.append(report)
        
class Transaction:
    """Transaction class to store blockchain transaction
    """
    def __str__(self): return json.dumps(self.__dict__, cls = SimpleObject, indent=4)

    def __init__(self, sender, recipient, report):
        """Intializes the transaction with sender, recipient and report

        Args:
            sender (User): Sender of the transaction
            recipient (User): Recipient of the transaction
            report (str): Sender's report that will be added to recipient's report list
        """
        self.sender = sender
        self.recipient = recipient
        self.report = report

    @classmethod
    def takeInput(cls):
        sender = input("Enter sender:")
        if(sender not in userList):
            print("Sender not found. Register First")
            return None
        recipient = input("Enter recipient:")
        if(recipient not in userList):
            print("Recipient not found. Invalid username")
            return None
        report = input("Enter report: ")
        return cls(sender, recipient, report)
    
    def verifyTransaction(self):
        """Transaction is verifeid by verifying the ZKP signature of sender and recipient

        Returns:
            bool: Retuen True if transaction is verified else False
        """
        if self.report not in self.sender.reportList:
            print("Report not found in sender's report list")
            return False
        ver1 = zkp.ZKP_Verifier(zkp_para, self.sender.zkp_signature)
        ver2 = zkp.ZKP_Verifier(zkp_para, self.recipient.zkp_signature)
        
        return ver1.verify() and ver2.verify()


class Block:
    def __str__(self): return json.dumps(self.__dict__)

    def __init__(self, index, timestamp, transactions, previousHash, nonce = 0):
        """Intialiszes the block with index, timestamp, transactions, previousHash and nonce

        Args:
            index (int): Index of the block in the blockchain
            timestamp (time): timestamp of the block creation
            transactions ([Transaction]): list of transactions in the block
            previousHash (hex): hexvalue of the previous block's hash
            nonce (int, optional): nonce or proof. Defaults to 0.
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.previousHash = previousHash

    @property
    def Hash(self):
        """Generates the hash of the block

        Returns:
            hex: Returns the hex value of the hash of the block
        """
        hashData = '{}{}{}{}'.format(
            self.previousHash, self.index, self.nonce, self.timestamp
        )
        return hashlib.sha256(hashData.encode()).hexdigest()


class Blockchain:
    """Blockchain class to store the blockchain
    """
    def __init__(self):
        """_Initializes the blockchain with creation of genesis block
        
        Difficulty for PoW is set to 4. It can be changed as per the requirement
        """
        self.difficulty = 4
        self.current_Transactions = []
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        """Creates genesis block with index 0 and hash of 100

        Returns:
            Block: Return the first or genesis block
        """
        return Block(0, time.time(), [], 100)

    @property
    def getLastBlock(self):
        """Returns the last block in the blockchain"""
        return self.chain[-1]
    
    def addTransaction(self, transaction=None):
        """Adds a transaction to the current or pending transaction list of the blockchain  

        Args:
            transaction (Transaction, optional): This transaction is added to the list. Defaults to None.

        Returns:
            int: number of pebding transactions in the blockchain if transaction is verifed else -1
        """
        print("Adding this transaction" , transaction)
        if not transaction:
            transaction = Transaction.takeInput()
        if(transaction.verifyTransaction()):
            if transaction.report not in transaction.recipient.reportList:
                transaction.recipient.reportList.append(transaction.report)
            else:
                print("Report already present in recipient's report list")
            self.current_Transactions.append(transaction)
            if(len(self.current_Transactions) > 0):
                self.mineBlock()
            return len(self.current_Transactions)
        else:
            print("Transaction not verified")
            return -1

    def viewTransactions(self):
        index = self.getLastBlock.index
        for i in range(0, index):
            print(self.current_Transactions[i])

    def newBlock(self, block, proof):
        """Adds new block to the blockchain

        Args:
            block (Block): This block is added to the blockchain
            proof (int): proof or nonce of the block

        Returns:
            bool: Returns True if proof or nonce is valid else False
        """
        previous_hash = self.getLastBlock.Hash
        if previous_hash != block.previousHash:
            return False
        if not self.isValidProof(block, proof):
            return False
        # block.Hash = proof
        self.chain.append(block)
        return True

    def mineBlock(self):
        """Mines a new block and adds it to the blockchain

        Returns:
            int: index of newy mined block if block is mined else False
        """
        if not self.current_Transactions:
            return False

        lastBlock = self.getLastBlock

        newBlock = Block(index=lastBlock.index + 1,
                          timestamp=time.time(),
                          transactions=self.current_Transactions,
                          previousHash=lastBlock.Hash)

        proof = self.proofOfWork(newBlock)
        self.newBlock(newBlock, proof)
        self.current_Transactions = []
        return newBlock.index

    def proofOfWork(self, block):
        """Implements proof of work (PoW) algorithm for the blockchain

        Args:
            block (Block): BLock for which proof is to be found

        Returns:
            hex: Returns the hex value of the hash of the block computed using proof of work (PoW) algorithm
        """
        block.nonce = 0
        computed_hash = block.Hash
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.Hash
        return computed_hash

    def isValidProof(self, block, block_hash):
        """Checks if the block hash is valid or not
        
        Checks if the block hash starts with 0's equal to the difficulty of the blockchain
        """
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.Hash)
    
    
    def isValidChain(self):
        """Checks validity of the blockchain by comparing the hash of the previous block with the previousHash of the current block

        Returns:
            bool: Returns True if blockchain is valid else False
        """
        for i in range(1, len(self.chain)):
            print(self.chain[i].previousHash, self.chain[i-1].Hash)
            if self.chain[i].previousHash != self.chain[i-1].Hash:
                return False
        return True
    
    def viewUser(self, username):
        """Returns the list of all the transaction of the given user stored in the blockchain

        Args:
            username (str): username of the user

        Returns:
            [str]: List of transactions of the user in the blockchain
        """
        print(userList)
        unl = [i.username for i in userList]
        if(username not in unl):
            print("Blockchain: User not found")
            return None
        tr_list = []
        for i in range(len(self.chain)):
            for j in range(0, len(self.chain[i].transactions)):
                if self.chain[i].transactions[j].sender.username == username or self.chain[i].transactions[j].recipient.username == username:
                    tr_list.append(self.chain[i].transactions[j])
        return tr_list



u1 = User("P00san", "1234")
u2 = User("P00Chetan", "1234")
u3 = User("D00Rathi", "0000")
u4 = User("D00Amogh", "0000")
u1.addReport("I am not feeling well")
u2.addReport("I have high blood pressure")
userList = [u1,u2,u3,u4]
b = Blockchain()
b.addTransaction(Transaction(u1, u3, "I am not feeling well"))
b.mineBlock()
b.addTransaction(Transaction(u2, u4, "I have high blood pressure"))
b.mineBlock()