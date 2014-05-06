Allows you to use many differents, yet strong password. From your main password and a "target" (ie the website you create a password for) the tools will generate a password (using the scrypt hash function).

The password file is encrypted using AES, and do not contains password. It contains some information that helps the tools to derive your password (target and password size).


This code is not tested, and is not very secure (for example the master password lives unencrypted in memory for the duration of the program).