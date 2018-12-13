package javadocExamplesFor240;

/**
 *An object that contains all information returned when
 *"<i>validateUser</i>" is called.
 *<br>
 *<b>Domain:</b>
 *<pre>
 *  result          : ValidationResult 
 *  firstName       : String
 *  lastName        : String
 *  numberOfRecords : Non-negative integer
 *</pre>
 */
public class ValidateUserOutput {
//Constructors
	/**
	 *Creates the return object for the validate user command.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *   result &ne; null AND firstName &ne; null AND lastName &ne; null AND
	 *   numRecords &ge; 0 AND firstName.matches("[a-zA-z]+") AND
	 *   lastName.matches("[a-zA-Z]")
	 *
	 *<b>Result</b>
	 *   this.result = result AND this.firstName = firstName AND
	 *   this.lastName = lastName AND this.numRecords = numRecords
	 *</pre>
	 *@param result -- the result of the validation
	 *@param firstName -- the person's first name
	 *@param lastName -- the person's last name
	 *@param numRecords -- number of records
	 */
	public ValidateUserOutput(ValidationResult result, 
							  String firstName, 
							  String lastName, 
							  int numRecords)
	{
        //To be implemented later
	}

	/**
	 *The toString method
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return
	 *<pre>A lexical representation of an instance of this class that satisfies
	 *the following grammar:
	 *   "ValidateUserOutput [result=" result ", firstName=" firstName
	 *   ", lastName=" lastName ", numRecords=" numRecords "]"   
	 *</pre>
	 */
	@Override
	public String toString() {
		//To be implemented later
		return null;
	}

	/**
	 *Result getter.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the result.toString()
	 */
	public String getResult() {
		//To be implemented later
		return null;
	}

	/**
	 *FirstName getter.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the firstName
	 */
	public String getFirstName() {
		return null;
	}

	/**
	 *LastName getter.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the lastName
	 */
	public String getLastName() {
		//To be implemented later
		return null;
	}

	/**
	 *NumberOfRecords getter.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return the numberOfRecords
	 */
	public int getNumRecords() {
		//To be implemented later
		return 0;
	}
}
