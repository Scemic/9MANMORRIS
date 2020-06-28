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
Just press enter at every stage except for `Authentication token`.
Enter your API token here, which can be found on the D-Wave dashbaord.
