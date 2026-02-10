# Python Environment

```bash
source venv/
```

> We used Python CGI scripts executed by the web server. Since Python 3.13 removed the deprecated `cgi` module, request parsing was implemented using environment variables (`QUERY_STRING`, `CONTENT_LENGTH`, `REQUEST_METHOD`) and standard libraries (`urllib.parse`). This still follows the CGI specification.
