#!/usr/bin/env bash



# CoreAPI direct
coreapi get http://localhost:8000/api/base/numeric-measurement-units

# CoreAPI via schema
coreapi get http://localhost:8000/api/schema
coreapi action base numeric-measurement-units list


# HTTP
http http://localhost:8000/api/base/numeric-measurement-units/
