package javadocExamplesFor240;

/**
 * A US phone number with area code and 7 digit number.
 * <pre>
 * <b>Domain</b>
 *    areaCode: String
 *    number  : String
 *     
 *    <i>Invariants</i>: areaCode.matches("\d{3}") AND
 *                number.matches("\d{7}")
 * </pre>
 */
public class PhoneNumber {
//Constructors
	/**
	 *The only constructor for an phone number.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  areaCode.matches("\d{3}") AND number.matches("\d{7}")
	 *  
	 *<b>Result:</b>"
	 *  this.areaCode = areaCode AND this.number = number
	 *</pre>
	 * @param areaCode the area code of a phone number
	 * @param number the number after the area code in a phone number
	 * @throws AssertionError
	 */
	public PhoneNumber(String areaCode, String number) {
		//To be implemented later
	}
	
	/**
	 *AreaCode getter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 * @return the areaCode
	 */
	public String getAreaCode() {
		//To be implemented later
		return null;
	}
	
	/**
	 *Number getter
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 * @return the number
	 */
	public String getNumber() {
		//To be implemented later
		return null;
	}
	
	/**
	 * Returns a string representation of the phone number.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 *  None
	 *</pre>
	 *@return a string satisfying the following syntax:<br>
	 *  "(" areaCode ") " number.substring(0,3) "-" number.substring(3)
	 */
	@Override
	public String toString() {
		//To be implemented later
		return null;
	}
}
