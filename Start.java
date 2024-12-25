import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Start extends JFrame implements ActionListener{
	private JButton admin,user;
	private JLabel title,la,lu;
	User u = new User();
	Login l = new Login();

	public Start(){
		super ("Bus Ticketing Syatem");
		setSize(400,400);
		setVisible(true);
		setLocationRelativeTo(null);

		Container c =getContentPane();
		ImageIcon ad = new ImageIcon(new ImageIcon("Pics/admin.png").getImage().getScaledInstance(100, 100, Image.SCALE_SMOOTH));
		ImageIcon us = new ImageIcon(new ImageIcon("Pics/user.png").getImage().getScaledInstance(100, 100, Image.SCALE_SMOOTH));
		c.setLayout(null);
		admin = new JButton("Admin");
		user = new JButton("User");


		c.setBackground(new Color(14,75,119));

		title = new JLabel("Bus Ticketing System");
		la = new JLabel(ad);
		lu = new JLabel(us);
		//la.setOpaque(true);
		//lu.setOpaque(true);

		title.setBounds(0,0,400,50);
		title.setBackground(new Color(50,130,181));
		title.setForeground(Color.black);
		title.setFont(new Font("Serif",Font.BOLD,32));
		title.setHorizontalAlignment(JLabel.CENTER);
		title.setOpaque(true);

		la.setBounds(66,50,100,100);
		lu.setBounds(230,50,100,100);
		admin.setBounds(66,150,100,70);
		admin.setFocusable(false);

		user.setBounds(230,150,100,70);
		user.setFocusable(false);

		admin.addActionListener(this);
		user.addActionListener(this);

		admin.setBackground(new Color(187,225,248));
		user.setBackground(new Color(187,225,248));

		c.add(title);
		c.add(la);
		c.add(lu);
		c.add(admin);
		c.add(user);

		setVisible(true);

		}

		public void actionPerformed(ActionEvent e){
			if(e.getSource() == user){
			u.setVisible(true);
		}else{
			l.setVisible(true);
			}
		this.setVisible(false);
			}

	}