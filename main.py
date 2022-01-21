class IPcalculator(object):
    """
    Class containing methods which calculate network and broadcast IP addresses,
    host count and calculates the mask IP address based on its shortened form

    @:param ip: IP address with mask, eg. 192.168.1.101/24
    """

    def __init__(self, ip):
        self.ip = ip.split("/")[0].split(".")
        self.full_mask = self.get_mask(ip)[0]
        self.shortened_mask = self.get_mask(ip)[1]

    def get_mask(self, ip):
        """
        Converts shortened mask to full form (eg. /24 to 255.255.255.0)

        @:returns tuple: eg. output[0]: 255.255.255.0, output[1]: /24
        """
        mask_short = int(ip.split("/")[1])
        octets = mask_short//8
        rest = mask_short - octets * 8
        mask = [str(int(8 * "1", 2)) for i in range(octets)]
        if rest > 0:
            string = f"{rest * '1'}{(8 - rest) * '0'}"
            mask.append(str(int(string, 2)))

        for i in range(3 - octets):
            mask.append("0")

        return ".".join(mask), mask_short

    def convert_ip(self, ip: list, out_base: int = 2):
        """
        Method which converts IP address to binary or decimal form.

        :param ip: IP address
        :param out_base: Decide if IP should be in binary form or decimal form
        :return list: converted IP address in form of list
        """
        if type(ip) is not list:
            ip = str(ip).split(".")

        o_ip = []
        if out_base == 2:
            '''Converts to bin'''
            for i in ip:
                binary = bin(int(i))[2:]
                if len(binary) < 8:
                    binary = f"{(8 - len(binary)) * '0'}{binary}"
                o_ip.append(binary)
        elif out_base == 10:
            '''Converts to dec'''
            for i in ip:
                o_ip.append(str(int(i, 2)))

        return o_ip

    def network_address(self):
        """
        Calculates the network address

        :returns string: Network address for IP specified in class
        """

        ip_bin = self.convert_ip(self.ip)
        ip_mask = self.convert_ip(self.full_mask.split("."))
        network_octet = ""
        network_ip = []

        for i in range(len(ip_bin)):
            for j in range(len(ip_bin[i])):
                network_octet += str(int(ip_bin[i][j]) * int(ip_mask[i][j]))
            network_ip.append(network_octet)
            network_octet = ""

        return ".".join(self.convert_ip(network_ip, 10))

    def broadcast_address(self):
        """Calculates the broadcast address, returns string"""

        ip_bin = self.convert_ip(self.ip)
        ip_mask = self.convert_ip(self.full_mask.split("."))
        broadcast_octet = ""
        broadcast_ip = []
        counter = 0

        for i in range(len(ip_bin)):
            for j in range(len(ip_bin[i])):
                if counter < self.shortened_mask:
                    broadcast_octet += str(int(ip_bin[i][j]) * int(ip_mask[i][j]))
                else:
                    broadcast_octet += "1"
                counter += 1
            broadcast_ip.append(broadcast_octet)
            broadcast_octet = ""

        return ".".join(self.convert_ip(broadcast_ip, 10))

    def host_count(self):
        """Calculates the host count for specified network"""
        return 2**(32 - self.shortened_mask) - 2

    def __str__(self):
        """Prints a set of information about the network of specified IP address."""

        return f"Adres IP: \t\t\t\t {'.'.join(self.ip)}\n" \
               f"Maska: \t\t\t\t\t {self.full_mask} (/{self.shortened_mask})\n" \
               f"Adres sieci: \t\t\t {self.network_address()}\n" \
               f"Adres rozgłoszeniowy:\t {self.broadcast_address()}\n" \
               f"Ilość hostów: \t\t\t {self.host_count()}"


ip = [
    "145.123.17.145/13",
    "134.123.17.176/17",
    "187.143.17.123/18",
    "164.124.17.134/23",
    "154.156.17.155/12",
    "165.123.17.123/19",
    "123.123.17.154/28",
    "134.122.17.134/22",
    "123.166.17.133/15",
    "133.23.17.155/3"
]

for i in ip:
    print(IPcalculator(i))
    print("----------")


if __name__ == '__main__':
    pass
