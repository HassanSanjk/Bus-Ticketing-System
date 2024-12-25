import java.awt.*;
import javax.swing.*;

public class BookTickets extends JFrame{
	private JComboBox pickup , drop ,date;
	private JLabel maxSeats;
	private JTextField phone , seat;
	private JButton book;

	public BookTickets(){
		super("Book Tickets");
		setSize(600,400);
		setVisible(false);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setLayout(null);

		pickup = new JComboBox(new String[3]);
		pickup.setBounds(50,50,100,30);

		drop = new JComboBox(new String[3]);
		drop.setBounds(200,50,100,30);

		date = new JComboBox(new String[3]);
		date.setBounds(350,50,100,30);

		maxSeats = new JLabel("40");
		maxSeats.setBounds(50,200,10,30);

		phone = new JTextField(15);
		phone.setBounds(50,100,100,30);

		seat = new JTextField(5);
		seat.setBounds(70,200,50,30);

		book = new JButton("Book");
		book.setBounds(170,300,60,50);
		book.setBackground(Color.green);

		c.add(pickup);
		c.add(drop);
		c.add(date);
		c.add(maxSeats);
		c.add(phone);
		c.add(seat);
		c.add(book);
		}

	}