#!/bin/bash

base_call='https://api.census.gov/data'
name='NAME'
pop='B01001_001E'
vars=$name","$pop
api_call=$base_call"/2021/acs/acs1?get="$vars"&for=county:*&in=state:*" 
curl -s $api_call  > data.txt