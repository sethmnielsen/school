package xmljson;

import java.io.*;

import xmljson.json.creating.*;
import xmljson.json.parsing.*;

public class Main {
	
	public static void main(String[] args) {
		
		try {
			JsonStreamInputExample.run(new File("cd_catalog.json"));
			JsonStreamOutputExample.run();

			JsonTreeInputExample.run(new File("cd_catalog.json"));
			JsonTreeOutputExample.run();

			JsonObjectSerializationInputExample.run(new File("serialized_cd_catalog.json"));
			JsonObjectSerializationOutputExample.run();
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
}