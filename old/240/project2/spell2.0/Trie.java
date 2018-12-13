package spell;

import java.util.TreeSet;

public class Trie implements ITrie {
	private Node root = new Node();
	private int word_cnt;
	private int node_cnt = 1;


	public void add(String word) {
		root.add(word);
	}

	public Node find(String word) {
		return root.find(word);
	}

	public Node getRoot() {
		return root;
	}


	public int getWordCount() {
		return word_cnt;
	}

	public int getNodeCount() {
		return node_cnt;
	}

	@Override
	public String toString() {
		StringBuilder sb_word = new StringBuilder();
		StringBuilder sb_list = new StringBuilder();
		root.toStringHelper(sb_word, sb_list);
		return sb_list.toString();
	}

	@Override
	public int hashCode() {
		return node_cnt * word_cnt * 59;
	}

	@Override
	public boolean equals(Object o) {
		// is null, is a Trie, is the same Trie
		if (o == null || o.getClass() != this.getClass()) {
			return false;
		}
		else {
			Trie t = (Trie)o;
			if (t.getNodeCount() != this.getNodeCount()
					|| t.getWordCount() != this.getWordCount()) {
				return false;
			}
			else {
				return equalsHelper(this.root, t.getRoot());
			}
		}
	}

	public boolean equalsHelper(Node n1, Node n2) {
		if (n1 == null && n2 == null) return true;
		else if (n1 == null || n2 == null) return false;
		else {
			if (n1.freq != n2.freq) return false;
			else  {
				for (int i = 0; i < 26; i++) {
					if (!equalsHelper(n1.nodes[i], n2.nodes[i])) {
						return false;
					}
				}
				return true;
			}
		}
	}

	public class Node implements ITrie.INode {

		private Node[] nodes = new Node[26];
		private int freq;
		
		public Node() {
			freq = 0;
		}

		public void toStringHelper(StringBuilder word, StringBuilder list) {
			if (freq > 0) {
				word.append("\n");
				list.append(word);
				word.setLength(word.length()-1);
			}
			for (int i = 0; i < 26; i++) {
				if (this.nodes[i] != null) {
					word.append((char)(i+'a'));
					this.nodes[i].toStringHelper(word, list);
					word.setLength(word.length()-1);
				}
			}
		}

		public void add(String word) {
			if (word.equals("")) {
				if (freq == 0) {
					word_cnt++;
				}
				freq++;
				return;
			}
			char c = word.charAt(0);
			if (nodes[c-'a'] == null) {
				nodes[c-'a'] = new Node();
				node_cnt++;
			}
			nodes[c-'a'].add(word.substring(1));
		}

		public Node find(String word) {
			if (word.equals("")) {
				if (freq == 0) {
					return null;
				}
				return this;
			}
			char c = word.charAt(0);
			if (nodes[c-'a'] == null) {
				return null;
			}
			return nodes[c-'a'].find(word.substring(1));
		}

		public int getValue() {
			return freq;
		}
	}
}
