import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.channels.Selector;
import java.util.InputMismatchException;
import java.util.Scanner;
import java.util.StringTokenizer;
import java.util.Vector;

/**
 * Created by Grant Callant. JaRPS
 *
 * @author Grant Callant
 */
public class Server
{
	public static void main(String[] args)
	{
		Server server = new Server();
	}

	private static Vector<Socket>             clientSockets = null;
	private static Vector<String>             clientName    = null;
	private        ServerSocket               serverSocket  = null;
	private        Socket                     servSocket    = null;
	private        String                     name          = "";
	private        Scanner                    scanner       = null;
	private        Selector select = null;
	private boolean inGame = true;

	private Server()
	{
		boolean valid = false;
		int port = -1;
		while(!valid || port < 0)
		{
			scanner = new Scanner(System.in);
			clientSockets = new Vector<>();
			clientName = new Vector<>();
			try
			{
				System.out.println("Enter port");
				port = scanner.nextInt();
				if(port < 1000 || port > 65535)
				{
					port = -1;
					throw new InputMismatchException();
				}
				serverSocket = new ServerSocket(port);
				valid = true;
				while(true)
				{
					servSocket = serverSocket.accept();
					Listen listener = new Listen(servSocket);
				}
			}
			catch(IOException e)
			{
				e.printStackTrace();
			}
			catch(InputMismatchException e)
			{
				System.out.println("Usage: 1000- 65535");
			}
		}
		try
		{
			select = Selector.open();
		}
		catch(IOException e)
		{
			e.printStackTrace();
		}
	}

	private class Listen extends Thread
	{
		private Socket           clientSocket     = null;
		private DataInputStream  dataInputStream  = null;
		private DataOutputStream dataOutputStream = null;

		private Listen(Socket socket)
		{
			clientSocket = socket;
			try
			{
				dataInputStream = new DataInputStream(socket.getInputStream());
				dataOutputStream = new DataOutputStream(socket.getOutputStream());

				name = dataInputStream.readUTF();

				System.out.println(name + " joined.");

				clientName.add(name);
				clientSockets.add(clientSocket);
				start();
			}
			catch(IOException e)
			{
				e.printStackTrace();
			}
		}

		public void run()
		{
			while(true)
			{
				String clientMessage = "";
				StringTokenizer stringTokenizer = null;
				String clientDestination = "";
				String from = "";
				String messageType = "";
				try
				{
					clientMessage = dataInputStream.readUTF();
					stringTokenizer = new StringTokenizer(clientMessage);
					clientDestination = stringTokenizer.nextToken();
					messageType = stringTokenizer.nextToken();
					from = stringTokenizer.nextToken();

					if(messageType.compareToIgnoreCase("Quit") == 0)
					{
						for(int i = 0; i < clientName.size(); i++)
						{
							if(clientName.elementAt(i).compareToIgnoreCase(clientDestination) == 0)
							{
								clientName.removeElementAt(i);
								clientSockets.removeElementAt(i);
								System.out.println(clientDestination + " Disconnected from session.");
								break;
							}
						}
					}
					else
					{
						String message ="";
						while(stringTokenizer.hasMoreTokens())
						{
							message += " " + stringTokenizer.nextToken();
						}

						for(int i = 0; i < clientName.size(); i++)
						{
							if(clientDestination.compareToIgnoreCase("everyone") == 0)
							{
								new DataOutputStream(clientSockets.elementAt(i).getOutputStream()).writeUTF(from + ": " + message);
							}
							else if(clientName.elementAt(i).compareToIgnoreCase(clientDestination) == 0)
							{
								new DataOutputStream(clientSockets.elementAt(i).getOutputStream()).writeUTF(from + ": " + message);
								break;
							}
						}
					}
					if(messageType.compareToIgnoreCase("Quit") == 0)
					{
						break;
					}
				}
				catch(IOException e)
				{
					e.printStackTrace();
				}
			}
		}
	}

}
