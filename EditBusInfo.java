import java.awt.*;
import javax.swing.*;

public class EditBusInfo extends JFrame{
	private JButton add;
	private JLabel label1,label2,label3,label4,label5,label6;
	private JTextField busNumber ,busColor, nmberOfStation ,driverName , PhoneNumber ,driverCardNumber ;
	private JButton edit;



	EditBusInfo(){
		super("Edit Bus Information ");
		setSize(300,400);
		setVisible(false);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setLayout(null);
		c.setBackground(new Color(14,75,119));

		label1 = new JLabel("Bus number :");
		label1.setBounds(10,10,100,20);
		label1.setForeground(new Color(187,225,248));

		label2 = new JLabel("Bus color :");
		label2.setBounds(10,40,100,20);
		label2.setForeground(new Color(187,225,248));

		label3 = new JLabel("Number of station :");
		label3 .setBounds(10,80,140,20);
		label3.setForeground(new Color(187,225,248));

		label4 = new JLabel("Driver name :");
		label4.setBounds(10,120,100,20);
		label4.setForeground(new Color(187,225,248));

		label5 = new JLabel("Phone number :");
		label5.setBounds(10,160,100,20);
		label5.setForeground(new Color(187,225,248));

		label6 = new JLabel("Driver card number :");
		label6.setBounds(10,200,140,20);
		label6.setForeground(new Color(187,225,248));

		edit = new JButton("Edit");
		edit.setBounds(100,250,100,50);
		edit.setBackground(new Color(187,225,248));

		c.add(label1);
		c.add(label2);
		c.add(label3);
		c.add(label4);
		c.add(label5);
		c.add(label6);
		c.add(edit);

		busNumber = new JTextField(50);
		busNumber.setBounds(150,10,100,20);

		busColor = new JTextField(50);
		busColor.setBounds(150,40,100,20);

		nmberOfStation = new JTextField(50);
		nmberOfStation.setBounds(150,80,100,20);

		driverName = new JTextField(50);
		driverName.setBounds(150,120,100,20);

		PhoneNumber = new JTextField(50);
		PhoneNumber.setBounds(150,160,100,20);

		driverCardNumber = new JTextField(50);
		driverCardNumber.setBounds(150,200,100,20);

		c.add(busNumber);
		c.add(busColor);
		c.add(nmberOfStation);
		c.add(driverName);
		c.add(PhoneNumber);
		c.add(driverCardNumber);


		}

	}