# NineQuantumsMorris

### Set up dev environment

Clone the repo
```
git clone https://github.com/Scemic/9MANMORRIS
```

Activate python3 virtual environment
```
virtualenv --python=python3 env
source env/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

### Get acces to D-Wave Quantum Computers:
Create an account at D-Wave and get you API token from
[the dashboard](https://cloud.dwavesys.com/leap/).
Work on you VirtualEnv, if you have one set up, and run
(D-Wave should be installed when installing the requirements):
```
dwave config create
```
Enter your API token here, which can be found on the D-Wave dashbaord.
The output shown below includes the interactive prompts and placeholder replies.
```
$ dwave config create
Configuration file not found; the default location is: /home/jane/.config/dwave/dwave.conf
Confirm configuration file path [/home/jane/.config/dwave/dwave.conf]:
Profile (create new) [prod]:
API endpoint URL [skip]:
Authentication token [skip]: ABC-1234567890abcdef1234567890abcdef
Default client class (qpu or sw) [qpu]:
Default solver [skip]:
Configuration saved.
```
