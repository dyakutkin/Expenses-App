#!/bin/bash

cd ./client
npm run build

rm -dfr ../expenses/static/*
mv ./build/* ../expenses/static
mv ../expenses/static/static/* ../expenses/static
rm -d ../expenses/static/static
cd ..