# Waage-Backend
Flask (Python) Backend of the Solawi-Waage.


# Prerequirements:

- python3
- pipenv
- flask
- sqlite

```
sudo apt-get install pipenv python3-flask
```

# Running



```
./bootstrap.sh
```

## Test it

```
# get current weight of the Scale
curl 0.0.0.0:5000/scale

# tare Scale
curl -X POST 0.0.0.0:5000/scale/tare

# get configuration (for debug purpose)
curl 0.0.0.0:5000/scale/config
```

## Other Things that did only make sense while development
```
# create a new product
curl -X POST -H 'Content-Type: application/json' -d '{
  "name": "Kartoffel",
  "description": "auch bekannt als Erdaepfel"
}' http://0.0.0.0:5000/products

# retrieve exams
curl http://0.0.0.0:5000/products
```







## Credits
this app is based on: https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-apps-part-1
