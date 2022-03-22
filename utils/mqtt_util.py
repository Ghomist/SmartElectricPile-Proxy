def on_rc(rc) -> str:
    on_rc = {
        '0': "Accepted",
        '1': "Refused, unacceptable protocol version",
        '2': "Refused, identifier rejected",
        '3': "Refused, server unavailable",
        '4': "Refused, bad user name or password",
        '5': "Refused, not authorized",
    }
    return on_rc.get(rc, "Unknown return code")
