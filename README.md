# robo-advisor project README

## Setup

## Installation

Fork this remote repository, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

After cloning the repo, navigate there from the command-line:

```sh
cd ~/Desktop/robo-advisor
```




### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```
### Security Requirements
From your current position in the command line. Create a .env file by calling "code .env" if you use the VSCode Text Editor or create the file in your own personal way inside of this directory:
```sh
code .env
```
The .env file will contain 3 variables named SENDGRID_API_KEY, MY_EMAIL_ADDRESS, and ALPHAVANTAGE_API_KEY

### Sendgrid API Installation
First, sign up for a free account here (https://signup.sendgrid.com/), then click the link in a confirmation email to verify your account. Then create an API Key here (https://app.sendgrid.com/settings/api_keys) with "full access" permissions.

To setup the usage examples below, store the API Key value in an environment variable called SENDGRID_API_KEY. Also set an environment variable called MY_EMAIL_ADDRESS to be the email address you just associated with your SendGrid account (e.g. "abc123@gmail.com"). You will send emails from this account


### Alpha Vantage API Installation
Claim your Alpha Vantage API Key by entering your email address on this website (https://www.alphavantage.co/support/#api-key). After receiving your API key place it into a environment variable in your .env file called ALPHAVANTAGE_API_KEY

## Usage



Run the program by calling
```sh
python robo-advisor/app/robo_advisor.py
```
and following the on screen instructions

If done correctly, any stock that you analyzed will have its information output into a csv file inside of the /data directory.

```sh
 ~/Desktop/robo-advisor/data
 ```

Also warning, the program automatically creates a line chart and opens the chart in your web browser. You have to return to the terminal or command line that you ran the program from to see the recommendations.

