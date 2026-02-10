TOMCAT_WEBAPPS=/opt/homebrew/opt/tomcat/libexec/webapps
WAR_NAME=calculatrice-servlet-1.0.0.war


run:
	mvn clean package
	test -f target/$(WAR_NAME)
	cp target/$(WAR_NAME) $(TOMCAT_WEBAPPS)/calculatrice-servlet.war
	catalina run
