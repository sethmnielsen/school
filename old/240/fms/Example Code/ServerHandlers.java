

package cs240;

import java.io.*;
import java.net.*;
import java.util.*;
import com.sun.net.httpserver.*;
import static java.net.HttpURLConnection.HTTP_OK;

class Server {

    public static void main(String[] args) throws Exception {

	Server server = new Server();
	server.startServer();
	
    }

    void startServer() throws Exception {

	int port = 8888;
	
	System.out.println("server listening on port: " + port);
	System.out.println();
	
	HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

	server.createContext("/", new RootHandler());

	server.start();
	
    }
    
    class RootHandler implements HttpHandler {
	@Override
	public void handle(HttpExchange exchange) throws IOException {

	    System.out.println("SERVER: root handler");
	    System.out.println();

	    getRequestHeaders(exchange);

	    getRequestBody(exchange);

	    exchange.sendResponseHeaders(HTTP_OK, 0);

	    sendResponseBody(exchange);

	    System.out.println();

	}
    }

    void getRequestHeaders(HttpExchange exchange) {

	System.out.println("request:");

	String method = exchange.getRequestMethod();
	System.out.println("method: " + method);
		    
	URI uri = exchange.getRequestURI();
	System.out.println("uri: " + uri);
		    
	String auth = exchange.getRequestHeaders().getFirst("Authorization");
	System.out.println("auth: " + auth);

	System.out.println();

	printHeaders(exchange.getRequestHeaders());

    }

    void getRequestBody(HttpExchange exchange) {

	System.out.println("request body:");

	Scanner in = new Scanner(exchange.getRequestBody());
	while (in.hasNextLine())
	    System.out.println(in.nextLine());
	in.close();

	System.out.println();

    }

    void sendResponseBody(HttpExchange exchange) {

	String response = "[Mock Server Response]";

	PrintWriter out = new PrintWriter(exchange.getResponseBody());
	out.print(response);
	out.close();

	System.out.println("response body:");
	System.out.println(response);
	System.out.println();

    }

    void printHeaders(Map<String, List<String>> headers) {

	System.out.println("request headers:");

	for (String name : headers.keySet())
	    System.out.println(name + " = " + headers.get(name));

	System.out.println();

    }

}


