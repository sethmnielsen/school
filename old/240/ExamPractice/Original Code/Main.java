package com.example;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.Random;


public class Main {

	/**
	 * 1) Dictionary file name
   * 2) word length (int >= 2)
   * 3) number of guesses (int >= 1)
	 */
	public static void main(String[] args) throws IOException {

		File f = new File(args[0]);
		int wordLength = Integer.parseInt(args[1]);
    int guesses = Integer.parseInt(args[2]);

		EvilHangmanGame game = new EvilHangmanGame();

		game.startGame(f, wordLength);
		
		Scanner sc = new Scanner(System.in);
		while (guesses > 0) {
			System.out.println("You have " + guesses + " guesses left");
			System.out.print("Used letters: ");
			for (String used : game.getPrevGuesses()) {
				System.out.print(used + " ");
			}
			System.out.println();
			System.out.println("Word: " + game.getWord());
			System.out.print("Enter guess: ");
			String s = sc.next();
			while (!game.checkGuess(s)) {
				System.out.println("Guess may only be a single letter (a-z).");
				s = sc.next();
			}
			try {
				String saveWord = game.getWord();
				game.makeGuess(s.toLowerCase().charAt(0));
				if (game.getWord().equals(saveWord)) {
					guesses--;
				}
				int counter = 0;
				for (int i = 0; i < wordLength; i++) {
					if (!Character.isLetter(game.getWord().charAt(i))) {
						counter++;
					}
				}
				if (counter == 0) {
					System.out.println("The word was: " + game.getWord());
					System.out.println("You win!");
					System.out.println("...??");
					return;
				}
			} catch (EvilHangmanGame.GuessAlreadyMadeException e) {
				System.out.println("That letter has already been guessed!\n");
			}
		}
		Random rand = new Random();
		int  n = rand.nextInt(game.getDict().size()) + 1;
		int cnt = 1;
		for (String s : game.getDict()) {
			if (cnt == n) {
				System.out.println("You lose!");
				System.out.println("The word was: " + s);
				return;
			}
			cnt++;
		}

	}
}
