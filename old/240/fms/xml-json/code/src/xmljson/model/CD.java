package xmljson.model;

public class CD {

	private String title;
	private String artist;
	private String country;
	private String company;
	private float price;
	private int year;
	
	// Used for object deserialization
	private CD() {
	}
	
	public CD(String title, String artist, String country,
				String company, float price, int year) {
		setTitle(title);
		setArtist(artist);
		setCountry(country);
		setCompany(company);
		setPrice(price);
		setYear(year);
	}
	
	public String getTitle() {
		return title;
	}
	
	public void setTitle(String title) {
		this.title = title;
	}
	
	public String getArtist() {
		return artist;
	}
	
	public void setArtist(String artist) {
		this.artist = artist;
	}
	
	public String getCountry() {
		return country;
	}
	
	public void setCountry(String country) {
		this.country = country;
	}
	
	public String getCompany() {
		return company;
	}
	
	public void setCompany(String company) {
		this.company = company;
	}
	
	public float getPrice() {
		return price;
	}
	
	public void setPrice(float price) {
		this.price = price;
	}
	
	public int getYear() {
		return year;
	}
	
	public void setYear(int year) {
		this.year = year;
	}

}
