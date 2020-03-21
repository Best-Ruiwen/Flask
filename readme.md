The content of this project is the IoT data management platform, and it is based on Flask framework.
Required additional python packages:
    1. flask;
    2. pycryptodome;
    3. redis.

Usage:
    A. On Windows machine:python main.py and open "http://127.0.0.1/" in browser

    B. On Linux machine(Ubuntu 16.04):
        1. Enter the 'configure' folder
        2. Run 'sudo chmox 777 configure.sh' in terminal
        3. Run './configure.sh' in terminal
        4. open "http://127.0.0.1/" in browser

    C. Test account:2016212707
            password:riven

Attention:
    1. No data for the last 7 days in the database for testing. 
    2. You can register new device if you have a machine which can upload data by http protocol.
    3. You can write data directly to database.