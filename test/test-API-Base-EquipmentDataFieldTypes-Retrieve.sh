#!/usr/bin/env bash


# CoreAPI direct
coreapi get http://localhost:8000/api/base/equipment-data-field-types/1

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base equipment-data-field-types read --param id=1


# HTTP
http http://localhost:8000/api/base/equipment-data-field-types/1/   # must have trailing slash
