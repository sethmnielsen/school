package xmljson.json.creating;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;

import java.io.*;

import xmljson.model.*;

public class JsonObjectSerializationOutputExample {

	private static ObjectMapper m = new ObjectMapper();
	
	public static void run() throws Exception {

		Catalog catalog = new Catalog();

        catalog.add(new CD("Hide your heart", "Bonnie Tyler", "UK",
                "CBS Records", 9.90f, 1988));
        catalog.add(new CD("Greatest Hits", "Dolly Parton", "USA",
                "RCA", 9.90f, 1982));
        catalog.add(new CD("Still got the blues", "Gary Moore", "UK",
                "Virgin records", 10.20f, 1990));

		ObjectWriter objWriter = m.writerWithDefaultPrettyPrinter();
        String jsonStr = objWriter.writeValueAsString(catalog);
		System.out.println(jsonStr);
	}

}
