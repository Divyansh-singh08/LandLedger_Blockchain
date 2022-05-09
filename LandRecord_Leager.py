import datetime
import hashlib
import json
# from pickle import FALSE
from flask import Flask,jsonify,request

# Structure of the Blockchain
class Blockchain:
    #constructor
    def __init__(self):
        self.chain=[]
        #Genesis Block
        self.create_block(owner='Divyansh',Reg_no='007',proof=1,previous_hash='0') 
        #proof allways change withint the block

        #First Block made by this command 
    def create_block(self,owner,Reg_no,proof,previous_hash):
        block={'owner':owner,
               'Reg_no':Reg_no,
               'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash

        }

        # add to the chain into the block
        self.chain.append(block)
        return block

    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False

        while check_proof is False:
            hash_val=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] == '0000':
                check_proof=True
            else:
                new_proof+=1
        
        return new_proof

#Block take and give Hash
    def hash(self,block):
        encooded_block = json.dumps(block).encode()
        return hashlib.sha256(encooded_block).hexdigest()

#check weather the chain valid or not
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_idx=1

        while block_idx < len(chain):
            block=chain[block_idx]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_val=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] != '0000':
                return False
            previous_block = block
            block_idx +=1

        return True

    def get_last_block(self):
        return self.chain[-1]


#Creating the web app using Flask 
#Basic code taken from the flask docomentation 

app = Flask(__name__)

blockchain = Blockchain()

#getting full Blockchain
@app.route('/get_chain',methods=['GET'])

def get_chain():
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid',methods=['GET'])

def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {'message':'All good. The LEADGER is the valid'}
    else:
        response = {'message':'Sir we have problem to add the block ,Data is not Valid'}

    return jsonify(response), 200


@app.route('/mine_block',methods=['POST'])
def mine_block():
    values=request.get_json()

    required = ['owner','Reg_no']

    if not all(k in values for k in required):
        return 'Missing Values', 400

    owner =values['owner']
    Reg_no = values['Reg_no']
    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(owner,Reg_no,proof,previous_hash)
    
    response = {'message':'record will be added to the LEADGER soon'}
    return jsonify(response), 200


app.run(host='0.0.0.0',port=5000,debug=True)
