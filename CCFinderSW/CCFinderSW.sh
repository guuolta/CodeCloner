#!/bin/bash

string_project=$1
string_output=${string_project}_outputtxt

java -jar ~/Documents/CCFinderSW-1.0/lib/CCFinderSW-1.0.jar D -d /Users/ogurayuuki/Documents/CCFinderSW-1.0/RemoveUsingFiles/${string_project} -l csharp -w 2 -o ${string_output} -ccfsw set

mv -f ${string_output}_ccfsw.txt ~/Documents/CCFinderSW-1.0/Outputs