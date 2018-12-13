package com.example;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class EvilHangmanGame {
	private TreeSet<String> dict_set = new TreeSet<String>();
	private TreeSet<String> prev_guesses = new TreeSet<String>();
	private int len;
	private StringBuilder word = new StringBuilder();

	public static class GuessAlreadyMadeException extends Exception {

	}

	/**
	 * Starts a new game of evil hangman using words from <code>dictionary</code>
	 * with length <code>wordLength</code>.
	 *	<p>
	 *	This method should set up everything required to play the game,
	 *	but should not actually play the game. (ie. There should not be
	 *	a loop to prompt for input from the user.)
	 *
	 * @param dictionary Dictionary of words to use for the game
	 * @param wordLength Number of characters in the word to guess
	 */
	public void startGame(File dictionary, int wordLength) {
		len = wordLength;
		for (int i = 0; i < len; i ++) {
			word.append("-");
		}
		String cur_word;
		Scanner s = null;
		try {
				s = new Scanner(dictionary);
		} catch (FileNotFoundException e) {
				e.printStackTrace();
		}
		while (s.hasNext()) {
			cur_word = s.next();
			if (cur_word.length() == wordLength) dict_set.add(cur_word.toLowerCase());
		}
  }

	/**
	 * Make a guess in the current game.
	 *
	 * param guess The character being guessed
	 *
	 * return The set of strings that satisfy all the guesses made so far
	 * in the game, including the guess made in this call. The game could claim
	 * that any of these words had been the secret word for the whole game.
	 *
	 * throws GuessAlreadyMadeException If the character <code>guess</code>
	 * has already been guessed in this game.
	 */
	public Set<String> makeGuess(char c) throws GuessAlreadyMadeException {
		StringBuilder sbc = new StringBuilder();
		sbc.append(c);
		if (prev_guesses.contains(sbc.toString())) {
			throw new GuessAlreadyMadeException();
		}
		else {
			prev_guesses.add(sbc.toString());
		}
		Map<String, TreeSet<String>> part_map = new TreeMap<String, TreeSet<String>>();
		StringBuilder sb = new StringBuilder();
		for (String s : dict_set) {
			sb.delete(0, len);
			for (int i = 0; i < len; i++) {
				if (s.charAt(i) == c) sb.append(c);
				else sb.append("-");
			}
			if (part_map.get(sb.toString()) == null) {
				TreeSet<String> ts = new TreeSet<String>();
				ts.add(s);
				part_map.put(sb.toString(), ts);
			}
			else part_map.get(sb.toString()).add(s);
		}

		String part = new String();
		int maxSize = 0;
		for (String key : part_map.keySet()) {
			if (part_map.get(key).size() > maxSize) {
				part = key;
				maxSize = part_map.get(key).size();
			}
			// Tie-breaker cases
			else if (part_map.get(key).size() == maxSize) {
				// Choose partition that doesn't contain guess
				if (part.contains(String.valueOf(c)) && !key.contains(String.valueOf(c))) part = key;
				else if (part.contains(String.valueOf(c)) && key.contains(String.valueOf(c))) {
					// Choose partition that has the fewest letters
					int cnt_lar = 0;
					int cnt_key = 0;
					for (int i = 0; i < len; i++) {
						if (part.charAt(i) == c) cnt_lar++;
						if (key.charAt(i) == c) cnt_key++;
					}
					if (cnt_key < cnt_lar) part = key;
					else if (cnt_key == cnt_lar) {
						// Choose partition with the rightmost guessed letter
						String c_str = Character.toString(c);
						int k = key.lastIndexOf(c_str);
						int l = part.lastIndexOf(c_str);
						if (k > l) part = key;
						else if (k == l) {
							// Choose partition with next rightmost guessed letter; repeat
							String key2 = key;
							String part2 = part;
							while (k == l) {
								key2 = key2.substring(0, k);
								part2 = part2.substring(0, l);
								k = key2.lastIndexOf(c_str);
								l = part.lastIndexOf(c_str);
								if (k > l) part = key;
							}
						}
					}
				}
			}
		}
		int counter = 0;
		for (int i = 0; i < len; i++) {
			if (part.charAt(i) == c) {
				word.setCharAt(i, c);
				counter++;
			}
		}
		if (counter == 0) {
			System.out.println("Sorry, there are no " + c + "'s");
			System.out.println();
		}
		else {
			System.out.println("Yes, there is " + counter + " " + c);
			System.out.println();
		}

		dict_set = part_map.get(part);
		return dict_set;
  }

	public TreeSet<String> getDict() {
		return dict_set;
	}

	public TreeSet<String> getPrevGuesses() {
		return prev_guesses;
	}

	public String getWord() {
		return word.toString();
	}

	public boolean checkGuess(String guess) {
		if (guess == null
				|| guess.length() > 1
				|| guess.length() == 0
				|| !Character.isLetter(guess.charAt(0))) return false;
		return true;
	}

}
