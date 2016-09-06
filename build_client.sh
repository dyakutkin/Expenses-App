#!/bin/bash

cd ./client
npm run build

rm -dfr ../core/static/*
mv ./build/* ../core/static
mv ../core/static/static/* ../core/static
rm -d ../core/static/static
cd ..