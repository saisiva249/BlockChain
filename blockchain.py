#imports
import datetime
import hashlib
import json
from flask import Flask, jsonify
#part 1 Building a blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1,previous_hash='0')
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash
                }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof= False
        while check_proof is False:
            #problem to solve by miners
            #1. it should be more complex and not so linear new+previous=previous+new, so looking for nonlinear relation ship, to make it more hard
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    
    # we will take the block as it contains the json data it will be converted to string using json dumps
    # then we use the string converted to the hash using haslib 256sha
    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    #verifies the proof of the current block is as per the target
    #verify the previous hash and hash of the previous block are same or not
    def is_chain_Valid(self, chain):
        previous_block = chain[0]
        block_index= 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            preious_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2-preious_proof**2).encode()).hexdigest()
            if(hash_operation[:4])!="0000":
                return False
            previous_block = block
            block_index+=1
        return True
# Part2 mining our blockchain
#create a Flask Webapp
app = Flask(__name__)
#creating instance of blockchain
blockchain = Blockchain()
@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message':'Congrats you have added a block to block chain',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response), 200
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response ={"chain":blockchain.chain,
               "length":len(blockchain.chain)}
    return jsonify(response), 200
@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_Valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
app.run(host="0.0.0.0",port=5000)
