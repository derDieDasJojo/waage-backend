# Waage-Backend
Flask (Python) Backend of the Solawi-Waage.

# Running



```
docker run --name online-exam-db     -p 5432:5432     -e POSTGRES_DB=online-exam     -e POSTGRES_PASSWORD=0NLIN3-ex4m     -d postgres

./bootstrap.sh
```

## Test it

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