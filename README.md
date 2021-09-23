**Activate the vitual enviorment**

```
source blockchain-env/bin/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual enviorment

```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual enviorment 

```
python3 -m backend.app
```

**Run a peer instance**

export PEER=True && python3 -m backend.app

**Run the frontend**

In the frontend directory:

```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual enviormen t

```
export SEED_DATA=True && winpty python3.exe -m backend.app
```

Attempt to fix 