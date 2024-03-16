from transformers import AutoTokenizer

# Specify the model identifier (e.g., BERT base uncased)
model_identifier = "bert-base-uncased"

# Load the pre-trained tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_identifier)

# Tokenize a sentence
tokens = tokenizer("I love transformers")
# Tokenization is the process of breaking down text into smaller units called tokens.
# Each token typically corresponds to a word or subword (an integer)
# Attention ! After breaking down the text, start token [CLS] and end token [SEP] will be added
# for the example above, we will get 5 tokens