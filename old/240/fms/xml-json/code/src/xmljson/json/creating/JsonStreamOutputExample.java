package xmljson.json.creating;

import com.fasterxml.jackson.core.*;

import java.io.*;

import xmljson.model.*;

public class JsonStreamOutputExample {

	public static void run() throws Exception {

		Catalog catalog = new Catalog();
		
		catalog.add(new CD("Hide your heart", "Bonnie Tyler", "UK",
				"CBS Records", 9.90f, 1988));
		catalog.add(new CD("Greatest Hits", "Dolly Parton", "USA",
				"RCA", 9.90f, 1982));
		catalog.add(new CD("Still got the blues", "Gary Moore", "UK",
                "Virgin records", 10.20f, 1990));

		StringWriter sw = new StringWriter();
		JsonFactory f = new JsonFactory();
		JsonGenerator jsonGen = f.createGenerator(sw);
		jsonGen.useDefaultPrettyPrinter();

		saveCatalog(catalog, jsonGen);

        jsonGen.flush();
		
		System.out.println(sw.toString());
	}
	
	private static void saveCatalog(Catalog catalog, JsonGenerator jsonGen) 
		throws Exception {

		jsonGen.writeStartObject();
		jsonGen.writeFieldName("CATALOG");

		jsonGen.writeStartArray();
		for (CD cd : catalog.getItems()) {
			saveCD(cd, jsonGen);
		}
		jsonGen.writeEndArray();

		jsonGen.writeEndObject();
	}
	
	private static void saveCD(CD cd, JsonGenerator jsonGen) throws Exception {

		jsonGen.writeStartObject();
		jsonGen.writeFieldName("CD");

		jsonGen.writeStartObject();
		jsonGen.writeFieldName("TITLE");
		jsonGen.writeString(cd.getTitle());
		jsonGen.writeFieldName("ARTIST");
		jsonGen.writeString(cd.getArtist());
		jsonGen.writeFieldName("COUNTRY");
		jsonGen.writeString(cd.getCountry());
		jsonGen.writeFieldName("COMPANY");
		jsonGen.writeString(cd.getCompany());
		jsonGen.writeFieldName("PRICE");
		jsonGen.writeNumber(cd.getPrice());
		jsonGen.writeFieldName("YEAR");
		jsonGen.writeNumber(cd.getYear());
		jsonGen.writeEndObject();

		jsonGen.writeEndObject();
	}

}
