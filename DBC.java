import java.sql.*;
import javax.swing.*;

public class DBC{
	private Connection connection;
	private Statement statement;
	private ResultSet resultSet;
	public DBC(){}

	public void connect(){
		try{
					System.out.println("We start");
					Class.forName("com.mysql.cj.jdbc.Driver");
					System.out.println("driver Loaded");
					connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/busdb","root@localhost","");
					System.out.println("Database connected");
					statement = connection.createStatement();
				}catch (SQLException sql){
					JOptionPane.showMessageDialog(null,sql.getMessage(),"DataBase Error",JOptionPane.ERROR_MESSAGE);
					//System.exit(1);
					}catch (ClassNotFoundException e){
						JOptionPane.showMessageDialog(null,"CLASS NOT FOUND","Error CLASS NOT FOUND",JOptionPane.ERROR_MESSAGE);
						System.exit(1);
						}
		}

	public void closeConnection(){
		try{
			connection.close();
			}catch(SQLException sql){
				JOptionPane.showMessageDialog(null,sql.getMessage(),"DataBase Error",JOptionPane.ERROR_MESSAGE);
				//System.exit(1);
				}
		}

	public void exStatement(String stmn){
		try{
		resultSet = statement.executeQuery(stmn);
		}catch(SQLException sql){				JOptionPane.showMessageDialog(null,sql.getMessage(),"DataBase Error",JOptionPane.ERROR_MESSAGE);
}
		}

	public void processInfo(String output,String name){
		try{
		while (resultSet.next()){
			output += "\n"+resultSet.getString(1)+"\t"+resultSet.getString(2)+"\t"+resultSet.getString(3)+"\t"+resultSet.getString(4)+"\t"+resultSet.getString(5);
			}

		JOptionPane.showMessageDialog(null,output,name,JOptionPane.INFORMATION_MESSAGE);

}catch(SQLException sql){				JOptionPane.showMessageDialog(null,sql.getMessage(),"DataBase Error",JOptionPane.ERROR_MESSAGE);
}
		}




}