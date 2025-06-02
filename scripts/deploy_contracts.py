import json
import os
from web3 import Web3
from solcx import install_solc, set_solc_version, compile_standard

from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")                  # Kairos Testnet RPC
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")    # 서버 지갑 공개주소
PRIVATE_KEY = os.getenv("PRIVATE_KEY")          # 서버 지갑 개인키

with open("../contracts/PaperChain.sol", "r", encoding="utf-8") as f :
    paper_source = f.read()

with open("../contracts/CommentChain.sol", "r", encoding="utf-8") as f :
    comment_source = f.read()

install_solc("0.8.17")
set_solc_version("0.8.17")

compile = compile_standard({
        "language": "Solidity",
        "sources": {
            "PaperChain.sol": {"content": paper_source},
            "CommentChain.sol": {"content": comment_source},
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.17",
)

paper_abi = compile["contracts"]["PaperChain.sol"]["PaperChain"]["abi"]
paper_bytecode = compile["contracts"]["PaperChain.sol"]["PaperChain"]["evm"]["bytecode"]["object"]

comment_abi = compile["contracts"]["CommentChain.sol"]["CommentChain"]["abi"]
comment_bytecode = compile["contracts"]["CommentChain.sol"]["CommentChain"]["evm"]["bytecode"]["object"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
chain_id = int(os.getenv("CHAIN_ID"))
account = PUBLIC_ADDRESS


# Paper Chain Deploy
Paper = w3.eth.contract(abi = paper_abi, bytecode = paper_bytecode)
nonce = w3.eth.get_transaction_count(account)
paper_tx = Paper.Constructor().build_transaction({
    "chainId" : chain_id,
    "from" : account,
    "nonce" : nonce,
    "gas" : 6_000_000,
    "gasPrice" : w3.to_wei("2", "gwei"),
})

signed_paper_tx = w3.eth.account.sign_transaction(paper_tx, private_key=PRIVATE_KEY)
paper_tx_hash = w3.eth.send_raw_transaction(signed_paper_tx.rawTransaction)
paper_receipt = w3.eth.wait_for_transaction_receipt(paper_tx_hash)
print(paper_receipt.contractAddress)


# Comment Chain Deploy
Comment = w3.eth.contract(abi = comment_abi, bytecode = comment_bytecode)
nonce += 1
comment_tx = Comment.constructor().build_transaction({
    "chainId" : chain_id,
    "from" : account,
    "nonce" : nonce,
    "gas" : 6_000_000,
    "gasPrice" : w3.to_wei("2", "gwei"),
})

signed_comment_tx = w3.eth.account.sign_transaction(comment_tx, private_key = PRIVATE_KEY)
comment_tx_hash = w3.eth.send_raw_transaction(signed_comment_tx.rawTransaction)
comment_receipt = w3.eth.wait_for_transaction_receipt(comment_tx_hash)
print(comment_receipt.contractAddress)


# 정보 저장
deployment_info = {
    "PaperChain": {
        "address": paper_receipt.contractAddress,
        "abi": paper_abi
    },
    "CommentChain": {
        "address": comment_receipt.contractAddress,
        "abi": comment_abi
    }
}

with open("../backend/app/deployment_info.json", "w", encoding="utf-8") as f :
    json.dump(deployment_info, f, ensure_ascii = False, indent = 2)
