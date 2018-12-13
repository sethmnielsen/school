package xmljson.json.creating;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;

import java.io.*;

import xmljson.model.*;

public class JsonTreeOutputExample {

	private static ObjectMapper m = new ObjectMapper();
	
	public static void run() throws Exception {

		Catalog catalog = new Catalog();

        catalog.add(new CD("Hide your heart", "Bonnie Tyler", "UK",
                "CBS Records", 9.90f, 1988));
        catalog.add(new CD("Greatest Hits", "Dolly Parton", "USA",
                "RCA", 9.90f, 1982));
        catalog.add(new CD("Still got the blues", "Gary Moore", "UK",
                "Virgin records", 10.20f, 1990));

		ObjectNode catalogObj = buildCatalog(catalog);

		ObjectWriter objWriter = m.writerWithDefaultPrettyPrinter();
        String jsonStr = objWriter.writeValueAsString(catalogObj);
		System.out.println(jsonStr);
	}
	
	private static ObjectNode buildCatalog(Catalog catalog) throws Exception {

		ArrayNode cdArr = m.createArrayNode();
		for (CD cd : catalog.getItems()) {
			cdArr.add(buildCD(cd));
		}

		ObjectNode catalogObj = m.createObjectNode();
		catalogObj.put("CATALOG", cdArr);

		return catalogObj;
	}
	
	private static ObjectNode buildCD(CD cd) throws Exception {

		ObjectNode cdObj = m.createObjectNode();

		cdObj.put("TITLE", cd.getTitle());
		cdObj.put("ARTIST", cd.getArtist());
		cdObj.put("COUNTRY", cd.getCountry());
		cdObj.put("COMPANY", cd.getCompany());
		cdObj.put("PRICE", cd.getPrice());
		cdObj.put("YEAR", cd.getYear());

		return cdObj;
	}

}
