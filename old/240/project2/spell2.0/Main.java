package spell;

import java.io.IOException;

public class Main {

	public static void main(String[] args) throws IOException {

		String dictionaryFileName = args[0];
		String inputWord = args[1];

		SpellCorrector corrector = new SpellCorrector();

		corrector.useDictionary(dictionaryfFileName);
		String suggestion = corrector.suggestSimilarWord(inputWord);
		if (suggestion == null) {
		    suggestion = "No similar word found";
		}

		System.out.println("Suggestion is: " + suggestion);
	}

}
