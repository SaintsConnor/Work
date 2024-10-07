// Simple Client to connect to a server and receive messages

#include <iostream>
#include <string>
#include <WS2tcpip.h>
pragma comment(lib, "ws2_32.lib")

using namespace std;

// Main Function
int Main() {
	// Initialize Winsock
	WSADATA wsData;
	WORD ver = MAKEWORD(2, 2);

	int wsOk = WSAStartup(ver, &wsData);
	if (wsOk != 0) {
		cerr << "Can't Initialize Winsock! Quitting" << endl;
		return 1;
	}

	// Create a socket
	SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock == INVALID_SOCKET) {
		cerr << "Can't create a socket! Quitting" << endl;
		return 1;
	}

	// Fill in a hint structure
	string ipAddress;
	cout << "Enter IP Address of the server: ";
	getline(cin, ipAddress);
	int port = 54000;
	sockaddr_in hint;
	hint.sin_family = AF_INET;

	hint.sin_port = htons(port);
	inet_pton(AF_INET, ipAddress.c_str(), &hint.sin_addr);

	// Connect to the server
	int connResult = connect(sock, (sockaddr*)&hint, sizeof(hint));
	if (connResult == SOCKET_ERROR) {
		cerr << "Can't connect to server! Quitting" << endl;
		closesocket(sock);
		WSACleanup();
		return 1;
	}

	// Do-while loop to send and receive data
	char buf[4096];
	string userInput;

	do {
		// Prompt the user for some text
		cout << "> ";
		getline(cin, userInput);

		if (userInput.size() > 0) {
			// Send the text
			int sendResult = send(sock, userInput.c_str(), userInput.size() + 1, 0);
			if (sendResult != SOCKET_ERROR) {
				// Wait for response
				ZeroMemory(buf, 4096);
				int bytesReceived = recv(sock, buf, 4096, 0);
				if (bytesReceived > 0) {
					// Echo response to console
					cout << "SERVER> " << string(buf, 0, bytesReceived) << endl;
				}
			}
		}
	} while (userInput.size() > 0);

	// Gracefully close down everything
	closesocket(sock);
	WSACleanup();
}