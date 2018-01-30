package dbtLab3;

import java.sql.ResultSet;
import java.sql.SQLException;

public class Show {
    private String theaterName;
    private String movie_name;
    private String date;

    public Show(ResultSet rs) {
        try {
            theaterName = rs.getString("theater_name");
            movie_name = rs.getString("movie_name");
            date = rs.getString("show_date");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public String getTheaterName() {
        return theaterName;
    }

    public String getMovieName() {
        return movie_name;
    }

    public String getShowdate() {
        return date;
    }
}
