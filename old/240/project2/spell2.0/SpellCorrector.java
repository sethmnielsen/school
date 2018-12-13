package spell;

import java.util.Iterator;
import java.util.TreeSet;
import java.io.IOException;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

import static java.lang.Character.*;

public class SpellCorrector implements ISpellCorrector {
	private Trie dict = new Trie();

	/**
	 * Tells this <code>SpellCorrector</code> to use the given file as its dictionary
	 * for generating suggestions.
	 * @param dictionaryFileName File containing the words to be used
	 * @throws IOException If the file cannot be read
	 */
	public void useDictionary(String dictionaryFileName) throws IOException {
		File f = new File(dictionaryFileName);
		Scanner s = null;
		try {
				s = new Scanner(f);
		} catch (FileNotFoundException e) {
				e.printStackTrace();
		}
		while (s.hasNext()) {
			dict.add(s.next());
		}
	}

	public String suggestSimilarWord(String inputWord) {
		inputWord = inputWord.toLowerCase();
		if (dict.find(inputWord) != null) {
			return inputWord;
		}
		else {
			TreeSet<String> edits = new TreeSet<String>();
			Trie.Node n = new Trie().new Node();
			Trie.Node n_maxf = new Trie().new Node();
			String new_word = new String();
			editWord(edits, inputWord);

			// Search through edit dist = 1 words, see if any are in Trie
			for (String s : edits) {
				n = dict.find(s);
				if (n != null) {
					// Compare the frequencies, take the largest one
					if (n.getValue() > n_maxf.getValue()) {
						n_maxf = n;
						new_word = s;
					}
				}
			}
			// If no word edit dist = 1, try again for edit dist = 2
			if (n_maxf.getValue() > 0) {
				return new_word;
			}
			else {
				TreeSet<String> edits2 = new TreeSet<String>(edits);
				for (String s : edits) {
					editWord(edits2, s);
				}
				for (String s : edits2) {
					n = dict.find(s);
					if (n != null) {
						// Compare the frequencies, take the largest one
						if (n.getValue() > n_maxf.getValue()) {
							n_maxf = n;
							new_word = s;
						}
					}
				}
				if (n_maxf.getValue() > 0) {
					return new_word;
				}
				return null;
			}
		}
	}

	public void editWord(TreeSet<String> edits, String word) {
		deletion(edits, word);
		transposition(edits, word);
		alteration(edits, word);
		insertion(edits, word);
	}

	/* For "bird",
	* Deletion Distance 1 - ird, brd, bid, bir
			4 strings that are DD of 1 from "bird"
			Size is 4 - 1
	* Transposition Distance - ibrd, brid, bidr
			(4 - 1) strings that are TD of 1 from "bird"
			Size is 4
	* Alteration Distance - (a-z,-b)ird, b(a-z,-i)rd, bi(a-z,-r)d, bir(a-z,-d)
			(25 * 4) strings AD of 1 from "bird"
			Size is 4
		Insertion Distance - (a-z)bird, b(a-z)ird, bi(a-z)rd, bir(a-z)d, bird(a-z)
			(26 * (4+1)) strings ID of 1 from "bird"
			Size is 4 + 1
		Only edit distance of 1 or 2
	*/

	public void deletion(TreeSet<String> edits, String word) {
		for (int i = 0; i < word.length()+1; i++){
			for (int j = 0; j < 26; j++) {
				StringBuilder sb = new StringBuilder(word);
				sb.insert(i,(char)(j+'a'));
				edits.add(sb.toString());
			}
		}
	}

	public void transposition(TreeSet<String> edits, String word) {
		for (int i = 0; i < word.length()-1; i++) {
			StringBuilder sb = new StringBuilder(word);
			sb.insert(i,word.charAt(i+1));
			edits.add(sb.deleteCharAt(i+2).toString());
		}
	}

	public void alteration(TreeSet<String> edits, String word) {
		for (int i = 0; i < word.length(); i++) {
			StringBuilder sb = new StringBuilder(word);
			for (int j = 0; j < 26; j++) {
				sb.setCharAt(i,(char)(j+'a'));
				edits.add(sb.toString());
			}
		}
	}

	public void insertion(TreeSet<String> edits, String word) {
		for (int i = 0; i < word.length(); i++) {
			StringBuilder sb = new StringBuilder(word);
			edits.add(sb.deleteCharAt(i).toString());
		}
	}
}
