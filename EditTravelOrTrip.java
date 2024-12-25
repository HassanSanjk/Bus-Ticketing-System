import java.awt.*;
import javax.swing.*;


public class EditTravelOrTrip extends JFrame{
	private JComboBox pickup , dropStation, busNumber,numberOfSeats;
	private JButton edit;

	private String[] name1 = {"Pickup"};
	private String[] name2 = {"Drop Station"};
	private String[] name3 = {"bus Number"};
	private String[]name4 = {"number Of Seats"};

	EditTravelOrTrip(){
		super("Edit Travel Or Trip");
		setSize(300,400);
		setVisible(false);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setLayout(null);
		c.setBackground(new Color(14,75,119));

		//c.setBackground( Color.gray);
		pickup = new JComboBox(name1);
		pickup.setBounds(30,20,100,20);
		pickup.setBackground(Color.red);
		dropStation = new JComboBox(name2);
		dropStation.setBounds(30,60,100,20);
		pickup.setForeground(Color.blue);
		busNumber = new JComboBox(name3);
		busNumber.setBounds(170,20,100,20);

		numberOfSeats = new JComboBox(name4);
		numberOfSeats.setBounds(170,40,100,20);

		edit = new JButton("Edit");
		edit.setBounds(130,300,40,20);
		edit.setBackground(new Color(187,225,248));

		c.add(pickup);
		c.add(dropStation);
		c.add(busNumber);
		c.add(numberOfSeats);
		c.add(edit);
		}

	}