# Calculator : CGI & Java Servlets (Tomcat)

This project implements the same calculator application in two server-side approaches:
  - CGI (Python) using HTTP cookies to store the last access time
  - Java Servlets (Tomcat) using HttpSession to store the last access time

Both versions support:
  - Addition (+)
  - Subtraction (-)
  - Multiplication (×)
  - Division (÷)


## CGI

<div style="display:flex; justify-content:center;">
  <video controls style="max-width:900px; width:100%; border-radius:12px;">
    <source src="./assets/cgi.mp4" type="video/mp4" />
  </video>
</div>

<div style="display:flex; justify-content:center;">
Demo video: <a href="./assets/cgi.mp4"> CGI Demo </a> 
</div>

***This version uses Python CGI scripts executed by the web server.***

Since Python 3.13 removed the deprecated cgi module, request parsing was implemented using:

- CGI environment variables (QUERY_STRING, CONTENT_LENGTH, REQUEST_METHOD)
- Standard libraries (urllib.parse)

This still follows the CGI specification.

### State Management (Cookie)

A cookie named `last_access` is used to store the user's last access time.
If the cookie exists, the script displays the previous access time. 
The cookie is updated on every request using the ***Set-Cookie header***.

## Java Servlets - Using Tomcat

<div style="display:flex; justify-content:center;">
  <video controls style="max-width:900px; width:100%; border-radius:12px;">
    <source src="./assets/servlet.mp4" type="video/mp4" />
  </video>
</div>

<div style="display:flex; justify-content:center;">
Demo video: <a href="./assets/servlet.mp4"> Servlet Demo </a> 
</div>


***This version uses Java Servlets running on Tomcat.*** 

### State Management (HttpSession)

The servlet uses `HttpSession` to store the user's last access time.
The session attribute is updated on every request.
The previous access time is displayed when available.

### CGI vs Servlets : A Comparison

In the CGI version, the state `last_access` is stored on the client side using an ***HTTP cookie***.
In the Servlet version, the state is stored on the ***server side*** using `HttpSession`.

- Cookies are simple and lightweight, but the client can modify them, so they are less secure and less trustworthy.
- Sessions give the server more control and are harder for the user to tamper with.
- CGI can be less efficient because each request may start a new process, while servlets run inside a long-lived server container.
- Sessions can use more server memory, but provide better control for authentication and user state.

## Project Structure

```txt
.
├── cgi/                  # Python CGI version (cookies)
├── servlet/              # Java servlet version (Tomcat + HttpSession)
├── assets/               # Demo videos (cgi.mp4, servlet.mp4)
├── Makefile              # Commands to run both versions
└── README.md
```

## Running the project locally

If you don't have make installed, please do so here :  [https://www.gnu.org/software/make/](https://www.gnu.org/software/make/)

### Running CGI

```bash
# Mac/Linux (Python3)
make run-cgi

# On Windows Machines with Python
make run-cgi-win
```

Once cgi is running, you can visit `http://localhost:8000/` and use the calculator

### Running Servlet

Servlet uses tomcat,

##### Requirements :

- Java (JDK 17+ recommended)
- Apache Tomcat 10.x (Servlet API Jakarta)

###### Build the WAR file 

```bash
cd servlet
mvn clean package
```

This generates a .war file in: `servlet/target/`

###### Deploy to Tomcat

Copy the WAR into Tomcat’s webapps/ folder:

```bash
cp target/*.war /path/to/tomcat/webapps/
```

Then start Tomcat: 

```bash
/path/to/tomcat/bin/startup.sh
```

##### Open the servlet in your browser

Once Tomcat is running, you can visit `http://localhost:8080/calculatrice-servlet/index.html` and use the calculator

##### Shutdown Tomcat

You can run `/path/to/tomcat/bin/shutdown.sh` to stop tomcat

> Built with <3 by Aditya - CSI 3540 A Winter 2025 @ UOttawa
