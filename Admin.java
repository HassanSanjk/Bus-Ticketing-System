import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Admin extends JFrame implements ActionListener{
	AddBus a= new AddBus();
	EditBusInfo b = new EditBusInfo();
	AddTravelOrTrip c = new AddTravelOrTrip();
	EditTravelOrTrip d = new EditTravelOrTrip();

	private JLabel l;
	private JPanel p;
	private JButton addBus, displayBusses, editBus, deleteBus, addTrip, displayTrips, editTrips, deleteTrips;
	public Admin(){
		super("Admin");
		setSize(400,500);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setLayout(null);
		c.setBackground(new Color(14,75,119));

		ImageIcon ad = new ImageIcon(new ImageIcon("Pics/admin.png").getImage().getScaledInstance(100, 100, Image.SCALE_SMOOTH));
		l = new JLabel("Welcome Admin");
		l.setIcon(ad);
		l.setBounds(0,0,400,100);
		l.setBackground(new Color(50,130,181));
		l.setHorizontalAlignment(JLabel.CENTER);
		l.setOpaque(true);
		l.setFont(new Font("Serif",Font.BOLD,35));

		p = new JPanel();
		p.setLayout(new GridLayout(4,2,10,10));
		p.setBounds(10,110,360,340);
		p.setBackground(new Color(14,75,119));

		addBus = new JButton("Add a Bus");
		addBus.setBackground(new Color(187,225,248));

		displayBusses = new JButton("Display busses");
		displayBusses.setBackground(new Color(187,225,248));

		editBus = new JButton("Edit a bus");
		editBus.setBackground(new Color(187,225,248));

		deleteBus = new JButton("Delete a bus");
		deleteBus.setBackground(new Color(187,225,248));

		addTrip = new JButton("add a trip");
		addTrip.setBackground(new Color(187,225,248));

		displayTrips = new JButton("display trips");
		displayTrips.setBackground(new Color(187,225,248));

		editTrips = new JButton("edit trips");
		editTrips.setBackground(new Color(187,225,248));

		deleteTrips = new JButton("delete trips");
		deleteTrips.setBackground(new Color(187,225,248));

		addBus.setFocusable(false);
		displayBusses.setFocusable(false);
		editBus.setFocusable(false);
		deleteBus.setFocusable(false);
		addTrip.setFocusable(false);
		displayTrips.setFocusable(false);
		editTrips.setFocusable(false);
		deleteTrips.setFocusable(false);


		addBus.addActionListener(this);
		displayBusses.addActionListener(this);
		editBus.addActionListener(this);
		deleteBus.addActionListener(this);
		addTrip.addActionListener(this);
		displayTrips.addActionListener(this);
		editTrips.addActionListener(this);
		deleteTrips.addActionListener(this);

		p.add(addBus);
		p.add(displayBusses);
		p.add(editBus);
		p.add(deleteBus);
		p.add(addTrip);
		p.add(displayTrips);
		p.add(editTrips);
		p.add(deleteTrips);

		c.add(p);
		c.add(l);


		}
			public void actionPerformed(ActionEvent e){
				if (e.getSource() == addBus)
				a.setVisible(true);
				else if (e.getSource() == editBus)
				b.setVisible(true);
				else if (e.getSource() == addTrip)
				c.setVisible(true);
				else if (e.getSource() == editTrips)
				d.setVisible(true);

				}

	}