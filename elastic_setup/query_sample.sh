#!/bin/bash

ES_HOST="http://elasticsearch:9200"
INDEX="vince"
TERM="array"
SIZE=10


curl -u "$ELASTIC_USER:$ELASTIC_PASSWORD" -s -X POST "$ES_HOST/$INDEX/_search?filter_path=hits.hits._source,hits.total.value,aggregations,hits.hits.highlight" \
  -H 'Content-Type: application/json' \
  -d "{
    \"size\": $SIZE,
    \"from\": 0,
    \"query\": {
      \"bool\": {
        \"should\": [
          {
            \"query_string\": {
              \"query\": \"$TERM\",
              \"fields\": [\"question\", \"answer\"]
            }
          },
          {
            \"query_string\": {
              \"query\": \"\\\"$TERM\\\"^10\",
              \"fields\": [\"question\", \"answer\"],
              \"boost\": 2
            }
          }
        ]
      }
    },
    \"aggs\": {
      \"category\": {
        \"terms\": { \"field\": \"category\" },
        \"aggs\": {
          \"subCategory\": { \"terms\": { \"field\": \"subCategory\" } }
        }
      }
    },
    \"highlight\": {
      \"fields\": {
        \"question\": {},
        \"answer\": {}
      }
    }
  }" #| jq
