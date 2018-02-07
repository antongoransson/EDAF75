package dbtLab3;

import java.sql.ResultSet;
import java.sql.SQLException;

public class Show {
    public final String theaterName;
    public final String movie_name;
    public final String date;

    public Show(ResultSet rs) throws SQLException {
        this.theaterName = rs.getString("theater_name");
        this.movie_name = rs.getString("movie_name");
        this.date = rs.getString("show_date");
    }

}
