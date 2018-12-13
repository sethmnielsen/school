package xmljson.json.parsing;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;

import java.io.*;

public class JsonTreeInputExample {

	public static void run(File file) throws Exception {

		ObjectMapper m = new ObjectMapper();
		
		ObjectNode rootObj = (ObjectNode)m.readTree(file);

        ArrayNode cdArr = (ArrayNode)rootObj.get("CATALOG");
		for (int i = 0; i < cdArr.size(); ++i) {

            ObjectNode elemObj = (ObjectNode)cdArr.get(i);
            ObjectNode cdObj = (ObjectNode)elemObj.get("CD");

            TextNode titleNode = (TextNode)cdObj.get("TITLE");
            TextNode artistNode = (TextNode)cdObj.get("ARTIST");

			System.out.println(titleNode.textValue() + ", " + 
								artistNode.textValue());
		}		
	}
	
}
