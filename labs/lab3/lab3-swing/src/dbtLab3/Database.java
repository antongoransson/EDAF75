package dbtLab3;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

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

    public boolean userExists(String userId) {
        String query =
            "SELECT  * \n" +
            "FROM    users\n" +
            "WHERE username = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, userId);
            ResultSet rs = ps.executeQuery();
            return rs.next();
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public List<String> getMovies() {
        List<String> movies = new ArrayList<String>();
        String query =
            "SELECT  * \n" +
            "FROM    movies\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ResultSet rs = ps.executeQuery();
            while(rs.next())
                movies.add(rs.getString("movie_name"));
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
        return movies;
    }

    public List<String> getDates(String movieName) {
        List<String> dates = new ArrayList<String>();
        String query =
                "SELECT  * \n" +
                "FROM    shows \n" +
                "WHERE movie_name = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, movieName);
            ResultSet rs = ps.executeQuery();
            while(rs.next())
                dates.add(rs.getString("show_date"));
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
        return dates;
    }
    public List<Show> getPerformance(String movieName, String date) {
        List<Show> shows = new ArrayList<Show>();
        String query =
            "SELECT  * \n" +
            "FROM    shows \n" +
            "WHERE movie_name = ? AND show_date = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, movieName);
            ps.setString(2, date);
            ResultSet rs = ps.executeQuery();
            while(rs.next())
                shows.add(new Show(rs));
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
        return shows;
    }

    public int getFreeSeats(String movieName, String date) {
        String query =
            "SELECT   *, seats, seats - COUNT() free_seats\n" +
            "FROM SHOWS \n" +
            "LEFT JOIN reservations \n" +
            "USING (movie_name, show_date) \n" +
            "JOIN theaters \n" +
            "USING (theater_name) \n" +
            "WHERE movie_name = ? AND show_date = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, movieName);
            ps.setString(2, date);
            ResultSet rs = ps.executeQuery();
            if(rs.next()) {
                if(rs.getInt("res_nbr") == 0)
                    return rs.getInt("seats");
                return rs.getInt("free_seats");
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return 0;
        }
        return 0;
    }


    public int makeReservation(String username, String movieName, String theaterName, String date) {
        String query =
            "INSERT \n" +
            "INTO reservations(username, theater_name, movie_name, show_date) \n" +
            "VALUES(?, ?, ?, ?)\n";
        int res_id = -1;
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, username);
            ps.setString(2, movieName);
            ps.setString(3, theaterName);
            ps.setString(4, date);
            ps.executeUpdate();
            ResultSet rs = ps.getGeneratedKeys();
            if (rs.next()) {
                res_id =  rs.getInt(1);
            }
            return res_id;
        } catch (SQLException e) {
            e.printStackTrace();
            return 0;
        }
    }
}
