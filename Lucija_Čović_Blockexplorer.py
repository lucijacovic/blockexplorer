# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 13:10:13 2021

@author: lucijacovic
"""

"""
Blockexplorer
￭ API upiti: getblock, getblockstats, listtransactions, getrawtransaction…
￭ pretraga po bloku ili transakciji
￭ prikaz najvažnijih informacija
    ￮ blok
    ￮ transakcija
    ￮ adresa
"""

#Note to self: terribly written code, next time use different GUI

from bitcoinrpc.authproxy import AuthServiceProxy
import pprint
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as st
from datetime import datetime
import requests

#Server access data (no data - security reasons)
rpc_user=""
rpc_password=""
host=""
port=""

rpc_client=AuthServiceProxy("http://"+rpc_user+":"+rpc_password+"@"+host+":"+port+"/")


#TxId: cc21e5e71a7d7db81010586c249b40ff431a5c5c621b6ef992cb526660b4bca8


def input_type():
    search = user_entry.get() #uzmi upisanu vrijednost search polja
    if len(search)!=64 and search!=int: #nevazeci unos
        text_box.delete(1.0, "end-1c")
        text_box.insert(tk.END, "Oops! We couldn’t find what you are looking for.\nPlease enter transaction id, block height or hash.\n")
        text_box2.delete(1.0, "end-1c")
    
    try: #ako je input visina bloka
        blockhash = rpc_client.getblockhash(int(search))
        block=rpc_client.getblock(blockhash) #Block info
        #pprint.pprint(block)
        block2 = rpc_client.getblockstats(blockhash)
        text_box.delete(1.0, "end-1c")
        text_box.insert(tk.END, "Blockhash: " + str(block['hash']) + "\n" + 
                                "Confirmations: " + str(block['confirmations']) + "\n" +
                                "Time: " + str(datetime.fromtimestamp(block['time'])) + "\n" +
                                "Height: " + str(block['height']) + "\n" +
                                "Number of Transactions: " + str(block['nTx']) + "\n" +
                                "Difficulty: " + str(block['difficulty']) + "\n" +
                                "Merkle root: " + str(block['merkleroot']) + "\n" +
                                "Version: " + str(block['version']) + "\n" +
                                "Bits: " + str(block['bits']) + "\n" +
                                "Weight: " + str(block['weight']) + "\n" +
                                "Size: " + str(block['size']) + "\n" +
                                "Nonce: " + str(block['nonce']) + "\n" +
                                "Transaction Volume: " + str(float(block2['total_out'])/100000000) + " BTC\n" +
                                "Block Reward: " + str(float(block2['subsidy'])/100000000) + " BTC\n" +
                                "Fee Reward: " + str(float(block2['totalfee'])/100000000) + " BTC")
        text_box2.delete(1.0, "end-1c")
        text_box2.insert(tk.END, "Transactions: " + str(block['tx']))
        #text_box.configure(state='disabled')
    except:
        pass
    
    try: #ako je input hash bloka
        block=rpc_client.getblock(str(search))
        block2 = rpc_client.getblockstats(search)
        text_box.delete(1.0, "end-1c")
        text_box.insert(tk.END, "Blockhash: " + str(block['hash']) + "\n" + 
                                "Confirmations: " + str(block['confirmations']) + "\n" +
                                "Time: " + str(datetime.fromtimestamp(block['time'])) + "\n" +
                                "Height: " + str(block['height']) + "\n" +
                                "Number of Transactions: " + str(block['nTx']) + "\n" +
                                "Difficulty: " + str(block['difficulty']) + "\n" +
                                "Merkle root: " + str(block['merkleroot']) + "\n" +
                                "Version: " + str(block['version']) + "\n" +
                                "Bits: " + str(block['bits']) + "\n" +
                                "Weight: " + str(block['weight']) + "\n" +
                                "Size: " + str(block['size']) + "\n" +
                                "Nonce: " + str(block['nonce']) + "\n" +
                                "Transaction Volume: " + str(float(block2['total_out'])/100000000) + " BTC\n" +
                                "Block Reward: " + str(float(block2['subsidy'])/100000000) + " BTC\n" +
                                "Fee Reward: " + str(float(block2['totalfee'])/100000000) + " BTC")
        text_box2.delete(1.0, "end-1c")
        text_box2.insert(tk.END, "Transactions: " + str(block['tx']))
        #text_box.configure(state='disabled')
    except:
        pass
    
    try: #ako je input txid
        tx_hex=rpc_client.getrawtransaction(str(search))
        tx_details = rpc_client.decoderawtransaction(tx_hex) #Tx info
        
        #Total Output
        t_outs=0
        for i in tx_details["vout"]: #IZLAZI
            t_outs=t_outs+i["value"]        
        
        text_box.delete(1.0, "end-1c")
        text_box.insert(tk.END, "TxId: " + str(tx_details['txid']) + "\n" +
                        "Hash: " + str(tx_details['hash']) + "\n" +
                         "Size: " + str(tx_details['size']) + "\n" +
                         "Weight: " + str(tx_details['weight']) + "\n" +
                         "Number of Inputs: " + str(len(tx_details["vin"])) + "\n" +
                         "Number of Outputs: " + str(len(tx_details["vout"])) + "\n")
        text_box2.delete(1.0, "end-1c")

        num_of_inputs=0
        t_ins=0
        text_box2.insert(tk.END, "Inputs\n")
        for i in (tx_details["vin"]):
            text_box2.insert(tk.END, "Index: " + str(num_of_inputs) + "\nSigscript: " + str(tx_details["vin"][num_of_inputs]["scriptSig"]["asm"]) + "\nWitness: " + str(tx_details["vin"][num_of_inputs]["txinwitness"]) + "\n")
            txid=(tx_details["vin"][num_of_inputs]["txid"])
            vout=(tx_details["vin"][num_of_inputs]["vout"])
            tx_hex1=rpc_client.getrawtransaction(txid)
            #ulaz f14fd51b0050e7845f071577a0ecd195091aa325392c8babec6b0b01889d0982, output 1 'vout': 1
            tx_details1 = rpc_client.decoderawtransaction(tx_hex1)
            num_of_inputs=num_of_inputs+1
            num_of_outputs=0
            
            for i in tx_details1["vout"]: #IZLAZI
                if tx_details1["vout"][num_of_outputs]["n"]==vout:
                    text_box2.insert(tk.END, "Value: " + str(tx_details1["vout"][num_of_outputs]["value"]) + " BTC" + "\n")
                    t_ins = t_ins + float(tx_details1["vout"][num_of_outputs]["value"]) #Total Output
                num_of_outputs=num_of_outputs+1
       
        #Fees
        fees=float(t_ins)-float(t_outs)
        
        text_box.insert(tk.END, "Total Input: " + str(t_ins) + " BTC\n"
                         + "Total Output: " + str(t_outs) + " BTC\n"
                         + "Fees: " + str(fees) + " BTC")
        
        num_of_outputs=0
        text_box2.insert(tk.END, "\nOutputs")
        # PROBLEM za 46873c3aa3bb6fb82e0ecd7799146c068f1c8a416ebd2e15174b4448c1f9f045
        # prvi output nema adresu pa ne ispisuje                   
        for i in (tx_details["vout"]): #IZLAZI treba mi i["n"], i["value"], i["scriptPubKey"]["addresses"]
            text_box2.insert(tk.END, "\nIndex: " + str(tx_details["vout"][num_of_outputs]["n"]) + "\nValue: " + str(tx_details["vout"][num_of_outputs]["value"]) + " BTC" + "\nAddress: " + str(tx_details["vout"][num_of_outputs]["scriptPubKey"]["addresses"]))
            num_of_outputs=num_of_outputs+1
    except:
        pass

#API request for current Bitcoin price
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()


#GUI using Tkinter

#window
root = tk.Tk()
root.configure(background='white')
root.rowconfigure(0, minsize=50, weight=1)
root.columnconfigure([0, 1, 2], minsize=50, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

#header
photo1 = PhotoImage(file = "b2.png")
welcome_label = tk.Label(root, image=photo1, border="0")
welcome_label.grid(row = 0, column = 0, columnspan=3, sticky='ew')
welcome_label.grid_rowconfigure(0, weight=1)
welcome_label.grid_columnconfigure(0, weight=1)

#Bitcoin price
photo2 = PhotoImage(file = "btc.png") #Bitcoin subheading
btc_label = tk.Label(root, image=photo2, compound = LEFT, text = " " + data["bpi"]["EUR"]["rate"] + "€    " + data["bpi"]["USD"]["rate"] + "$", font=("Arial", 12, 'bold'), bg="white", fg="#282321")
btc_label.grid(row = 2, column = 0, columnspan=3, padx=20, pady=10, sticky = 'w')

#row color
titleframe = tk.Frame(root, bg ="#121d33", height=60)
titleframe.grid(row=1, column=0, columnspan=3, sticky='ew')

#clear user_entry function
def clear_entry(event, user_entry):
    user_entry.delete(0, END)
    user_entry.unbind('<Button-1>', click_event)

placeholder_text = 'Search Tx or Block'

#user entry
user_entry = ttk.Entry(root,width = 65, font=("Arial", 11))
user_entry.insert(0, placeholder_text)
user_entry.bind("<Button-1>", lambda event: clear_entry(event, user_entry))
user_entry.grid(row = 1, column = 0, sticky='e', padx=50)
user_entry.grid_rowconfigure(2, weight=1)
user_entry.grid_columnconfigure(1, weight=1)

#search button
photo = PhotoImage(file = "sss.png")
btn_search = tk.Button(master=root, text="Search", image=photo, command=input_type, font=("Arabic Transparent", 10),height=35, width=35, bg ="#121d33",border="0") #kako povezat entry i botun
btn_search.grid(row=1, column=1, sticky = 'w')
btn_search.grid_rowconfigure(2, weight=1)
btn_search.grid_columnconfigure(2, weight=1)

#textbox1
text_box = st.ScrolledText(root, width = 100, height = 15, font=("Arial", 10))
text_box.grid(row = 3, column = 0, columnspan = 3,padx=10)

#details subheading
photo3 = PhotoImage(file = "d.png")
tr_label = tk.Label(root, text = "Transaction Info:", image=photo3, font=("Arabic Transparent", 11), bg="white")
tr_label.grid(row = 4, column = 0, padx=20, pady=5, sticky = 'w')

#textbox2
text_box2 = st.ScrolledText(root, width = 100, height = 20, font=("Arial", 10))
text_box2.grid(row = 5, column = 0, columnspan = 3, padx=10)

root.mainloop()
