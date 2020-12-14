def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    import platform    # For getting the operating system name
    import subprocess  # For executing a shell command
    
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def connect_to_db_server(user, password, 
    database, host="db", port="5432"):
    """ Connect to database server with provided environment variables """
    from psycopg2 import connect
    try:
        connection = connect(
                user=user,
                password=password,
                database=database,
                host=host,
                port=port)
        cursor = connection.cursor()
        #print("Successfully connected to Postgres Server\n")
        return connection
    except Exception as e:
        #print(f"could not connect to the postgres {e}\n")
        return None