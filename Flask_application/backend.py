import time
import base64
import hmac
import hashlib
import struct
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import secrets
import pyotp
import torch


class LM_TOTP:
    def __init__(self, secret , time_step = 120):
        model_name = 'gpt2'
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()

        self.secret = secret
        self.time_step = time_step

    def gpt2_(self , prompt):
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')

        attention_mask = torch.ones(input_ids.shape, device=input_ids.device)

        output = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=100,
            num_return_sequences=1,
            temperature=1,           # Controls randomness:  more makes the generated text more random
            top_k=50,
            top_p=0.95,
            no_repeat_ngram_size=2,
            early_stopping=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)




    def last_160_bits(self , input_string):
        byte_data = input_string.encode('utf-8')
        last_256_bits = byte_data[-20:]
        base32_encoded = base64.b32encode(last_256_bits).decode('utf-8')
        return base32_encoded


    def generate_key(self , secret_key  , given_timestamp):

        if given_timestamp == None:
            TimeStamp = int(time.time())  // self.time_step
        else:
            TimeStamp = given_timestamp // self.time_step

        prompt = secret_key + str(TimeStamp)
        response = self.gpt2_(prompt)
        new_key = self.last_160_bits(response)
        

        return TimeStamp , new_key


    def generate_totp(self , timestamp = None):
        response = self.generate_key(self.secret  , timestamp)

        time_stamp = response[0]
        new_secret = response[1]

        totp = pyotp.TOTP(new_secret)
        otp = totp.at(time_stamp)

        return otp


    def validate(self , given_totp ):
        totp = self.now()
        if given_totp == totp:
            return True
        else:
            return False
        
    def now(self):
        return self.generate_totp()


    def at(self , timestamp):
        return  self.generate_totp(timestamp)