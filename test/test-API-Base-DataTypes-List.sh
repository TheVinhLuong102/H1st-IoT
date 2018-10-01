#!/usr/bin/env bash


# CoreAPI direct
coreapi get http://localhost:8000/api/base/data-types

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base data-types list


# HTTP
http http://localhost:8000/api/base/data-types/   # must have trailing slash
