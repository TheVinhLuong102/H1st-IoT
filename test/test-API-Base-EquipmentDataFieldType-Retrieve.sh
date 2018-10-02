#!/usr/bin/env bash


# CoreAPI direct
coreapi get http://localhost:8000/api/base/equipment-data-field-types/control

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base equipment-data-field-types read --param name=control


# HTTP
http http://localhost:8000/api/base/equipment-data-field-types/control/   # must have trailing slash
