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

## two methods to use:
### call get_ready_to_generate_different_spelling
`differnet_english_spells = get_ready_to_generate_different_spelling(firstname_in_persian, 'First_name')` 

`differnet_english_spells = get_ready_to_generate_different_spelling(lastname_in_persian, 'Last_name')`

1. you must give above function persian firstname or lastname in first argument
2. in second argument you must specify what type of name you want to generate different spells ('First_name' or 'Last_name')
3. the output is a dictionary of different spells with their probilities
4. the output is just for firstname or lastname, so this func can't generate different spells of fullname



### call get_name
`first_tname, last_name, diff_spells = get_name(firstname, lastname)`

1. you must give above function persian firstname and persian lastname 
2. the output is dictionary of different spells of firstname, lastname and fullname in english language

### sample code 

`first_tname, last_name, diff_spells = get_name('علیرضا', 'رضایی')` 
