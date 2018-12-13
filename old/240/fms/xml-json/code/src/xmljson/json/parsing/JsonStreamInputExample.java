package xmljson.json.parsing;

import com.fasterxml.jackson.core.*;

import java.io.*;

public class JsonStreamInputExample {

	private static void parseExpectedToken(JsonParser parser, JsonToken token)
		throws Exception {
			
		if (parser.nextToken() != token)
			throw new Exception();
	}
	
	public static void run(File file) throws Exception {
		
		// Use streaming JSON parser to find list of CD titles and artists

		JsonFactory f = new JsonFactory();
		JsonParser parser = f.createParser(file);
		
		parseExpectedToken(parser, JsonToken.START_OBJECT);
		parseExpectedToken(parser, JsonToken.FIELD_NAME); // skip "CATALOG" property name
		parseExpectedToken(parser, JsonToken.START_ARRAY);

        String title = "";
        String artist = "";

        while (parser.nextToken() == JsonToken.START_OBJECT) {

			parseExpectedToken(parser, JsonToken.FIELD_NAME); // skip "CD" property name
			parseExpectedToken(parser, JsonToken.START_OBJECT);

            while (parser.nextToken() == JsonToken.FIELD_NAME) {
                String propName = parser.getCurrentName();
                switch (propName) {
                    case "TITLE":
                        title = parser.nextTextValue();
                        break;
                    case "ARTIST":
                        artist = parser.nextTextValue();
                        break;
                    default:
                        parser.nextToken();	// skip property value
                        break;
                }
            }

            System.out.println(title + ", " + artist);

			parseExpectedToken(parser, JsonToken.END_OBJECT);
        }

		parseExpectedToken(parser, JsonToken.END_OBJECT);
	}
	
}
