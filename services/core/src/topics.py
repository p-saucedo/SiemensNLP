from tokenizers import Tokenizer
from transformers import BertTokenizer

def run2():
    tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
    text = "Replace me by any text you'd like."
    inputs = tokenizer.encode(text)
    print(inputs.ids)
    print(inputs.tokens)
    print(inputs.attention_mask)
if __name__ == '__main__':
    run2()
