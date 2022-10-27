#!/usr/bin/env python3
#%%
import requests
import json
import pandoc

#%%
from_date = '2022-10-15'
to_date = '2022-10-23'
base_url = "https://content.guardianapis.com/search"
# base_url = "https://content.guardianapis.com/international"
headers = {
    "api-key": "bb42fde3-79eb-43fa-b969-d2c95a2b68d7",
    "format": "json",
    "from-date": from_date,
    "to-date": to_date,
    "show-most-viewed": 'True',
    "order-by": "oldest",
    "page-size": "10",
    "show-fields": "headline,body"
}

req = requests.get(base_url, headers)
req_dict = req.json() # This holds all the info


#%% Print request to  file
fn_response = 'response.json'


# %% convert to epub with pandoc

# TODO the pandoc python library is not working!
# This would be the easiest choice, also for the potential user that wants this installed
# doc = pandoc.read(source=first_text, format='html')
# pandoc.write(doc, file='output.epub')
#
# Instead, use the command-line pandoc
# First, write an .html file
FN_OUTPUT = 'output'
N_ARTICLES = 10
with open(FN_OUTPUT+'.html', 'w') as f:
    for i in range(N_ARTICLES):
        headline = req_dict['response']['results'][i]['fields']['headline']
        text = req_dict['response']['results'][i]['fields']['body']
        publication_date = req_dict['response']['results'][i]['webPublicationDate'][:10]
        f.write("<h1>" + headline + "</h1>")
        f.write("<h3> Publication date: " + publication_date + "</h3>")
        f.write("<br>")
        f.write(text)

# Run a command line pandoc prompt
pandoc_command = ['pandoc', f'{FN_OUTPUT}.html', '-f', 'html', '-t', 'epub', '-s', '-o', f'{FN_OUTPUT}.epub']
document_title = 'oldspaper_from_' + from_date
pandoc_command = pandoc_command + ['--metadata', f'title={document_title}']
import subprocess
from pathlib import Path
root_folder = Path('/home/txart/Programming/github/oldspaper')
subprocess.run(pandoc_command, check=True, cwd=root_folder)


with open(fn_response, 'w') as f:
    json.dump(req.json(), f, indent=1)
