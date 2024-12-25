import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class User extends JFrame implements ActionListener{
	BookTickets b = new BookTickets();

	private JButton display, book;
	public User(){
		super("User");
		setSize(400,400);
		setVisible(false);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setBackground(new Color(14,75,119));

		c.setLayout(null);
		display = new JButton("Display available trips");
		display.setBackground(new Color(187,225,248));
		display.setBounds(100,200,60,40);

		book = new JButton("Book Tickets");
		book.setBackground(new Color(187,225,248));
		book.setBounds(100,300,60,40);

		c.add(display);
		c.add(book);

		display.addActionListener(this);
		book.addActionListener(this);
		}

		public void actionPerformed(ActionEvent e){
			if(e.getSource() == display){
				DBC d = new DBC();
				d.connect();
				d.exStatement("select * from trips");
				d.processInfo("bus number\tpickup \tdrop \tseats \tcost","Display available trips");
				d.closeConnection();
				}else{
					b.setVisible(true);
					}
			}
	}