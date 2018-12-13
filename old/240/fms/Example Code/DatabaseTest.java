package dataaccess;

import org.junit.* ;

import java.util.Set;

import static org.junit.Assert.* ;

public class DatabaseTest {

    private Database db;

    @Before
    public void setUp() throws DatabaseException {
        db = new Database();
        db.openConnection();
        db.createTables();
        db.fillDictionary();
    }

    @After
    public void tearDown() throws DatabaseException {
        db.closeConnection(false);
        db = null;
    }

    @Test
    public void testLoadDictionaryFromDatabase() throws DatabaseException {

        Set<String> words = db.loadDictionary();

        assertEquals(4, words.size());
        assertTrue(words.contains("fred"));
        assertTrue(words.contains("barney"));
        assertTrue(words.contains("betty"));
        assertTrue(words.contains("wilma"));
    }
}
