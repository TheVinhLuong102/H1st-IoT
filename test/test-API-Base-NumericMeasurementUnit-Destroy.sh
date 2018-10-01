#!/usr/bin/env bash


# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base numeric-measurement-units delete --param id=10


# HTTP
http --auth app:apppw123 DELETE http://localhost:8000/api/base/numeric-measurement-units/ name=kmh