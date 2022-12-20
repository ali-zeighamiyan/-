# use probility files to generate english differnet spells of persian names
  
## prepare
write these in command prompt to install require packages  
`pip install nltk`  
`pip install deep_translator` 

## package function
### ngrams
	extract continuous sequences of words or symbols or tokens in a document
### GoogleTranslator
    get source and target language and the text, then request to google translator and give us translated text

## start code
### import packages to script
`from nltk import ngrams`
`import tqdm`
`import json`
`from deep_translator import GoogleTranslator`

## method to use:

### call get_name
`first_tname, last_name, diff_spells = get_name(firstname, lastname)`

1. you must give above function persian firstname and persian lastname 
2. the output is dictionary of different spells of firstname, lastname and fullname in english language

### sample code 

`first_tname, last_name, diff_spells = get_name('علیرضا', 'رضایی')` 
