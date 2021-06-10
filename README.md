# Characterizing Logging in Data Science and Non Data Science Github Repositories - Java

The software engineering applications are known to follow the product quality rigour. Application logging is one of the standard practice to bring software engineering rigour. The logs are used for debugging, testing, execution path analysis and many more use cases.

In the recent times, the data science projects are being integrated into mainstream software engineering applications.  

In this work, we quantitively and qualitatively analyze Logging practices of Data Science and Non-Data Science (Software Engineering) applications.


## Data
Data is acquired using GitHub API. Search query for DataScience : [Link](https://api.github.com/search/repositories?page=1&per_page=100&q=data+science+java+language:java), search query for Non-DataScience : [Link](https://api.github.com/search/repositories?page=1&per_page=100&q=java+projects+language:java).

## Input
The input file contains the list of repos of data science and non-data science in csv format, it resides in `data/input` directory.

## Using Semgrep rules
Logs were extracted from the repos using two semgrep rules.
### Log Instances
The [log instances rule](https://semgrep.dev/s/krishnatejaj:log_count_java) is used to extract logs in the following categories
* print
* log4j
* slf4j
* tinylog
* logging


```
rules:
  - fix: ""
    id: print
    languages:
      - java
    message: Match found print
    pattern-either:
      - pattern: System.out.print(...);
      - pattern: System.out.println(...);
      - pattern: System.err.print(...);
    severity: WARNING
  - fix: ""
    id: log4j
    languages:
      - java
    message: Match found for log4j
    patterns:
      - pattern-either:
          - pattern: $A.info(...);
          - pattern: $A.error(...);
          - pattern: $A.warn(...);
          - pattern: $A.debug(...);
          - pattern: $A.trace(...);
      - pattern-inside: |
          import org.apache.log4j.$B;
          ...
    severity: WARNING
  - fix: ""
    id: slf4j
    languages:
      - java
    message: Match found for slf4j
    patterns:
      - pattern-either:
          - pattern: $C.info(...);
          - pattern: $C.error(...);
          - pattern: $C.warn(...);
          - pattern: $C.debug(...);
          - pattern: $C.trace(...);
      - pattern-inside: |
          import org.slf4j.$D;
          ...
    severity: WARNING
  - fix: ""
    id: tinylog
    languages:
      - java
    message: Match found for tinylog
    patterns:
      - pattern-either:
          - pattern: $E.info(...);
          - pattern: $E.error(...);
          - pattern: $E.warn(...);
          - pattern: $E.debug(...);
          - pattern: $E.trace(...);
      - pattern-inside: |
          import org.tinylog.Logger;
          ...
    severity: WARNING
  - fix: ""
    id: logging
    languages:
      - java
    message: Match found for logging
    patterns:
      - pattern-either:
          - pattern: $F.finest(...);
          - pattern: $F.finer(...);
          - pattern: $F.fine(...);
          - pattern: $F.config(...);
          - pattern: $F.info(...);
          - pattern: $F.warning(...);
          - pattern: $F.severe(...);
          - pattern: $G.$H(Level.FINEST,...);
          - pattern: $G.$H(Level.FINER,...);
          - pattern: $G.$H(Level.FINE,...);
          - pattern: $G.$H(Level.CONFIG,...);
          - pattern: $G.$H(Level.INFO,...);
          - pattern: $G.$H(Level.WARNING,...);
          - pattern: $G.$H(Level.SEVERE,...);
      - pattern-inside: |
          import java.util.logging.$I;
          ...
    severity: WARNING

```


`./scripts/log_instances.py` implements the log extraction in the above categories

### Log Level
The [log level rule](https://semgrep.dev/s/krishnatejaj:log_level_java) is used to extract logs in the following categories
* class
* method
* info 
* error 
* warning 
* debug
* trace


```
rules:
  - fix: ""
    id: class_
    languages:
      - java
    message: Match found for class_
    patterns:
      - pattern: class $CNAME {...}
      - metavariable-regex:
          metavariable: $CNAME
          regex: ^((?!log).)*$
    severity: WARNING
  - fix: ""
    id: method_
    languages:
      - java
    message: Match found for method_
    patterns:
      - pattern: $RTYPE $METHOD(...) {...}
      - metavariable-regex:
          metavariable: $RTYPE
          regex: (void|char|int|float|double)
      - metavariable-regex:
          metavariable: $METHOD
          regex: ^((?!log).)*$
    severity: WARNING
  - fix: ""
    id: end_line_
    languages:
      - java
    message: Match found for end_line_
    patterns:
      - pattern-regex: (.*)$
    severity: WARNING
  - fix: ""
    id: info
    languages:
      - java
    message: Match found for info
    pattern-either:
      - pattern: System.out.print(...)
      - pattern: System.out.println(...)
      - pattern: $C.info(...)
    severity: WARNING
  - fix: ""
    id: error
    languages:
      - java
    message: Match found for error
    pattern-either:
      - pattern: System.out.print("=~/.*[eE][rR][rR][oO][rR].*/")
      - pattern: System.out.println("=~/.*[eE][rR][rR][oO][rR].*/")
      - pattern: $D.error(...)
      - pattern: System.err.print(...)
    severity: WARNING
  - fix: ""
    id: warning
    languages:
      - java
    message: Match found for warning
    pattern-either:
      - pattern: System.out.print("=~/.*[wW][aA][rR][nN][iI][nN][gG].*/")
      - pattern: $E.warn(...)
      - pattern: $G.warning(...)
      - pattern: System.out.println("=~/.*[wW][aA][rR][nN][iI][nN][gG].*/")
    severity: WARNING
  - fix: ""
    id: debug
    languages:
      - java
    message: Match found for debug
    pattern-either:
      - pattern: System.out.print("=~/.*[dD][eE][bB][uU][gG].*/")
      - pattern: System.out.println("=~/.*[dD][eE][bB][uU][gG].*/")
      - pattern: $F.debug(...)
    severity: WARNING
  - fix: ""
    id: trace
    languages:
      - java
    message: Match found for trace
    pattern: $F.trace(...)
    severity: WARNING

```


`./scripts/log_level.py` implements the log extraction in the above categories

### Log Churn
Extracted the code churn of the last 10 commits of data science and non-data science projects to review the improvement in quantity and quality of logs.<br>
`./scripts/logvnlog.py` extracts and categorises Data Science and Non Data Science code churns.

## Output
After applying the Semgrep rules, the following outputs files were generated.

`./scripts/final_export.py` outputs `./output/FINAL.csv`<br> 
The output file consists of log instances count, log density, log level count, code churn of all java files in every repository and the log details of a specific java file in a repo.<br>
This file is used to calculate Gini Index of the repositories to analyze logging inequalities of Data Science and Non-Data Science GitHub repos - Java.

`./scripts/gini_index.py` outputs `./output/gini_index.xlsx`<br>
The output file contains the gini index of the repository, file level (includes log level categories), class level (includes log level categories) and method level (includes log level categories).

`./scripts/final_export2.py` outputs `./output/LogMetrics-Summarized.xlsx`<br>
The output file consists summary of log instances count, log level count, churn and log statements of Data Science and Non-Data Science repositories.


___
