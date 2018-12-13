package javadocExamplesFor240;

import java.util.List;

/**
 *A student in a teacher's class.
 *<pre>
 *<b>Domain</b>:
 *   id           : int     -- The unique id for the student
 *   name         : String         
 *   phoneNumbers : List<PhoneNumber>    -- May be an empty list
 *
 *   <i>Invariant</i>: id &ge; 0 AND isAlphabetic(name) AND |name| &ge; 1
 *</pre>
 */
public class Student {

//Constructors
	/**
	 *The only constructor for a Student. It is a domain initialization
	 *constructor
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  id &ge; 0 AND name &ne; null AND phoneNumbers &ne; null AND
	 *  name.matches("[a-zA-Z]+")
	 *  
	 *<b>Result:</b>"
	 *  this.id = id AND this.name = name AND this.phoneNumbers = phoneNumbers
	 *</pre>
	 *@param id the id of a student
	 *@param name the name of a student
	 *@param phoneNumbers the list of phone numbers of a student,
	 *     possible empty
	 *@throws AssertionError
	 */
	public Student(int id, String name, List<PhoneNumber> phoneNumbers) {
		//To be implemented later
	}

//Queries	
	/**
	 * Id getter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the id
	 */
	public int getId() {
		//To be implemented later
		return 0;
	}

	/**
	 * Name getter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the name
	 */
	public String getName() {
		//To be implemented later
		return null;
	}

	/**
	 *PhoneNumbers getter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the phoneNumbers
	 */
	public List<PhoneNumber> getPhoneNumbers() {
		//To be implemented later
		return null;
	}

	/**
	 * Id setter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  id &ge; 0
	 *  
	 *<b>Result</b>:
	 *  this.id = id
	 *</pre>
	 *@param id the id to set
	 *@throws AssertionError
	 */
	public void setId(int id) {
		//To be implemented later
	}

	/**
	 * Name setter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  name &ne; null AND name.matches("[a-zA-Z]+")
	 *
	 *<b>Result</b>:
	 *  this.name = name
	 *</pre>
	 *@param name the name to set
	 *@throws AssertionError
	 */
	public void setName(String name) {
		//To be implemented later
	}

	/**
	 * PhoneNumbers setter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  phoneNumbers &ne; null
	 *
	 *<b>Result</b>:
	 *  this.phoneNumbers = phoneNumbers
	 *</pre>
	 *@param phoneNumbers the phoneNumbers to set
	 *@throws AssertionError
	 */
	public void setPhoneNumbers(List<PhoneNumber> phoneNumbers) {
		//To be implemented later
	}

	/**
	 *The toString method for a student
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *
	 *<b>Result</b>:
	 *  result satisfies the following syntax:
	 *      "Student [id=" id ", name=" name ", phoneNumbers=" phoneNumbers "]"
	 *</pre>
	 */
	@Override
	public String toString() {
		//To be implemented later
		return null;
	}
}
