# repo-monitor
Datamole test assignment implementation of an API that monitors GitHub repositories

## Endpoints

1. http://127.0.0.1:8000/docs - Swagger documentation
2. http://127.0.0.1:8000/health - Use this endpoint to check the health of the application
3. http://127.0.0.1:8000/events - List of all events for the particular repositories (cached)
4. http://127.0.0.1:8000/statistics - Provide basic statistics for the repositories passed in the
JSON body with `repositories` key as a list of strings.

Have a look in the Swagger documentation for more details on the endpoints.

## How to use

### Statistics

To report statistics one can set up which repositories and if to filter by a specific event.

To get a notion what it is like, you can run this in the terminal:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/statistics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "repositories": [
    "https://github.com/michtesar/repo-monitor"
  ]
}'
```

This is an example response for this repository:

```bash
{
  "successful": true,
  "results": {
    "repository": "https://github.com/michtesar/repo-monitor",
    "average": 860.7727272727273,
    "std": 1061.2603541337999,
    "min": "2024-05-02T07:37:34",
    "max": "2024-05-02T12:53:11",
    "n_events": 23,
    "timestamps": [
      "2024-05-02T07:37:34",
      "2024-05-02T07:37:34",
      "2024-05-02T07:37:34",
      "2024-05-02T07:41:11",
      "2024-05-02T08:07:40",
      "2024-05-02T08:09:15",
      "2024-05-02T08:12:58",
      "2024-05-02T08:13:29",
      "2024-05-02T08:19:11",
      "2024-05-02T08:55:50",
      "2024-05-02T09:13:32",
      "2024-05-02T09:18:26",
      "2024-05-02T09:18:53",
      "2024-05-02T09:32:59",
      "2024-05-02T10:46:48",
      "2024-05-02T10:51:54",
      "2024-05-02T11:19:49",
      "2024-05-02T11:26:27",
      "2024-05-02T11:51:56",
      "2024-05-02T11:52:54",
      "2024-05-02T11:53:47",
      "2024-05-02T12:28:41",
      "2024-05-02T12:53:11"
    ],
    "duration": [
      0,
      0,
      217,
      1589,
      95,
      223,
      31,
      342,
      2199,
      1062,
      294,
      27,
      846,
      4429,
      306,
      1675,
      398,
      1529,
      58,
      53,
      2094,
      1470
    ]
  }
}
```
### Repositories

In order to specify the repositories, please only put the GitHub links to a public
ones in their common form (not the API one), such as:

https://github.com/michtesar/repo-monitor

There is validation check on the URL itself and on the number of the repositories as well.

The max number of repositories could be changed in the `config.py`.

## How it works

A FastAPI is being used as a backend for the application. If this was a production
application, we would consider implementing routers to enables `v1/api` or `v2/api` style
routes.

So far the application is opened on the empty (non-existing route - root /) - later we would
want to implement some frontend or router dict for specified API versions.

To query the GitHub API a `requests-cached` library is being used to cache the request
for 5 minutes in `sqllite3` database. Again, in production we would want a `/settings` endpoint
with authentication that would enable admins/users to change this. Also, it would be better to use
`PostgreSQL` database, which library support as well.

## How to run

### Development

For development run, please create a Python virtual environment with Python3.12:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

Then, install all production dependencies with:

```bash
pip install -r requirements.txt
```

For running the application, please utilize the `Makefile` targets. To see all
the options for development and run, run: `make help`. If you just run `make`
everything is going to be set for you automatically:
1. Clean the repository
2. Install all packages
3. Set the formatter and format, lint, check the code
4. Run all tests
5. Run the application

In case you only want to run the application you either use of `Makefile` target
```bash
make run
```

Which will run the application on the localhost on default port `8000` fot FastAPI applications.

Or you can use `uvicorn` to run the application they way you want (e.g., set the port):

```bash
uvicorn repo_monitor.main:app --port 5000
```

### Production

In production, a Docker container is highly recommended. Please, find included `Dockerfile` in the
repository, or use `Makefile` targets:

1. `make docker/build` - Build a Docker image with the name of `repo-monitor`
2. `make docker/run` - Run the image into container with the name of `repo-monitor`

In case of Docker a port `5000` is being used and exposed, so please navigate to:

- http://127.0.0.1:5000
or
- http://localhost:5000


## Used libraries

In order to visualize all the used libraries and their dependencies, please
find this table generated with `pip-licenses`:

| Name               | Version  | License                              |
|--------------------|----------|--------------------------------------|
| annotated-types    | 0.6.0    | MIT License                          |
| anyio              | 4.3.0    | MIT License                          |
| attrs              | 23.2.0   | MIT License                          |
| cattrs             | 23.2.3   | MIT License                          |
| certifi            | 2024.2.2 | Mozilla Public License 2.0 (MPL 2.0) |
| charset-normalizer | 3.3.2    | MIT License                          |
| click              | 8.1.7    | BSD License                          |
| fastapi            | 0.110.3  | MIT License                          |
| h11                | 0.14.0   | MIT License                          |
| idna               | 3.7      | BSD License                          |
| numpy              | 1.26.4   | BSD License                          |
| platformdirs       | 4.2.1    | MIT License                          |
| pydantic           | 2.7.1    | MIT License                          |
| pydantic-settings  | 2.2.1    | MIT License                          |
| pydantic_core      | 2.18.2   | MIT License                          |
| python-dotenv      | 1.0.1    | BSD License                          |
| requests           | 2.31.0   | Apache Software License              |
| requests-cache     | 1.2.0    | BSD License                          |
| six                | 1.16.0   | MIT License                          |
| sniffio            | 1.3.1    | Apache Software License; MIT License |
| starlette          | 0.37.2   | BSD License                          |
| typing_extensions  | 4.11.0   | Python Software Foundation License   |
| url-normalize      | 1.4.3    | MIT License                          |
| urllib3            | 2.2.1    | MIT License                          |
| uvicorn            | 0.29.0   | BSD License                          |

As it can be seen only free and open-source libraries were used.

### Security

No security vulnerabilities were found with `bandit` in distributed packages:

```
Run started:2024-05-02 13:07:53.668476

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 0
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

## Assignment Description

The objective of this assignment is to track activities on GitHub. To achieve this, utilize the GitHub Events API.

The application can monitor up to five configurable repositories. It generates statistics based on a rolling window of either 7 days or 500 events, whichever is less. These statistics are made available to end-users via a REST API. Specifically, the API will show the average time between consecutive events, separately for each combination of event type and repository name.

The application should minimize requests to the GitHub API and retain data through application restarts.

Please include a README file with your solution detailing the steps to run the application and a brief outline of your assumptions. Also, include reasonable documentation for fellow engineers and API users.

The assignment should be completed in Python.

It should take no more than 8 hours of cumulative work to finish. Please submit the best solution you can deliver within this time frame. If you do not manage to finish the solution fully, please report which parts are missing and sketch possible future work.

Please hand in your solution within 14 days as a ZIP file with a Git repository.
