#!/usr/bin/env bash



# CoreAPI direct
coreapi get http://localhost:8000/api/base/equipment-data-field-types

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base equipment-data-field-types list


# HTTP
http http://localhost:8000/api/base/equipment-data-field-types/   # must have trailing slash