package javadocExamplesFor240;

/**
 *A Date consisting of a day, month, and year.
 *<pre>
 *<b>Domain</b>:
 *     day : int
 *     month : int
 *     year : int
 *		
 *     <b>Invariant</b>:
 *         1 &le; month &le; 12 AND
 *         1 &le; year &le; 9999 AND
 *         day &ge; 1 AND
 *         month = 1, 3, 5, 7, 8, 10, 12  &rArr; day &le; 31 AND
 *         month = 4, 6, 9, 11 &rArr; day &le; 30 AND
 *         month = 2 &rArr;
 *             (year mod 4 &ne; 0 &rArr; day &le; 28)
 *             AND
 *             (year mod 4 = 0 &rArr;
 *                 (year mod 100 &ne; 0 &rArr; day &le; 29)
 *                 AND
 *                 (year mod 100 = 0 AND year mod 400 &ne; 0 &rArr; day &le; 28)
 *                 AND
 *                 (year mod 100 = 0 AND year mod 400 = 0 &rArr; day &le; 29)
 *             )
 *</pre>
 */
public class Date {
//Constructor
	/**
	 *The single constructor for the date.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * invariant(year, month, day)
	 * 
	 *<b>Result:</b>"
	 * this.year = year AND this.month = month AND this.day = day
	 *</pre>
	 *@param year the new year for the date
	 *@param month the new month for the date
	 *@param day the new day for the date
	 *@pre invariant(year, month, day)
	 *@throws AssertionError
	 */
	public Date(int year, int month, int day) {
		//To be implemented later
	}

	/**
	 *The getter for the field "day".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * None
	 *</pre>
	 *@return the day
	 */
	public int getDay() {
		//To be implemented later
		return 0;
	}

	/**
	 *The getter for the field "month".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * None
	 *</pre>
	 *@return the month
	 */
	public int getMonth() {
		//To be implemented later
		return 0;
	}

	/**
	 *The getter for the field "year".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * None
	 *</pre>
	 *@return the year
	 */
	public int getYear() {
		//To be implemented later
		return 0;
	}
	
	/**
	 *The toString method for a Date.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * None
	 *</pre>
	 *@return A string representation of a date that satisfies the following
	 *format: dd/dd/dddd.  If a day or month is a single digit then prepend with a
	 *'0'.  If the year is less than 4 digits prepend with enough '0' characters
	 *to make it 4 digits long.
	 */
	public String toString() {
		//To be implemented later
		return null;
	}

//Commands
	/**
	 *The setter for the field "day".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * the new day must be &ge; 1 AND the new day must be valid for the current month and current year.
	 *
	 *<b>Result</b>:
	 * this.day = day
	 *</pre>
	 *@param day the new day for this date
	 *@throws AssertionError
	 */
	public void setDay(int day) {
		//To be implemented later
	}

	/**
	 *The setter for the field "month".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * the month must be between 1 and 12 and the current day must be valid for the new month and current year.
	 *
	 *<b>Result</b>:
	 * this.month = month
	 *</pre>
	 *@param month the new month for this date
	 *@throws AssertionError
	 */
	public void setMonth(int month) {
		//To be implemented later
	}

	/**
	 *The setter for the field "year".
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * the year must be &ge; 1 and &le; 9999 AND the current day must be valid for the current month and new year.
	 *
	 *<b>Result</b>:
	 * this.year = year
	 *</pre>
	 *@param year the new year of the date
	 *@throws AssertionError
	 */
	public void setYear(int year) {
		//To be implemented later
	}
	
//Supporting Constants and Methods
	/**
	 *Implements the invariant.
	 *<pre>
	 *<b>Constraints on the input</b>:
	 * None
	 *</pre>
	 *@return
	 *<pre>
	 *if year is &ge; 0 AND year &le; 9999 AND the month is &ge; 1 AND &le; 12 AND the day &ge; 1 THEN
	 *  if month represents Jan, Mar, May, Jul, Aug, Oct, or Dec then result = day &le; 31 ELSE
	 *  if the month is Apr, Jun, Sep, or Nov then result = day &le; 30 ELSE
	 *  if the month is Feb THEN
	 *    if it is a leap year THEN
	 *      result = day &le; 29
	 *    else
	 *      result = day &le; 28
	 *else
	 *  result = false
	 *</pre>
	 *@param year  the year 
	 *@param month the month of the year
	 *@param day the day of the month
	 */
	private boolean invariant(int year, int month, int day) {
		//To be implemented laters
		return true;
	}
	
	/**
	 *Converts the number to a string representation.  It will be of length "numberOfDigits".  If necessary, to make the result long
	 *enough, the right number of the character '0' are added to the left.	 *<pre>
	 *<b>Constraints on the input</b>:
	 * number &ge; 0 AND |Integer.toString(number)| &le; numberOfDigits
	 *</pre>
	 *@return
	 *<pre>
	 *The result formatted such that:
	 *  |result| = numberOfDigits AND
	 *    &exist; 0 &le; i &le; numberOfDigits (result[i..|result|-1] = Integer.toString(number) AND 
	 *    &forall; 0 &le; j &lt; i (result[j] = '0'))
	 *</pre>
	 *@param number the number to be converted to a string
	 *@param numberOfDigits the length of the result
	 *@throws AssertionError
	 */
	private String convert(int number, int numberOfDigits) {
		//To be implemented later
		return null;
	}

}
