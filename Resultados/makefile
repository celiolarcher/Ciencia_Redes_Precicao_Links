all: 	execute.class

execute.class:execute.java
	javac -cp weka.jar:classifierBasedAttributeSelection.jar execute.java

run: 
	java -cp .:weka.jar:classifierBasedAttributeSelection.jar execute

clean:
	rm execute.class
