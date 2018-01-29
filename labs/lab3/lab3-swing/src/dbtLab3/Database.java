package dbtLab3;

import java.sql.*;
import java.util.*;

/**
 * Database is an interface to the college application database, it
 * uses JDBC to connect to a SQLite3 file.
 */
public class Database {

    /**
     * The database connection.
     */
    private Connection conn;

    /**
     * Creates the database interface object. Connection to the
     * database is performed later.
     */
    public Database() {
        conn = null;
    }

    /**
     * Opens a connection to the database, using the specified
     * filename (if we'd used a traditional DBMS, such as PostgreSQL
     * or MariaDB, we would have specified username and password
     * instead).
     */
    public boolean openConnection(String filename) {
        try {
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:" + filename);
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    /**
     * Closes the connection to the database.
     */
    public void closeConnection() {
        try {
            if (conn != null) {
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * Checks if the connection to the database has been established
     * 
     * @return true if the connection has been established
     */
    public boolean isConnected() {
        return conn != null;
    }
    
    public List<String> checkIfUserExists(String userId) {
        List<String> found = new LinkedList<>();
//        System.out.println(userId);
//        String query =
//            "SELECT  * \n" +
//            "FROM    users\n" 
//            ;
//        try (PreparedStatement ps = conn.prepareStatement(query)) {
////            ps.setString(1, ...);
//            ResultSet rs = ps.executeQuery();
//            while (rs.next()) {
////                found.add(new ...(rs));
//            }
//        } catch (SQLException e) {
//            e.printStackTrace();
//        }
        return found;
    }

    /* ================================== */
    /* --- insert your own code below --- */
    /* ===============================*== */

    /*
    public List<...> ...(...) {
        List<...> found = new LinkedList<>();
        String query =
            "SELECT  ...\n" +
            "FROM    ...\n" +
            "...\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, ...);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                found.add(new ...(rs));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return found;
    }
    */
}
