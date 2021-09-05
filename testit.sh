# Default test with results to the terminal.
pytest \
    --durations=0 \
    --cov-report term-missing \
    --cov=census_cb .

# Generate HTML Reports of coverage with pytest
# pytest\
#     --durations=0 \
#     --cov-report html:cov_html \
#     --cov=census_cb .
