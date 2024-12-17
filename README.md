# Social Media Scraping
The purpose of the repository is an experimental approach to scraping various social media accounts for information, and creating an image representation of the scraped person(s). 
For now the scraping possibilities are limited to LinkedIn profiles.

The scraped information is then intended to be summarized using a using a GPT model from OpenAI, and then finally this output can be put into an image generator model, e.g. DALL-E 3, from OpenAI.

To utilize the elements in this project requires an active LinkedIn account to use for scraping and an available OpenAI resource with deployed models.

# Packages
The used packages for this project are introduced below.

## LinkedIn Scraper
I will utilize the following publically available library to scrape LinkedIn profiles:
https://github.com/tomquirk/linkedin-api

**UPDATE DECEMBER 2024:** The Library seems to have encountered some errors, leaving it unable to connect to LinkedIn. There are multiple open tickets reporting the same issue that I am seeing.
```
linkedin_api.cookie_repository.LinkedinSessionExpired
```
I suspect it is due to some updates from LinkedIn that is blocking the access.

NB! LinkedIn has some fairly aggressive policies towards api scraping, and will potentially ban accounts. Open source tools therefore always highlight that any consequences are the user's own responsibility. Scraping should therefore be done carefully by minimising API calls. For this reason the implemented script in this repo can only scrape a single person per run.

## OpenAI
The project utilize Microsoft's OpenAI service. An available resource is thus a requirement to run this project.
https://learn.microsoft.com/en-us/azure/ai-services/openai/

To use requires and available endpoint (URL) to the resource, specified in the corresponding .toml files. Additionally, an available API key is a requirement. Since this should be kept secret it will not be 
put into the code, but in stead specified as an environment variable set manually.

# Process Description
This section will explain in detail how to run each job in project separately.

## extract_profile_info.py
This job will scrape individual profiles for the information. To minimize API calls this only a single person is allowed to be scraped per run. 

The scraped information is returned as dictionary with each element from LinkedIn being stored within a separate key. There is a lot of information here,
much of which is deemed irrelevant. Therefore, only a subset of the keys are retained for the out of this job.

The output is then stored as pickle files (dictionaries) for use later.

The job expects a dictionary *'LINKEDIN_ACCOUNTS'* defined in /modules/config.py. This dictionary contains key & value pairs tieing the entire procject together.

The key can in theory be any string, thought be aware that outputs are saved with naming on the key string, and subsequent jobs will refer to this key when loading information.
I therefore recommended using a key string that makes it easy to recognize which person is the information refers to.

The value in the dictionary refers to the personal LinkedIn URL, which is used to prompt the API call and return information. This can be found on each profile by viewing the *contact info*
in the top of a profile. It will look something like this.  
![image](https://github.com/user-attachments/assets/7c38e3db-055b-42ec-a552-9a738c94ee9c)


In summary the dictionary in the config.py should have a structure similar to this.
```python
LINKEDIN_ACCCOUNTS = {
    "Christian Heiden": "christianheiden",
}
```

The job is then run from the command line interface. It requires two inputs to be specified.
1. --person_name: The key value from the dictionary
2. --user_email: User email for LinkedIn

It can this be run like this.  

`python -m extract_profile_info --person_name "Christian Heiden" --user_email chr_heiden@hotmail.com`

The CLI will then prompt you for a password for the given LinkedIn account.  

NB: Obviously you should always use your own account! Don't get someone else banned from LinkedIn.

## process_profile_info.py
This job will take a dictionary of information from the previous step and run it through a GPT model from OpenAI. The job has a set of standard instructions, defined in
*/modules/instructions/default_openai_settings.toml*

The default instructions are set up to summarize the information from the person's linkedIn profile and make some assumptions about the person based on available information. If different
outputs are desired a custom set of instructions can be added.

Any custom instructions file should contain the same 3 'keys' from the default .toml files as they control inputs in respective code elements.

NB: The default instructions contain a placeholder endpoint which should be replaced by your resource.

The job is run from the command line interface and has one required input, and one optional
1. --person_name: reflects the file name of the pickle file to load.
2. --instruction_path (optional): local path to instructions. If left out it defaults to standard instructions. 

Before running the job the API key must be set as an environment variable.  
`export OPEN_AI_KEY="insert_your_api_key_here"`

See e.g. https://medium.com/@ofirziv/how-to-start-using-openai-api-step-by-step-38ff1ee4b15b

The job is then run via the CLI as:  
`python -m process_profile_info --person_name "Christian Heiden"`

or  

`python -m process_profile_info --person_name "ALL"`

or 

`python -m process_profile_info --person_name "Christian Heiden" --instruction_path my/custom/path.toml`

## generate_images.py
This job will generate an image based on instructions and input content using an image generation model from OpenAI. The job has a set of standard instructions, defined in
*/modules/instructions/default_img_gen_settings.toml*

The default instructions are set up to create an image based on a summarized linkedIn profile and create a realistic looking image. If different
outputs are desired a custom set of instructions can be added. As of now the code is set to return only a single image output. It is technically possible to return
more than 1 image from the OpenAI, the code could be changed to accomodate this.

Any custom instructions file should contain the same 3 'keys' from the default .toml files as they control inputs in respective code elements.

NB: The default instructions contain a placeholder endpoint which should be replaced by your resource.

The job is run from the command line interface and has one required input, and one optional
1. --person_name: reflects the file name of the pickle file to load.
2. --instruction_path (optional): local path to instructions. If left out it defaults to standard instructions. 

Before running the job the API key must be set as an environment variable.  
`export OPEN_AI_KEY="insert_your_api_key_here"`

The job is then run via the CLI as:  
`python -m generate_images --person_name "Christian Heiden"`

or 

`python -m generate_images --person_name "Christian Heiden" --instruction_path my/custom/path.toml`
