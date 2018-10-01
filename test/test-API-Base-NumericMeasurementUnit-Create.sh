#!/usr/bin/env bash


# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base numeric-measurement-units create --param name=test


# HTTP
http --auth app:apppw123 POST http://localhost:8000/api/base/numeric-measurement-units/ name=test
