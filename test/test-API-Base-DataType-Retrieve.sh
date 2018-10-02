#!/usr/bin/env bash


# CoreAPI direct
coreapi get http://localhost:8000/api/base/data-types/cat

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base data-types read --param name=cat


# HTTP
http http://localhost:8000/api/base/data-types/cat/   # must have trailing slash
