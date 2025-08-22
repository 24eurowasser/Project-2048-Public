import socket
from threading import Thread
import ipaddress


class ControllerClient:
    """This class implements the client part that sends commands to the server."""

    def __init__(self, hostname):
        """
        Constructor of the class ControllerClient.

        Parameters:
        ----------
        hostname: str
            ip adress of the server
        """
        # Validate the IP address
        if self._validate_ip_address(ip_string=hostname):
            self._hostname = hostname
        else:
            # If the entered IP address is invalid, then just generate a false IP address that is at least valid.
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self._hostname = ip_address

        t1 = Thread(target=self._send_messages, daemon=False)
        t1.start()

    def _send_messages(self) -> None:
        """Sets up the client"""
        running = True
        while running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                server_address = (self._hostname, 2048)
                client_socket.connect(server_address)

                inp: str = input("Please choose command (w, a, s, d, pause, start, exit, restart, quit client): ")
                if inp.lower() == "quit client":
                    running = False

                bytes_to_send = bytes(inp, "utf-8")
                client_socket.sendall(bytes_to_send)

    def _validate_ip_address(self, ip_string: str) -> bool:
        try:
            # If building an IP address object fails, then it's not a valid input.
            temp_object = ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False
