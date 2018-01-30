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
                movies.add(rs.getString("name"));
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

    public int getFreeSeats(String theaterName, String date) {
        int seats = 0;
        String query =
                "SELECT  * \n" +
                "FROM    theaters \n" +
                "WHERE name = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, theaterName);
            ResultSet rs = ps.executeQuery();
            while(rs.next())
                seats = rs.getInt("seats");
            int nbr = getNumberOfReservations(theaterName, date);
            return seats - nbr;
        } catch (SQLException e) {
            e.printStackTrace();
            return 0;
        }
    }

    public int getNumberOfReservations(String theaterName, String date) {
        String query =
                "SELECT  COUNT() as cnt \n" +
                        "FROM    reservations \n" +
                        "WHERE theater_name = ? AND show_date = ?\n";
        try (PreparedStatement ps = conn.prepareStatement(query)) {
            ps.setString(1, theaterName);
            ps.setString(2, date);
            ResultSet rs = ps.executeQuery();
            while(rs.next())
                return rs.getInt("cnt");
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
        String id = "SELECT last_insert_rowid()";
        try (PreparedStatement ps = conn.prepareStatement(query, new String []{"res_nbr"})) {
            PreparedStatement psmt = conn.prepareStatement(id);
            ps.setString(1, username);
            ps.setString(2, movieName);
            ps.setString(3, theaterName);
            ps.setString(4, date);
            ps.executeUpdate();
            ResultSet rs = psmt.executeQuery();
            return rs.getInt(1);

        } catch (SQLException e) {
            e.printStackTrace();
            return 0;
        }
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
