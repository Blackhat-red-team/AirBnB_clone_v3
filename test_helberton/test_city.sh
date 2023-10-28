#!/usr/bin/env bash

# invalid state id
echo "***************************"
echo "Testing invalid state id"
curl -X GET http://0.0.0.0:5000/api/v1/states/not_an_id/cities/

echo "***************************"
echo "Testing valid state id to get cities"
# valid state id
curl -X GET http://0.0.0.0:5000/api/v1/states/0e391e25-dd3a-45f4-bce3-4d1dea83f3c7/cities/

# valid state id with no cities

echo "***************************"
echo "Testing valid state id with no cities"
curl -X GET http://0.0.0.0:5000/api/v1/states/387da8e2-b4f2-4879-abf5-c55af03288bb/cities/


echo "***************************"
echo "Testing invalid city id"
# invalid city id
curl -X GET http://0.0.0.0:5000/api/v1/cities/not_an_id

echo "***************************"
echo "Testing valid city id"
# valid city id
curl -X GET http://0.0.0.0:5000/api/v1/cities/1da255c0-f023-4779-8134-2b1b40f87683


# # POST 
curl -X POST http://0.0.0.0:5000/api/v1/states/387da8e2-b4f2-4879-abf5-c55af03288bb/cities -H "Content-Type: application/json" -d '{"name": "Alexandria"}' -vvv

# # PUT
curl -X PUT http://0.0.0.0:5000/api/v1/cities/521b47cf-4223-4425-87a0-9b95eec19149 -H "Content-Type: application/json" -d '{"name": "OooooOOOOMGGGGGGGGGGGGG"}'
