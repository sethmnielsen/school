package xmljson.json.parsing;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;

import java.io.*;

import xmljson.model.*;

public class JsonObjectSerializationInputExample {

	public static void run(File file) throws Exception {

		ObjectMapper m = new ObjectMapper();
		Catalog catalog = m.readValue(file, Catalog.class);
		
		for (CD cd : catalog.getItems()) {
            System.out.println(cd.getTitle() + ", " + cd.getArtist());
		}
	}
	
}
