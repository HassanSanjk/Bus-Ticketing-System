import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Login extends JFrame implements ActionListener{
	Admin a = new Admin();
	private JLabel l1, l2 , l0;
	private JTextField t;
	private JPasswordField p;
	private JButton login;

	public Login(){
		super("Login");
		setSize(400,400);
		setVisible(false);
		setLocationRelativeTo(null);

		Container c = getContentPane();
		c.setLayout(null);
		c.setBackground(new Color(50,130,181));


		l0 = new JLabel("Login");
		l0.setFont(new Font("Serif",Font.BOLD,45));
		l0.setHorizontalAlignment(JLabel.CENTER);
		l0.setForeground(new Color(187,225,248));
		l0.setBounds(0,0,400,100);

		l1 = new JLabel("Username:");
		l1.setBounds(50,140,100,40);
		l1.setForeground(new Color(187,225,248));
		l1.setFont(new Font("Serif",Font.BOLD,20));

		l2 = new JLabel("Password:");
		l2.setBounds(50,200,100,40);
		l2.setForeground(new Color(187,225,248));
		l2.setFont(new Font("Serif",Font.BOLD,20));

		t = new JTextField();
		t.setBounds(170,150,150,30);
		t.setFont(new Font("Serif",Font.PLAIN,16));

		p = new JPasswordField();
		p.setBounds(170,210,150,30);

		login = new JButton("Login");
		login.setBounds(150,270,100,50);
		login.setFont(new Font("Serif",Font.PLAIN,22));
		login.setBackground(new Color(187,225,248));
		login.setFocusable(false);
		login.addActionListener(this);

		c.add(l0);
		c.add(l1);
		c.add(l2);
		c.add(t);
		c.add(p);
		c.add(login);
		}
	public void actionPerformed(ActionEvent e){
		if(t.getText().equals("Hassan") && p.getText().equals("Osama")){
			System.out.print(p.getPassword());
			a.setVisible(true);
			this.setVisible(false);
			}else{
				JOptionPane.showMessageDialog(null,"Invalid Username or Password","Error Invalid Input",JOptionPane.ERROR_MESSAGE);
				}


		}


	public static void main(String args[]){
		Login l = new Login();
	}
	}